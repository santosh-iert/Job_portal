from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.status import HTTP_400_BAD_REQUEST

from Job_Portal.settings import EMAIL_HOST_USER
from applicants.models import AppliedJobs
from applicants.serializers import AppliedJobsSerializer
from job_function.models import PostedJobs
from job_function.serializers import PostedJobsSerializer


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def job_apply(request):
    try:
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = AppliedJobsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            job_obj = PostedJobs.objects.get(id=data.get('jobId'))
            # Send mail to Candidate
            user_email = user.email
            subject = f"Thank You for Applying {job_obj.job_title}"
            message = (f"Dear {user.first_name},\n\n"
                       f"Thank you for applying for the {job_obj.job_title} position .")
            send_mail(subject, message, EMAIL_HOST_USER, [user_email])
            # Send mail to Recruiter
            recruiter_message = (f"Dear {job_obj.postedBy.first_name},\n\n"
                       f"{user.first_name} successfully applied for the {job_obj.job_title}.")
            recruiter_email = job_obj.postedBy.email
            send_mail(f"{user.first_name} {user.last_name} applied for the {job_obj.job_title}",
                      recruiter_message, EMAIL_HOST_USER, [recruiter_email])
            return JsonResponse({"message": "Successfully Applied for the Job", "data": serializer.data}, status=201)
        return JsonResponse(serializer.errors, status=400)
    except ValidationError as vr:
        return JsonResponse({'error': "You have already applied for this job"}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def jobs_applied(request):
    try:
        user = request.user
        applied_jobs = AppliedJobs.objects.filter(user=user)
        serializer = AppliedJobsSerializer(applied_jobs, many=True)
        return JsonResponse({"message": "Applied Jobs", "data": serializer.data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(['GET'])
def available_jobs(request):
    try:
        posted_jobs = PostedJobs.objects.all()
        serializer = PostedJobsSerializer(posted_jobs, many=True)
        return JsonResponse({"message": "Available Jobs to apply", "data": serializer.data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



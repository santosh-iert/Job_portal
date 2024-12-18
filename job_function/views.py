from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from applicants.models import AppliedJobs
from applicants.serializers import AppliedJobsSerializer
from job_function.models import PostedJobs
from job_function.serializers import PostedJobsSerializer


# @csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_job(request):
    try:
        user = request.user
        data = request.data
        data['postedBy'] = user.id
        serializer = PostedJobsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Successfully Posted New Job", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_post_jobs(request):
    try:
        user = request.user
        posted_jobs = PostedJobs.objects.filter(postedBy=user)
        # posted_jobs = PostedJobs.objects.all()
        serializer = PostedJobsSerializer(posted_jobs, many=True)
        return JsonResponse({"message": "Posted Jobs", "data": serializer.data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_applicants(request, job_id):
    try:
        applied_jobs = AppliedJobs.objects.filter(jobId=job_id)
        serializer = AppliedJobsSerializer(applied_jobs, many=True)

        return JsonResponse({"message": "Applied Candidates for the given Job ID", "data": serializer.data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

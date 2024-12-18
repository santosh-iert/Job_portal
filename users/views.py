from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# from django.contrib.auth.hashers import make_password, check_password


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserLoginView(APIView):
    def post(self, request):
        try:
            user_email = request.data.get('email')
            password = request.data.get('password')
            user_model = get_user_model()
            user = user_model.objects.get(email=user_email)
            if user and user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "message": "Login successful!"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print("Error==>", str(e))
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:

            request.user.auth_token.delete()
            return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



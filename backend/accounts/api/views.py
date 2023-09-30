from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserLoginSerializer, UserSignupSerializer
from .permissions import IsAnonymous, IsAuthenticated


class UserLoginView(APIView):
    permission_classes = (IsAnonymous,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        payload = request.data
        serializer = self.serializer_class(data=payload)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.data["username"],
                password=serializer.data["password"],
            )
            if not user:
                response = {"message": "provided credentials are not provided!"}
                code = status.HTTP_403_FORBIDDEN
            else:
                login(request, user)
                response = {"message": "you logged in successfully!"}
                code = status.HTTP_200_OK
        else:
            response = {"message": "something went wrong!", "error": serializer.errors}
            code = status.HTTP_403_FORBIDDEN
        return Response(data=response, status=code)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request=request)
        response = {"message": "you logged out successfully!"}
        code = status.HTTP_200_OK
        return Response(data=response, status=code)


class UserRegisterView(APIView):
    serializer_class = UserSignupSerializer

    def post(self, request):
        payload = request.data
        serializer = self.serializer_class(data=payload)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            response = {"message": "you signed up successfully!"}
            code = status.HTTP_201_CREATED
        else:
            response = {"message": "something went wrong!"}
            code = status.HTTP_403_FORBIDDEN
        return Response(data=response, status=code)

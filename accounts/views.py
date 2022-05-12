from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import LoginSerializer
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]

            return Response({'token':token.key})

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

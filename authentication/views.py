from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate


class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = request.data
        if "username" not in data or "password" not in data:
            return Response(
                {"error": "Must provide username and password"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = authenticate(username=data["username"], password=data["password"])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

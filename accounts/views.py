from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, UserSerializer


class LoginView(APIView):


    permission_classes = [AllowAny]

    def post(self, request):
        serailizer = LoginSerializer(data=request.data)
        serailizer.is_valid(raise_exception=True)

        usr = authenticate(
            username=serailizer.validated_data["username"],
            password=serailizer.validated_data["password"],
        )

        if not usr:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refesh = RefreshToken.for_user(usr)

        return Response(
            {
                "access": str(refesh.access_token),
                "refresh": str(refesh),
                "user": UserSerializer(usr).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refesh_token = request.data.get("refresh")

        if not refesh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tokn = RefreshToken(refesh_token)
            tokn.blacklist()
        except Exception:
            return Response(
                {"detail": "Invalid or already blacklisted token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class MeView(APIView):
  

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

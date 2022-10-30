
# Create your views here.
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from star_studio.api.serializers import RegisterSerializer, LoginSerializer, UserSerializer, ChangePasswordSerializer, \
    DeleteUserSerializer
from star_studio.constants import INVALID_OLD_PASSWORD, UPDATED_PASSWORD_MSG, DELETED_USER
from star_studio.models import User


class RegisterView(generics.CreateAPIView):
    """
    # Register Endpoint #

    * Return user details when user register and enters required fields

    ## Payload ##
            {
                "username": "demouser2",
                "email": "demouser2@gmail.com",
                "password": "demouser2345",
                "confirm_password": "demouser2345",
                "phone": 9087654321,
            }

    ## Response ##
            {
                "user": {
                    "id": 27,
                    "username": "demouser2",
                    "email": "demouser2@gmail.com",
                    "phone_number": 9087654321
                },
                "token": "18e7cc5c43e17aa50b38bcb5b1639a37f0a99486"
            }
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'user': serializer.data, 'token': token.key})


class UserLoginView(generics.GenericAPIView):
    """
    # Login Endpoint #

    * Return token if provided credentials are valid.

    ## Payload ##
            {
                "email": "user1@gmail.com",
                "password": "user123456"
            }

    ## Response ##
            {
                "user_id": 27,
                "name": "user1",
                "email": "user1@gmail.com",
                "phone_number": "9087654321"
            }
    """
    serializer_class = LoginSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer_class = LoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            user = serializer_class.validated_data['user']
            return Response({'user_id': user.id, 'name': user.username,
                             'email': user.email, 'phone_number': user.phone_number}, status=HTTP_200_OK)
        return Response(serializer_class.data, status=HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """
    # User List Api endpoint #
    ## Response ##
            [
                {
                    "id": 1,
                    "username": "mina",
                    "email": "mina@gmail.com",
                    "password": "pbkdf2_sha256$260000$MtcMp9rorbmX7mzkiBda18$gWhstDFRHaNoYBvZVZmKXoDjwbRzOM0TXE+krKJkF6g=",
                    "phone": 9086765432
                },
                {
                    "id": 2,
                    "username": "demouser1",
                    "email": "demouser1@gmail.com",
                    "password": "pbkdf2_sha256$260000$lzxBcj62BW19HIs7KvVN0g$OKtGFhcWoqre5l9TIXJekyB57/G7epFM9d8LSz897oQ=",
                    "phone": 9086765432
                }
            ]
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChangePasswordView(UpdateAPIView):
    """
    # change password ENDPOINT #

    ## Payload ##
            {
                "old_password" : "demouser123",
                "new_password: "demouser@123"
            }

    ## Response ##
            {
                "status_code": 200,
                "message": "Password updated successfully",
                "updated_password": "demouser@123"
            }

    """
    model = User
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password of user's
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": INVALID_OLD_PASSWORD}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            updated_password = serializer.data.get('new_password')
            response = {
                'status_code': status.HTTP_200_OK,
                'message': UPDATED_PASSWORD_MSG,
                'updated_password': updated_password
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = DeleteUserSerializer

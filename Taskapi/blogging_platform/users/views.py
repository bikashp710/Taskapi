from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_tokens_for_user
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        active_tokens = OutstandingToken.objects.filter(user=user)
        for token in active_tokens:
            if not BlacklistedToken.objects.filter(token=token).exists():
                return Response(
                    {
                        'detail': 'You are already logged in from another session.',
                        'action': 'Please logout from your current session before logging in again.'
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        tokens = generate_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:

        refresh_token = request.data.get('refresh',None)
        if not refresh_token:
            return Response({'detail': 'Refresh token is required for logout.'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist() 
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': 'Invalid token or logout failed.'}, status=status.HTTP_400_BAD_REQUEST)



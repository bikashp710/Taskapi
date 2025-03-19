from rest_framework_simplejwt.tokens import RefreshToken

def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    return {
        'refresh': str(refresh),
        'access': str(access)
    }

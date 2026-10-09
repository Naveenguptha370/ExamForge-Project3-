from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User, UserActivityLog
from .serializers import UserSerializer, UserActivityLogSerializer, ChangePasswordSerializer

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            existing_user = User.objects.filter(username=username).first()
            if existing_user and existing_user.check_password(password) and not existing_user.is_active:
                return Response({'error': 'Account has been deactivated. Please contact the administrator.'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'Account has been deactivated. Please contact the administrator.'}, status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=user)

        # Log activity
        ip = request.META.get('REMOTE_ADDR')
        UserActivityLog.objects.create(
            user=user,
            action='LOGIN_SUCCESS',
            ip_address=ip,
            details={'method': 'TokenAuthentication'}
        )

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({'message': 'Successfully logged out'})


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Incorrect current password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.must_change_password = False
            user.save()
            return Response({'message': 'Password updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        role = self.request.query_params.get('role')
        search = self.request.query_params.get('search')
        is_active = self.request.query_params.get('is_active')

        if role:
            qs = qs.filter(role=role)
        if search:
            qs = qs.filter(username__icontains=search) | qs.filter(email__icontains=search) | qs.filter(first_name__icontains=search) | qs.filter(last_name__icontains=search)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        return qs


class UserActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

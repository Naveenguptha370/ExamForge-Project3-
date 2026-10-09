from django.contrib.auth import login, logout
from django.contrib.auth.password_validation import validate_password
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import AuditLog, User
from .permissions import IsAdminOrSelf
from .serializers import AuditLogSerializer, LoginSerializer, PasswordResetSerializer, UserCreateSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        source_ip = self._get_client_ip(request)
        AuditLog.objects.create(
            actor=request.user,
            action='user_created',
            model_name='User',
            object_id=str(user.pk),
            details=f'Created {user.get_full_name() or user.username}',
            ip_address=source_ip,
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        AuditLog.objects.create(
            actor=request.user,
            action='user_updated',
            model_name='User',
            object_id=str(user.pk),
            details=f'Updated {user.get_full_name() or user.username}',
            ip_address=self._get_client_ip(request),
        )
        return Response(UserSerializer(user).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def dashboard(self, request):
        users = User.objects.all()
        data = {
            'total_users': users.count(),
            'active_users': users.filter(is_active=True).count(),
            'inactive_users': users.filter(is_active=False).count(),
            'faculty_users': users.filter(role=User.Role.FACULTY).count(),
            'available_faculty': users.filter(role=User.Role.FACULTY, status=User.Status.ACTIVE).count(),
            'incomplete_profiles': users.filter(role=User.Role.FACULTY).filter(Q(first_name='') | Q(last_name='')).count(),
        }
        return Response(data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def deactivate(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id is required.'}, status=400)
        user = User.objects.get(pk=user_id)
        user.is_active = False
        user.status = User.Status.INACTIVE
        user.save(update_fields=['is_active', 'status'])
        AuditLog.objects.create(
            actor=request.user,
            action='user_deactivated',
            model_name='User',
            object_id=str(user.pk),
            details=f'Deactivated {user.get_full_name() or user.username}',
            ip_address=self._get_client_ip(request),
        )
        return Response({'detail': 'User deactivated.'})

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def reset_password(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(username=serializer.validated_data['username']).first()
        if user is None:
            return Response({'detail': 'User not found.'}, status=404)
        try:
            validate_password(serializer.validated_data['new_password'], user=user)
        except Exception as exc:
            return Response({'detail': str(exc)}, status=400)
        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        AuditLog.objects.create(
            actor=request.user,
            action='password_reset',
            model_name='User',
            object_id=str(user.pk),
            details=f'Password reset for {user.username}',
            ip_address=self._get_client_ip(request),
        )
        return Response({'detail': 'Password updated successfully.'})

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class LoginAPIView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        user.last_login_ip = self._get_client_ip(request)
        user.save(update_fields=['last_login_ip', 'last_login'])
        AuditLog.objects.create(
            actor=user,
            action='login',
            model_name='User',
            object_id=str(user.pk),
            details='Successful login',
            ip_address=user.last_login_ip,
        )
        return Response(UserSerializer(user).data)

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        AuditLog.objects.create(
            actor=request.user,
            action='logout',
            model_name='User',
            object_id=str(request.user.pk),
            details='User logged out',
            ip_address=self._get_client_ip(request),
        )
        logout(request)
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-created_at')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import User, UserActivity, UserRole
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer,
    PasswordChangeSerializer, UserActivitySerializer
)
from .permissions import IsAdminUserRole

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # Record login activity
            UserActivity.objects.create(
                user=user,
                action='USER_LOGIN',
                module='AUTH',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:250],
                details={'message': f"User {user.username} logged in successfully."}
            )

            return Response({
                'success': True,
                'message': 'Login successful.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            UserActivity.objects.create(
                user=user,
                action='USER_LOGOUT',
                module='AUTH',
                ip_address=request.META.get('REMOTE_ADDR'),
                details={'message': f"User {user.username} logged out."}
            )
        logout(request)
        return Response({'success': True, 'message': 'Logged out successfully.'})


class CurrentUserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'success': True,
            'user': UserSerializer(request.user).data
        })

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'user': serializer.data})
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'success': False, 'message': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.must_change_password = False
            user.save()
            UserActivity.objects.create(
                user=user,
                action='PASSWORD_CHANGED',
                module='AUTH',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response({'success': True, 'message': 'Password changed successfully.'})
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserRole]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        role = self.request.query_params.get('role')
        search = self.request.query_params.get('search')
        is_active = self.request.query_params.get('is_active')

        if role:
            qs = qs.filter(role=role)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if search:
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(employee_or_roll_id__icontains=search)
            )
        return qs

    def perform_create(self, serializer):
        user = serializer.save()
        UserActivity.objects.create(
            user=self.request.user,
            action='USER_CREATED',
            module='ACCOUNTS',
            details={'created_username': user.username, 'role': user.role}
        )


class UserActivityListView(views.APIView):
    permission_classes = [IsAdminUserRole]

    def get(self, request):
        activities = UserActivity.objects.all()[:100]
        serializer = UserActivitySerializer(activities, many=True)
        return Response({'success': True, 'activities': serializer.data})

from django.urls import path

from star_studio.views import RegisterView, UserLoginView, UserListView, ChangePasswordView, DeleteUserView

app_name = 'star_studio'

urlpatterns = [
        path('register/', RegisterView.as_view(), name='register'),
        path('login/', UserLoginView.as_view(), name='login'),
        path('users/list/', UserListView.as_view(), name='user_list'),
        path('change-password/', ChangePasswordView.as_view(), name='change_password'),
        path('delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
        ]
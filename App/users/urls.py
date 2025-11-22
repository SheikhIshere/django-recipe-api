"""url mapping for the user api"""
from django.urls import path
from .views import (
    CreateUserVIew,
    CreateTokenView,
    ManageUserView
)

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserVIew.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me' )
]
from django.contrib import admin
from django.db.models.query_utils import PathInfo
from django.urls import path
from .views import signupview, register_user


urlpatterns = [
        path('admin/', admin.site.urls),
        path('signup/', signupview, name='signup'),
        path('register_user/', register_user, name='register_user'),

]
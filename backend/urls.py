from django.urls import path
from .views import user_manage


app_name = 'backend'

urlpatterns = [
    path('manage_index/', user_manage.manage_index, name='manage_index'),
    path('base_info/', user_manage.base_info, name='base_info'),
]

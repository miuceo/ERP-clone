from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import (
    AdminHomeView,
)

# ADMIN router

router = DefaultRouter()
router.register('teacher_admins', AdminHomeView, basename='admin')


urlpatterns = [
    *router.urls,
]
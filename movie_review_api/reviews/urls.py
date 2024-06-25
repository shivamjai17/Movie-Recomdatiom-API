from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterAPI, LoginAPI, MovieViewSet, ReviewViewSet, recommend_movies_view
from knox import views as knox_views

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('api/auth/register/', RegisterAPI.as_view(), name='register'),
    path('api/auth/login/', LoginAPI.as_view(), name='login'),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/recommendations/', recommend_movies_view, name='recommendations'),
    path('', include(router.urls)),
]

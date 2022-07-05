from rest_framework.authtoken import views
from rest_framework import routers
from django.urls import include, path

from .views import CommentViewSet, GroupViewSet, PostViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'posts', PostViewSet)
v1_router.register(r'groups', GroupViewSet)
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='Comments'
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
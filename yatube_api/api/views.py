from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from posts.models import Comment, Group, Post, User
from posts.serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer,
    UserSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=self.kwargs.get("post_id"))
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Нельзя трогать чужой контент!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Нельзя удалять чужой контент!')
        super(CommentViewSet, self).perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Нельзя трогать чужой контент!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Нельзя удалять чужой контент!')
        super(PostViewSet, self).perform_destroy(instance)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

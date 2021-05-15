from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Follow, Group, Post, User
from .permissions import AuthorPermissions
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [AuthorPermissions, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorPermissions, IsAuthenticatedOrReadOnly]

    def get_post(self):
        post_id = int(self.kwargs.get('post_id'))
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Follow.objects.filter(following=self.request.user)
        username = self.request.query_params.get('search', None)
        if username is not None:
            user = get_object_or_404(User, username=username)
            queryset = queryset.filter(user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        username = request.data.get('following')
        if username:
            user = get_object_or_404(User, username=username)
            if user == self.request.user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.filter(following=user,
                                           user=self.request.user)
            if follow:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                data = {'following': user, 'user': self.request.user}
                serializer = FollowSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(following=user, user=self.request.user)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

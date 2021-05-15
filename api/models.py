from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    slug = models.SlugField(unique=False, default='any_group')
    title = models.CharField(verbose_name='имя группы', max_length=75)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name='Группа',
                              related_name='posts', blank=True, null=True,)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-created',)


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'user'],
                name='uniq_follow',
            )
        ]

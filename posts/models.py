from tinymce.models import HTMLField

import uuid
from django.db import models

from accounts.models import CustomUser
from posts.constants import POST_CHOICES


class CommonInfo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class PostCategory(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "PostCategory"
        verbose_name_plural = "PostCategories"

    def __str__(self):
        return self.name


class PostTag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Post(CommonInfo):
    title = models.CharField(max_length=150)
    content = HTMLField()
    author = models.ForeignKey(
        CustomUser,
        related_name="author",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=10,
        choices=POST_CHOICES,
        default="draft",
    )
    category = models.ForeignKey(
        "PostCategory",
        related_name="posts",
        on_delete=models.SET_NULL,
        null=True,
    )
    tag = models.ManyToManyField("PostTag", related_name="posts", blank=True)
    likes = models.PositiveIntegerField(default=0, blank=True)
    dislikes = models.PositiveIntegerField(default=0, blank=True)
    views = models.PositiveBigIntegerField(default=0, blank=True)
    published_on = models.DateTimeField(null=True, blank=True)
    featured_image = models.ImageField(
        upload_to="posts/featured_images/", null=True, blank=True
    )

    class Meta:
        ordering = ["-published_on"]

    def __str__(self):
        return f"Post by {self.author} - {self.title[:20]}"


class Comment(CommonInfo):
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    comment_writer = models.ForeignKey(
        CustomUser,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    comment = models.TextField()
    likes = models.PositiveIntegerField(default=0, blank=True)
    dislikes = models.PositiveIntegerField(default=0, blank=True)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.comment_writer} on {self.post.title[:20]}"


class Reply(CommonInfo):
    comment = models.ForeignKey(
        Comment, null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="child_replies",
    )
    reply_writer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    reply_content = models.TextField()
    likes = models.PositiveIntegerField(default=0, blank=True)
    dislikes = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_parent(self):
        return self.parent is None

    def __str__(self):
        return f"Reply by {self.reply_writer} on {self.comment.post.title[:20]}"

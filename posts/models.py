from tinymce.models import HTMLField

import uuid
from django.db import models

from accounts.models import CustomUser
from posts.constants import POST_CHOICES


class CommonInfo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


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
        "Category",
        related_name="posts",
        on_delete=models.SET_NULL,
    )
    tag = models.ManyToManyField("Tag", related_name="posts", blank=True)
    likes = models.PositiveIntegerField(default=0, blank=True)
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
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title[:20]}"

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
    views = models.PositiveBigIntegerField(default=0, blank=True)
    published_on = models.DateTimeField(null=True, blank=True)
    featured_image = models.ImageField(
        upload_to="posts/featured_images/", null=True, blank=True
    )

    class Meta:
        ordering = ["-published_on"]

    def __str__(self):
        return f"Post by {self.author} - {self.title[:20]}"

    @property
    def like_count(self):
        return self.postlikes.count()

    @property
    def dislike_count(self):
        return self.postdislikes.count()


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
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.comment_writer} on {self.post.title[:20]}"

    @property
    def like_count(self):
        return self.commentlikes.count()

    @property
    def dislike_count(self):
        return self.commentdislikes.count()


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

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Reply"
        verbose_name_plural = "Replies"

    def __str__(self):
        if self.comment:
            return f"Reply by {self.reply_writer} on {self.comment.post.title[:20]}"
        return f"Reply by {self.reply_writer} on {self.parent.reply_writer}'s comment"

    @property
    def like_count(self):
        return self.replylikes.count()

    @property
    def dislike_count(self):
        return self.replydislikes.count()


class LikeDislikeCommonInfo(CommonInfo):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        action = self.get_action()
        related_obj = self.get_related_object()
        return f"{action} by {self.user} on {related_obj}"

    def get_related_object(self):
        raise NotImplementedError("Subclasses must implement `get_related_object`.")

    def get_action(self):
        raise NotImplementedError("Subclasses must implement `get_action`.")


class PostLikes(LikeDislikeCommonInfo):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postlikes")

    class Meta:
        unique_together = ["post", "user"]
        verbose_name = "Post like"
        verbose_name_plural = "Post likes"

    def get_related_object(self):
        return self.post.title[:20]

    def get_action(self):
        return "Like"


class PostDislikes(LikeDislikeCommonInfo):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="postdislikes"
    )

    class Meta:
        unique_together = ["post", "user"]
        verbose_name = "Post dislike"
        verbose_name_plural = "Post dislikes"

    def get_related_object(self):
        return self.post.title[:20]

    def get_action(self):
        return "Dislike"


class CommentLikes(LikeDislikeCommonInfo):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="commentlikes"
    )

    class Meta:
        unique_together = ["comment", "user"]
        verbose_name = "Comment like"
        verbose_name_plural = "Comment likes"

    def get_related_object(self):
        return self.comment.post.title[:20]

    def get_action(self):
        return "Like"


class CommentDislikes(LikeDislikeCommonInfo):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="commentdislikes"
    )

    class Meta:
        unique_together = ["comment", "user"]
        verbose_name = "Comment dislike"
        verbose_name_plural = "Comment dislikes"

    def get_related_object(self):
        return self.comment.post.title[:20]

    def get_action(self):
        return "Dislike"


class ReplyLikes(LikeDislikeCommonInfo):
    reply = models.ForeignKey(
        Reply, on_delete=models.CASCADE, related_name="replylikes"
    )

    class Meta:
        unique_together = ["reply", "user"]
        verbose_name = "Reply like"
        verbose_name_plural = "Reply likes"

    def get_related_object(self):
        return self.reply.comment.post.title[:20]

    def get_action(self):
        return "Like"


class ReplyDislikes(LikeDislikeCommonInfo):
    reply = models.ForeignKey(
        Reply, on_delete=models.CASCADE, related_name="replydislikes"
    )

    class Meta:
        unique_together = ["reply", "user"]
        verbose_name = "Reply dislike"
        verbose_name_plural = "Reply dislikes"

    def get_related_object(self):
        return self.reply.comment.post.title[:20]

    def get_action(self):
        return "Dislike"

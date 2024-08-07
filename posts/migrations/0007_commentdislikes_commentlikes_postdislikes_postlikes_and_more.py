# Generated by Django 4.2.3 on 2024-08-08 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_replylikedislike_postlikedislike_commentlikedislike'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentDislikes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommentLikes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostDislikes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostLikes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyDislikes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyLikes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='postlikedislike',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='postlikedislike',
            name='post',
        ),
        migrations.RemoveField(
            model_name='postlikedislike',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='replylikedislike',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='replylikedislike',
            name='reply',
        ),
        migrations.RemoveField(
            model_name='replylikedislike',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='likes',
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='CommentLikeDislike',
        ),
        migrations.DeleteModel(
            name='PostLikeDislike',
        ),
        migrations.DeleteModel(
            name='ReplyLikeDislike',
        ),
        migrations.AddField(
            model_name='replylikes',
            name='reply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replylikes', to='posts.reply'),
        ),
        migrations.AddField(
            model_name='replylikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='replydislikes',
            name='reply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replydislikes', to='posts.reply'),
        ),
        migrations.AddField(
            model_name='replydislikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postlikes',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postlikes', to='posts.post'),
        ),
        migrations.AddField(
            model_name='postlikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postdislikes',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postdislikes', to='posts.post'),
        ),
        migrations.AddField(
            model_name='postdislikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentlikes',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentlikes', to='posts.comment'),
        ),
        migrations.AddField(
            model_name='commentlikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentdislikes',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentdislikes', to='posts.comment'),
        ),
        migrations.AddField(
            model_name='commentdislikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='replylikes',
            unique_together={('reply', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='replydislikes',
            unique_together={('reply', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='postlikes',
            unique_together={('post', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='postdislikes',
            unique_together={('post', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='commentlikes',
            unique_together={('comment', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='commentdislikes',
            unique_together={('comment', 'user')},
        ),
    ]

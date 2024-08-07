# Generated by Django 4.2.3 on 2024-07-19 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'PostCategory',
                'verbose_name_plural': 'PostCategories',
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=150)),
                ('content', tinymce.models.HTMLField()),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published')], default='draft', max_length=10)),
                ('likes', models.PositiveIntegerField(blank=True, default=0)),
                ('views', models.PositiveBigIntegerField(blank=True, default=0)),
                ('published_on', models.DateTimeField(blank=True, null=True)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='posts/featured_images/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='posts.postcategory')),
                ('tag', models.ManyToManyField(blank=True, related_name='posts', to='posts.posttag')),
            ],
            options={
                'ordering': ['-published_on'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('comment', models.TextField()),
                ('comment_writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='posts.comment')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]

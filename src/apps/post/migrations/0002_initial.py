# Generated by Django 4.2.2 on 2023-06-22 11:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by_user_id', related_query_name='%(app_label)s_%(class)s_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='post',
            name='modifier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated_by_user_id', related_query_name='%(app_label)s_%(class)s_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modifier'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by_user_id', related_query_name='%(app_label)s_%(class)s_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='comment',
            name='modifier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_updated_by_user_id', related_query_name='%(app_label)s_%(class)s_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modifier'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['api_post_id', 'title'], name='post_post_api_pos_f3e4a4_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['api_comment_id', 'post'],
                               name='post_commen_api_com_32abb2_idx'),
        ),
    ]
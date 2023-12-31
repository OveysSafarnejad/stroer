# Generated by Django 4.2.2 on 2023-06-22 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True,
                                                      verbose_name='Create time')),
                ('modified_time', models.DateTimeField(auto_now=True,
                                                       verbose_name='Modify time')),
                ('api_comment_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True,
                                                      verbose_name='Create time')),
                ('modified_time', models.DateTimeField(auto_now=True,
                                                       verbose_name='Modify time')),
                ('api_post_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-28 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('member', 'member'), ('moderator', 'moderator')], max_length=9, null=True),
        ),
    ]
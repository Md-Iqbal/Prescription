# Generated by Django 3.1.3 on 2020-12-06 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20201206_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='follower',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.IntegerField(default=0),
        ),
    ]

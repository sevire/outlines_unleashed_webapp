# Generated by Django 3.0 on 2020-02-16 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ou_app', '0003_auto_20200215_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datanodedescriptor',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
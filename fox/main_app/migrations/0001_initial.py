# Generated by Django 4.1.1 on 2022-09-13 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('discription', models.TextField(max_length=500)),
                ('price', models.FloatField(default=0)),
            ],
        ),
    ]

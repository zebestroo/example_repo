# Generated by Django 4.1.1 on 2022-09-17 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data_json', models.JSONField(default={'item_ids': []})),
                ('total_scale', models.FloatField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='item',
            old_name='discription',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
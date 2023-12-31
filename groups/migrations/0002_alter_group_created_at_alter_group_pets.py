# Generated by Django 4.2.5 on 2023-10-03 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='pets',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='group', to='pets.pet'),
        ),
    ]

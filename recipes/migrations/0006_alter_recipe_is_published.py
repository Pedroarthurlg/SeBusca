# Generated by Django 4.0 on 2022-09-20 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipe_options_alter_recipe_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]

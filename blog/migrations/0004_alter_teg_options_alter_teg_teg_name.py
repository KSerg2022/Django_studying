# Generated by Django 4.1.4 on 2022-12-25 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_teg_post_teg'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teg',
            options={'ordering': ('teg_name',)},
        ),
        migrations.AlterField(
            model_name='teg',
            name='teg_name',
            field=models.CharField(help_text='format - #*** some word.', max_length=10, unique=True, verbose_name='Теги'),
        ),
    ]
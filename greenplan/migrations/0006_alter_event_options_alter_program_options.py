# Generated by Django 5.0.6 on 2024-10-11 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greenplan', '0005_alter_event_options_alter_program_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_datetime', '-updated_at', 'title'], 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='program',
            options={'ordering': ['title'], 'verbose_name': 'Program', 'verbose_name_plural': 'Programs'},
        ),
    ]
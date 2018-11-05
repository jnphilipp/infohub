# Generated by Django 2.1.2 on 2018-10-17 14:47

from django.db import migrations, models
import django.db.models.deletion
import django_fsm
import infohub.fields


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('slug', models.SlugField(max_length=4096, unique=True, verbose_name='Slug')),
                ('url', models.URLField(max_length=2096, unique=True, verbose_name='URL')),
                ('title', infohub.fields.SingleLineTextField(blank=True, null=True, verbose_name='Title')),
                ('state', django_fsm.FSMField(default='alive', max_length=50, verbose_name='State')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feeds', to='feeds.Type', verbose_name='Type')),
            ],
            options={
                'ordering': ('state', 'url'),
                'verbose_name': 'Feed',
                'verbose_name_plural': 'Feeds',
            },
        ),
    ]
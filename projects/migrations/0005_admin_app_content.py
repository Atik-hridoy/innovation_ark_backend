from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('projects', '0004_sitesettings')]

    operations = [
        migrations.AddField(model_name='project', name='problem', field=models.TextField(blank=True, null=True)),
        migrations.AddField(model_name='project', name='solution', field=models.TextField(blank=True, null=True)),
        migrations.AddField(model_name='project', name='impact', field=models.TextField(blank=True, null=True)),
        migrations.AddField(model_name='project', name='sort_order', field=models.PositiveIntegerField(default=0)),
        migrations.AddField(model_name='project', name='is_published', field=models.BooleanField(default=True)),
        migrations.AddField(model_name='contactmessage', name='is_read', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='sitesettings', name='office_address', field=models.CharField(blank=True, max_length=500, null=True)),
        migrations.AddField(model_name='sitesettings', name='map_url', field=models.URLField(blank=True, max_length=1000, null=True)),
        migrations.CreateModel(
            name='BookingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)), ('email', models.EmailField(max_length=254)),
                ('project_type', models.CharField(max_length=255)), ('preferred_date', models.DateField()),
                ('preferred_time', models.CharField(max_length=50)), ('timezone', models.CharField(default='Asia/Dhaka', max_length=100)),
                ('brief', models.TextField(blank=True, default='')), ('status', models.CharField(choices=[('new','New'),('confirmed','Confirmed'),('completed','Completed'),('cancelled','Cancelled')], default='new', max_length=20)),
                ('internal_note', models.TextField(blank=True, default='')), ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ContentBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField(max_length=120, unique=True)), ('label', models.CharField(max_length=255)),
                ('value', models.JSONField(blank=True, default=dict)), ('is_published', models.BooleanField(default=True)), ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['key']},
        ),
    ]

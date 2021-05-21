# Generated by Django 3.1.3 on 2021-05-18 06:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=746, multiple=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapGoogleDataLinkData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_id', models.IntegerField()),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'permissions': (('give_refund', 'Can refund customers'), ('can_hire', 'Can hire employees')),
                'default_permissions': ('add',),
            },
        ),
        migrations.CreateModel(
            name='ScrapJsonData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('images', models.TextField(blank=True, null=True)),
                ('source', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('born', models.TextField(blank=True, null=True)),
                ('height', models.TextField(blank=True, null=True)),
                ('books', models.TextField(blank=True, null=True)),
                ('education', models.TextField(blank=True, null=True)),
                ('children', models.TextField(blank=True, null=True)),
                ('known_attributes', models.TextField(blank=True, null=True)),
                ('profiles', models.TextField(blank=True, null=True)),
                ('people_also_search_for', models.TextField(blank=True, null=True)),
                ('related_searches', models.TextField(blank=True, null=True)),
                ('related_questions', models.TextField(blank=True, null=True)),
                ('organic_results', models.TextField(blank=True, null=True)),
                ('pagination', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapWeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'permissions': (('give_refund', 'Can refund customers'), ('can_hire', 'Can hire employees')),
                'default_permissions': ('add',),
            },
        ),
        migrations.CreateModel(
            name='Semrush',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('keyword', models.CharField(blank=True, max_length=255, null=True)),
                ('seed_keyword', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('keyword_difficulty', models.CharField(blank=True, max_length=255, null=True)),
                ('ccp', models.CharField(blank=True, max_length=255, null=True)),
                ('competitive_density', models.CharField(blank=True, max_length=255, null=True)),
                ('number_of_results', models.CharField(blank=True, max_length=255, null=True)),
                ('serp_Features', models.TextField(blank=True, null=True)),
                ('trend', models.CharField(blank=True, max_length=255, null=True)),
                ('click_potential', models.CharField(blank=True, max_length=255, null=True)),
                ('competitors', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('skill', models.CharField(max_length=255)),
                ('location', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadGoogleDataLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('links', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('keyword_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.semrush')),
            ],
            options={
                'permissions': (('give_refund', 'Can refund customers'), ('can_hire', 'Can hire employees')),
                'default_permissions': ('add',),
            },
        ),
    ]

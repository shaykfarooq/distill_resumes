# Generated by Django 5.1.6 on 2025-02-25 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_resume_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='candidate_name',
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='certifications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='education_history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='minified_context',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='personal_information',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='projects',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='skills',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='work_experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]

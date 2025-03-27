# Generated by Django 5.1.7 on 2025-03-27 07:42

import reviews.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_review_rating_assignment_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='file',
            field=models.FileField(upload_to=reviews.models.assignment_upload_path),
        ),
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.FileField(upload_to=reviews.models.submission_upload_path),
        ),
    ]

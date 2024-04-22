# Generated by Django 5.0.4 on 2024-04-21 21:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplicantModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                ("email", models.CharField(max_length=100)),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Pending"), (1, "Approved"), (2, "Rejected")],
                        default=0,
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("can_add_applicant", "Can create an applicant"),
                    ("can_view_applicant", "Can view an applicant"),
                    ("can_change_applicant_status", "Can approve or reject applicants"),
                    ("can_add_applicant_note", "Can add notes to applicants"),
                ],
            },
        ),
        migrations.CreateModel(
            name="ApplicantNoteModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note", models.TextField()),
                ("created", models.DateTimeField()),
                (
                    "applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="applicants.applicantmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

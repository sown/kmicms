# Generated by Django 4.2.7 on 2023-11-22 18:00

import django.db.models.deletion
import modelcluster.fields
import wagtail.search.index
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DegreeSubject",
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
                (
                    "name",
                    models.CharField(
                        help_text="Degree subject or area of study", max_length=40,
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="DegreeType",
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
                (
                    "name",
                    models.CharField(
                        help_text="Degree type or level of study", max_length=40,
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Person",
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
                (
                    "name",
                    models.CharField(
                        help_text="The real name of the person. Only displayed to logged-in users if public name is set.",  # noqa: E501
                        max_length=120,
                        unique=True,
                    ),
                ),
                (
                    "nickname",
                    models.CharField(
                        blank=True,
                        help_text="A publicly displayed name for the person, if they do not wish for their real name to be published publicly.",  # noqa: E501
                        max_length=120,
                    ),
                ),
                (
                    "irc_nick",
                    models.CharField(
                        blank=True,
                        help_text="IRC nick, if applicable. Useful for identifying past members.",
                        max_length=60,
                        verbose_name="IRC Nick",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("alumni", "Alumni"),
                            ("guest", "Guest"),
                            ("staff", "Staff"),
                            ("student", "Student"),
                        ],
                        max_length=7,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is active?"),
                ),
                (
                    "radio_licence",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("full", "Full"),
                            ("inte", "Intermediate"),
                            ("fdtn", "Foundation"),
                        ],
                        max_length=4,
                    ),
                ),
                ("is_radio_instructor", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "people",
                "ordering": ("name",),
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name="RadioCallsign",
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
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("callsign", models.CharField(max_length=10)),
                (
                    "owner",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="callsigns",
                        related_query_name="callsigns",
                        to="people.person",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DegreeCourse",
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
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "graduation_year",
                    models.CharField(
                        blank=True,
                        help_text="Year of graduation, approx if not known.",
                        max_length=20,
                        verbose_name="Graduation Year",
                    ),
                ),
                (
                    "degree_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="degree_courses",
                        related_query_name="degree_courses",
                        to="people.degreetype",
                    ),
                ),
                (
                    "person",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="degree_courses",
                        related_query_name="degree_courses",
                        to="people.person",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="degree_courses",
                        related_query_name="degree_courses",
                        to="people.degreesubject",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
        migrations.AddConstraint(
            model_name="radiocallsign",
            constraint=models.UniqueConstraint(
                models.F("callsign"),
                name="unique_callsign",
                violation_error_message="That callsign is already assigned to another person.",
            ),
        ),
    ]

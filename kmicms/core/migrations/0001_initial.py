# Generated by Django 4.2.7 on 2023-11-22 21:43

import django.core.validators
import django.db.models.deletion
import modelcluster.fields
import taggit.managers
import wagtail.blocks
import wagtail.fields
import wagtail.images.models
import wagtail.models.collections
import wagtail.search.index
from django.conf import settings
from django.db import migrations, models

import core.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomImage",
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
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "file",
                    wagtail.images.models.WagtailImageField(
                        height_field="height",
                        upload_to=wagtail.images.models.get_upload_to,
                        verbose_name="file",
                        width_field="width",
                    ),
                ),
                ("width", models.IntegerField(editable=False, verbose_name="width")),
                ("height", models.IntegerField(editable=False, verbose_name="height")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="created at",
                    ),
                ),
                ("focal_point_x", models.PositiveIntegerField(blank=True, null=True)),
                ("focal_point_y", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "focal_point_width",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "focal_point_height",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("file_size", models.PositiveIntegerField(editable=False, null=True)),
                (
                    "file_hash",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        max_length=40,
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        default=wagtail.models.collections.get_root_collection_id,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.collection",
                        verbose_name="collection",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text=None,
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="tags",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uploaded by user",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail.images.models.ImageFileMixin,
                wagtail.search.index.Indexed,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="SiteSettings",
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
                    "title",
                    models.CharField(
                        blank=True,
                        help_text="This is used in the footer",
                        max_length=63,
                    ),
                ),
                (
                    "brand",
                    models.CharField(
                        choices=[("sown", "SOWN"), ("suws", "SUWS")],
                        default="sown",
                        max_length=15,
                    ),
                ),
                (
                    "copyright_start_year",
                    models.PositiveIntegerField(
                        default=core.utils.last_year,
                        help_text="The initial year of copyright for the site.",
                        validators=[
                            django.core.validators.MinValueValidator(1950),
                            core.utils.max_value_current_year,
                        ],
                    ),
                ),
                (
                    "main_menu",
                    wagtail.fields.StreamField(
                        [
                            (
                                "page_link",
                                wagtail.blocks.StructBlock(
                                    [("page", wagtail.blocks.PageChooserBlock())],
                                ),
                            ),
                            (
                                "external_link",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "label",
                                            wagtail.blocks.CharBlock(
                                                label="Label",
                                                max_length=55,
                                            ),
                                        ),
                                        ("url", wagtail.blocks.URLBlock(label="URL")),
                                    ],
                                ),
                            ),
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
                (
                    "footer_menu",
                    wagtail.fields.StreamField(
                        [
                            (
                                "page_link",
                                wagtail.blocks.StructBlock(
                                    [("page", wagtail.blocks.PageChooserBlock())],
                                ),
                            ),
                            (
                                "external_link",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "label",
                                            wagtail.blocks.CharBlock(
                                                label="Label",
                                                max_length=55,
                                            ),
                                        ),
                                        ("url", wagtail.blocks.URLBlock(label="URL")),
                                    ],
                                ),
                            ),
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.site",
                    ),
                ),
            ],
            options={
                "verbose_name": "Site Settings",
            },
        ),
        migrations.CreateModel(
            name="SocialMediaAccount",
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
                    "service",
                    models.CharField(
                        choices=[
                            ("discord", "Discord"),
                            ("facebook", "Facebook"),
                            ("github", "GitHub"),
                            ("mastodon", "Mastodon"),
                            ("snapchat", "Snapchat"),
                            ("twitter", "Twitter / X"),
                            ("whatsapp", "WhatsApp"),
                            ("youtube", "YouTube"),
                        ],
                        max_length=20,
                    ),
                ),
                ("url", models.URLField()),
                (
                    "site_settings",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="social_media_accounts",
                        to="core.sitesettings",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomRendition",
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
                ("filter_spec", models.CharField(db_index=True, max_length=255)),
                (
                    "file",
                    wagtail.images.models.WagtailImageField(
                        height_field="height",
                        storage=wagtail.images.models.get_rendition_storage,
                        upload_to=wagtail.images.models.get_rendition_upload_to,
                        width_field="width",
                    ),
                ),
                ("width", models.IntegerField(editable=False)),
                ("height", models.IntegerField(editable=False)),
                (
                    "focal_point_key",
                    models.CharField(
                        blank=True,
                        default="",
                        editable=False,
                        max_length=16,
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="renditions",
                        to="core.customimage",
                    ),
                ),
            ],
            options={
                "unique_together": {("image", "filter_spec", "focal_point_key")},
            },
            bases=(wagtail.images.models.ImageFileMixin, models.Model),
        ),
    ]
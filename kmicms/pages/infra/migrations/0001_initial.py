# Generated by Django 4.2.7 on 2023-12-27 21:44

import django.db.models.deletion
import wagtail.contrib.routable_page.models
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
    ]

    operations = [
        migrations.CreateModel(
            name="NetboxInfrastructurePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("introduction", wagtail.fields.RichTextField()),
                ("device_description", wagtail.fields.RichTextField()),
                ("vm_description", wagtail.fields.RichTextField()),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail.contrib.routable_page.models.RoutablePageMixin,
                "wagtailcore.page",
            ),
        ),
    ]
# Generated by Django 4.2.8 on 2024-01-15 19:28

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("standard_page", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="standardpage",
            name="content",
            field=wagtail.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "size",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("h2", "Heading 2"),
                                            ("h3", "Heading 3"),
                                            ("h4", "Heading 4"),
                                        ]
                                    ),
                                ),
                                ("text", wagtail.blocks.TextBlock()),
                            ]
                        ),
                    ),
                    (
                        "rich_text",
                        wagtail.blocks.RichTextBlock(editor="all-but-headings"),
                    ),
                    (
                        "alert",
                        wagtail.blocks.StructBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(required=False)),
                                (
                                    "alert_type",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("primary", "Primary"),
                                            ("secondary", "Secondary"),
                                            ("success", "Success"),
                                            ("danger", "Danger"),
                                            ("warning", "Warning"),
                                            ("info", "Info"),
                                            ("light", "Light"),
                                            ("dark", "Dark"),
                                        ]
                                    ),
                                ),
                                ("content", wagtail.blocks.TextBlock()),
                            ]
                        ),
                    ),
                    (
                        "card_grid",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "grid_class",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("row-cols-md-2", "2 Cards Wide"),
                                            ("row-cols-md-3", "3 Cards Wide"),
                                            ("row-cols-md-4", "4 Cards Wide"),
                                        ],
                                        label="Grid Type",
                                    ),
                                ),
                                (
                                    "card_list",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(),
                                                ),
                                                ("title", wagtail.blocks.TextBlock()),
                                                (
                                                    "text",
                                                    wagtail.blocks.RichTextBlock(),
                                                ),
                                                (
                                                    "cta_list",
                                                    wagtail.blocks.ListBlock(
                                                        wagtail.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "label",
                                                                    wagtail.blocks.CharBlock(),
                                                                ),
                                                                (
                                                                    "style",
                                                                    wagtail.blocks.ChoiceBlock(
                                                                        choices=[
                                                                            (
                                                                                "primary",
                                                                                "Primary",
                                                                            ),
                                                                            (
                                                                                "secondary",
                                                                                "Secondary",
                                                                            ),
                                                                            (
                                                                                "success",
                                                                                "Success",
                                                                            ),
                                                                            (
                                                                                "danger",
                                                                                "Danger",
                                                                            ),
                                                                            (
                                                                                "warning",
                                                                                "Warning",
                                                                            ),
                                                                            (
                                                                                "info",
                                                                                "Info",
                                                                            ),
                                                                            (
                                                                                "light",
                                                                                "Light",
                                                                            ),
                                                                            (
                                                                                "dark",
                                                                                "Dark",
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ),
                                                                (
                                                                    "link",
                                                                    wagtail.blocks.PageChooserBlock(
                                                                        label="Internal Link",
                                                                        required=False,
                                                                    ),
                                                                ),
                                                                (
                                                                    "external_link",
                                                                    wagtail.blocks.URLBlock(
                                                                        label="External Link",
                                                                        required=False,
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                        label="Calls to Action",
                                                    ),
                                                ),
                                            ]
                                        ),
                                        label="Cards",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "code",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "language",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("bash", "Bash/Shell"),
                                            ("css", "CSS"),
                                            ("diff", "diff"),
                                            ("html", "HTML"),
                                            ("javascript", "Javascript"),
                                            ("json", "JSON"),
                                            ("python", "Python"),
                                            ("scss", "SCSS"),
                                            ("yaml", "YAML"),
                                        ],
                                        help_text="Coding language",
                                        identifier="language",
                                        label="Language",
                                    ),
                                ),
                                (
                                    "code",
                                    wagtail.blocks.TextBlock(identifier="code", label="Code"),
                                ),
                            ]
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
    ]
from wagtail import blocks


class HeadingBlock(blocks.StructBlock):
    size = blocks.ChoiceBlock([("h2", "Heading 2"), ("h3", "Heading 3"), ("h4", "Heading 4")])
    text = blocks.TextBlock()

    class Meta:
        icon = "title"
        template = "core/blocks/elements/heading.html"


class AlertBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    alert_type = blocks.ChoiceBlock(
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
    )
    content = blocks.TextBlock()

    class Meta:
        template = "core/blocks/elements/alert.html"


class CallToActionBlock(blocks.StructBlock):
    label = blocks.CharBlock()
    link = blocks.PageChooserBlock()
    style = blocks.ChoiceBlock(
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
    )

    class Meta:
        template = "core/blocks/elements/call-to-action.html"

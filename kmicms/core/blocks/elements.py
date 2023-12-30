from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


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


class CardBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.TextBlock()
    text = blocks.RichTextBlock()
    cta_list = blocks.ListBlock(CallToActionBlock(), label="Calls to Action")

    class Meta:
        label = "Card"
        template = "core/blocks/elements/card.html"


class CardGridBlock(blocks.StructBlock):
    grid_class = blocks.ChoiceBlock(
        [("row-cols-md-2", "2 Cards Wide"), ("row-cols-md-3", "3 Cards Wide"), ("row-cols-md-4", "4 Cards Wide")],
        label="Grid Type",
    )
    card_list = blocks.ListBlock(CardBlock(), label="Cards")

    class Meta:
        label = "Card Grid"
        template = "core/blocks/elements/card-grid.html"

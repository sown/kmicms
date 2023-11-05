from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class MastheadBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text="An image with dimensions 1900x1216 works best")
    content = blocks.RichTextBlock()

    class Meta:
        icon = "doc-empty-inverse"
        template = "blocks/masthead.html"


class ShowcaseBlock(blocks.StructBlock):
    direction = blocks.ChoiceBlock([('left', 'Image on Left'), ('right', 'Image on Right')])
    image = ImageChooserBlock()
    title = blocks.TextBlock()
    description = blocks.TextBlock()

    class Meta:
        template = "blocks/showcase.html"


class HomePageBlock(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock(template="blocks/rich_text.html")
    masthead = MastheadBlock()
    showcase = ShowcaseBlock()

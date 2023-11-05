from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class MastheadBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text="An image with dimensions 1900x1216 works best")
    content = blocks.RichTextBlock()

    class Meta:
        icon = "doc-empty-inverse"
        template = "components/masthead.html"


class HomePageBlock(blocks.StreamBlock):
    masthead = MastheadBlock()

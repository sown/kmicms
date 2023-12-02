from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from .elements import CallToActionBlock


class MastheadBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text="An image with dimensions 1900x1216 works best")
    content = blocks.RichTextBlock()
    cta_list = blocks.ListBlock(CallToActionBlock(), max_num=3, label="Call to Action buttons")

    class Meta:
        icon = "doc-empty-inverse"
        template = "core/blocks/components/masthead.html"


class ShowcaseBlock(blocks.StructBlock):
    direction = blocks.ChoiceBlock([("left", "Image on Left"), ("right", "Image on Right")])
    image = ImageChooserBlock()
    title = blocks.TextBlock()
    description = blocks.TextBlock()
    cta_list = blocks.ListBlock(CallToActionBlock(), max_num=3, label="Call to Action buttons")

    class Meta:
        template = "core/blocks/components/showcase.html"

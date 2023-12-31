from wagtail import blocks
from wagtailcodeblock.blocks import CodeBlock

from .components import MastheadBlock, ShowcaseBlock
from .elements import AlertBlock, CardGridBlock, HeadingBlock


class StoryBlock(blocks.StreamBlock):
    heading = HeadingBlock()
    rich_text = blocks.RichTextBlock(editor="all-but-headings")
    alert = AlertBlock()
    card_grid = CardGridBlock()
    code = CodeBlock()


class ContainerBlock(blocks.StructBlock):
    content = StoryBlock()

    class Meta:
        label = "Container"
        template = "core/blocks/layout/container.html"


class TwoColumnBlock(blocks.StructBlock):
    left_content = StoryBlock()
    right_content = StoryBlock()

    class Meta:
        label = "Columns - Two"
        template = "core/blocks/layout/columns-6-6.html"


class BodyBlock(blocks.StreamBlock):
    masthead = MastheadBlock()
    showcase = ShowcaseBlock()
    container = ContainerBlock()
    columns_two = TwoColumnBlock()

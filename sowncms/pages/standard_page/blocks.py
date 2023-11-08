from wagtail import blocks


class HeadingBlock(blocks.StructBlock):

    size = blocks.ChoiceBlock([("h1", "Heading 1"), ("h2", "Heading 2"), ("h3", "Heading 3"), ("h4", "Heading 4")])
    text = blocks.TextBlock()

    class Meta:
        icon = "title"
        template = "blocks/heading.html"


class ContentBlock(blocks.StreamBlock):

    heading = HeadingBlock()
    rich_text = blocks.RichTextBlock(editor='all-but-headings')
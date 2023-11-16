from wagtail import blocks


class ExternalNavLinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(label="Label", max_length=55)
    url = blocks.URLBlock(label="URL")

    class Meta:
        label = "External Link"
        icon = "link-external"


class InternalPageBlock(blocks.StructBlock):

    page = blocks.PageChooserBlock()

    class Meta:
        label = "Page"
        icon = "link"


class MainMenuBlock(blocks.StreamBlock):

    page_link = InternalPageBlock()
    external_link = ExternalNavLinkBlock()

    class Meta:
        icon = "bars"
        label = "Main Menu"


class FooterMenuBlock(blocks.StreamBlock):

    page_link = InternalPageBlock()
    external_link = ExternalNavLinkBlock()

    class Meta:
        icon = "bars"
        label = "Footer"

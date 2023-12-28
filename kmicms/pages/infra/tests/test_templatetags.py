from pages.infra.templatetags.infra_tags import format_dns


class TestFormatDNSTemplateFilter:
    def test_fqdn(self) -> None:
        assert format_dns("www.google.com") == "www.google.com"

    def test_not_fully_qualified(self) -> None:
        assert format_dns("gw-b100") == "gw-b100.sown.org.uk"

    def test_not_fully_qualified_custom_domain(self) -> None:
        assert format_dns("gw-b100", "suws.org.uk") == "gw-b100.suws.org.uk"

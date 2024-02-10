from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from wagtail.contrib.forms.forms import FormBuilder


class ContactFormBuilder(FormBuilder):
    CAPTCHA_FIELD_NAME = "captcha"

    @property
    def formfields(self) -> dict:
        # Add wagtailcaptcha to formfields property
        fields = super().formfields
        fields[self.CAPTCHA_FIELD_NAME] = ReCaptchaField(widget=ReCaptchaV3)

        return fields


def remove_captcha_field(form: forms.Form) -> None:
    if form.is_valid():
        form.fields.pop(ContactFormBuilder.CAPTCHA_FIELD_NAME, None)
        form.cleaned_data.pop(ContactFormBuilder.CAPTCHA_FIELD_NAME, None)

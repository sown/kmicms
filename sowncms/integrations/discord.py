import requests
from wagtail.contrib.forms.models import FormSubmission


def submit_discord_webhook_for_form(webhook: str, content: str, form_submission: FormSubmission) -> None:

    fields = {
        field.clean_name: field.label
        for field in form_submission.page.form_fields.all()
    }

    payload = {
        "content": content,
        "embeds": [
            {
                "title": "Form Data",
                "fields": [
                    {"name": fields.get(key, key), "value": str(value), "inline": True}
                    for key, value in form_submission.get_data().items()
                ]
            },
        ],
    }

    resp = requests.post(webhook, json=payload)
    resp.raise_for_status()
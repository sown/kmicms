from django.core.exceptions import ValidationError
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable
from wagtail.search import index


class Person(index.Indexed, ClusterableModel):
    class PersonStatus(models.TextChoices):
        ALUMNI = "alumni", "Alumni"
        GUEST = "guest", "Guest"
        STAFF = "staff", "Staff"
        STUDENT = "student", "Student"

    class RadioLicence(models.TextChoices):
        FULL = "full", "Full"
        INTERMEDIATE = "inte", "Intermediate"
        FOUNDATION = "fdtn", "Foundation"

    # Identifying Info
    name = models.CharField(
        max_length=120,
        unique=True,
        help_text="The real name of the person. Only displayed to logged-in users if public name is set.",
    )
    nickname = models.CharField(
        max_length=120,
        blank=True,
        help_text="A publicly displayed name for the person, if they do not wish for their real name to be published publicly.",  # noqa: E501
    )
    irc_nick = models.CharField(
        verbose_name="IRC Nick",
        max_length=60,
        blank=True,
        help_text="IRC nick, if applicable. Useful for identifying past members.",
    )

    # Membership Info
    status = models.CharField(max_length=7, choices=PersonStatus.choices)
    is_active = models.BooleanField("Is active?", default=True)

    # HAM Radio
    radio_licence = models.CharField(
        max_length=4, blank=True, choices=RadioLicence.choices,
    )
    is_radio_instructor = models.BooleanField(default=False)

    search_fields = [
        index.AutocompleteField("name"),
        index.AutocompleteField("nickname"),
        index.AutocompleteField("irc_nick"),
        index.FilterField("status"),
        index.FilterField("is_active"),
        index.FilterField("radio_licence"),
        index.RelatedFields(
            "callsigns",
            [
                index.AutocompleteField("callsign"),
            ],
        ),
    ]

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "people"

    def __str__(self) -> str:
        if self.nickname:
            return f"{self.name} ({self.nickname})"
        return self.name


class RadioCallsign(Orderable, models.Model):
    owner = ParentalKey(
        Person, related_name="callsigns", related_query_name="callsigns",
    )
    callsign = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "callsign",
                name="unique_callsign",
                violation_error_message="That callsign is already assigned to another person.",
            ),
        ]

    def __str__(self) -> str:
        return self.callsign

    def clean(self) -> None:
        self.callsign = self.callsign.upper().strip()


class DegreeSubject(models.Model):
    name = models.CharField(max_length=40, help_text="Degree subject or area of study")

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class DegreeType(models.Model):
    name = models.CharField(max_length=40, help_text="Degree type or level of study")

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class DegreeCourse(Orderable, ClusterableModel):
    person = ParentalKey(
        Person, related_name="degree_courses", related_query_name="degree_courses",
    )
    subject = models.ForeignKey(
        DegreeSubject,
        blank=True,
        null=True,
        related_name="degree_courses",
        related_query_name="degree_courses",
        on_delete=models.PROTECT,
    )
    degree_type = models.ForeignKey(
        DegreeType,
        blank=True,
        null=True,
        related_name="degree_courses",
        related_query_name="degree_courses",
        on_delete=models.PROTECT,
    )
    graduation_year = models.CharField(
        "Graduation Year",
        blank=True,
        max_length=20,
        help_text="Year of graduation, approx if not known.",
    )

    def clean(self) -> None:
        if not any((self.subject, self.degree_type, self.graduation_year)):
            raise ValidationError(
                "Please provide at least one of subject, degree level or course.",
            )

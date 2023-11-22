import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandParser

from people.models import DegreeCourse, DegreeSubject, DegreeType, Person, RadioCallsign


class Command(BaseCommand):
    help = "Import teams and pit locations from SRComp"  # noqa: A003

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--file", type=Path, required=True)

    def handle(
        self,
        *,
        file: Path,
        verbosity: int,
        settings: str,
        pythonpath: str,
        traceback: bool,
        no_color: bool,
        force_color: bool,
        skip_checks: bool,
    ) -> None:
        status_lut = {
            v: k
            for k, v in Person.PersonStatus.choices
        }
        licence_lut = {
            v: k
            for k, v in Person.RadioLicence.choices
        }
        with file.open('r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                person, _ = Person.objects.get_or_create(
                    name=row['Name'].strip(),
                    defaults={
                        'status': status_lut.get(row['Status']),
                        'is_active': row['Active'].strip() == "Yes",
                    },
                )

                person.nickname = row['Nickname'].strip()
                person.irc_nick = row['IRC Nick'].strip()
                person.radio_licence = licence_lut.get(row['Licence'], '')
                person.is_radio_instructor = row['Instructor'].strip() == "Yes"
                person.save()

                for field in ['Callsign 1', 'Callsign 2', 'Callsign 3']:
                    if callsign := row[field].strip():
                        RadioCallsign.objects.get_or_create(callsign=callsign, owner=person)

                if degree_name := row['Degree Type']:
                    degree_type, _ = DegreeType.objects.get_or_create(name=degree_name)
                else:
                    degree_type = None

                if course_name := row['Degree Course']:
                    degree_course, _ = DegreeSubject.objects.get_or_create(name=course_name)
                else:
                    degree_course = None

                if degree_type or degree_course or row['Graduation Year'].strip():
                    DegreeCourse.objects.get_or_create(
                        person=person,
                        defaults={
                            'subject': degree_course,
                            'degree_type': degree_type,
                            'graduation_year': row['Graduation Year'].strip(),
                        },
                    )

        self.stdout.write("Imported people")

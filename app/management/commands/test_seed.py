from django.core.management.base import BaseCommand
from app.models import Cake, YumRating
import random


class Command(BaseCommand):
    help = "Seeds some initial data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--wipe",
            action="store_true",
            help="Wipes the database prior to seeding it",
        )

    def handle(self, *args, **options):
        if options["wipe"]:
            YumRating.objects.all().delete()
            Cake.objects.all().delete()

        for i in range(5):
            cake = Cake.objects.create(
                name='cake %s' % i,
                comment='comment %s' % i,
                imageUrl='https://www.example.com/%s.jpg' % i
            )

            for _ in range(3):
                YumRating.objects.create(
                    cake=cake,
                    rating=random.randint(1, 5)
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded_data')
        )

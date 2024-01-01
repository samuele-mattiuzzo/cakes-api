from app.const import CAKE_NAME_MAX_LENGTH, YUM_RATING_MAX_VALUE
from app.models import Cake, YumRating
from django.forms import ValidationError
from django.test import TestCase

valid_cake_arguments = {
    'name': 'name',
    'comment': 'comment',
    'imageUrl': 'https://www.valid.com/url.png'
}


class CakeModelTestCase(TestCase):
    def test_valid_cake_creation(self):
        Cake.objects.create(**valid_cake_arguments)
        self.assertEqual(Cake.objects.count(), 1)

        cake = Cake.objects.first()
        self.assertEqual(
            cake.name, valid_cake_arguments['name'])
        self.assertEqual(
            cake.comment, valid_cake_arguments['comment'])
        self.assertEqual(
            cake.imageUrl, valid_cake_arguments['imageUrl'])

    def test_invalid_cake_errors(self):
        cake = Cake(
            name='aa' * CAKE_NAME_MAX_LENGTH,
            comment=valid_cake_arguments['comment'],
            imageUrl=valid_cake_arguments['imageUrl']
        )
        with self.assertRaises(ValidationError):
            cake.full_clean()
        self.assertEqual(Cake.objects.count(), 0)


class YumRatingModelTestCase(TestCase):
    def setUp(self):
        self.valid_rating = YUM_RATING_MAX_VALUE
        self.invalid_rating = YUM_RATING_MAX_VALUE + 1
        self.cake = Cake.objects.create(
            **valid_cake_arguments)

    def test_valid_rating_creation(self):
        self.assertEqual(Cake.objects.count(), 1)

        YumRating.objects.create(
            cake=self.cake,
            rating=self.valid_rating
        )

        self.assertEqual(YumRating.objects.count(), 1)

    def test_invalid_rating_raises_error(self):
        self.assertEqual(Cake.objects.count(), 1)

        yum = YumRating(
            cake=self.cake,
            rating=self.invalid_rating
        )
        with self.assertRaises(ValidationError):
            yum.full_clean()
        self.assertEqual(YumRating.objects.count(), 0)


class YumFactorTestCase(TestCase):
    def setUp(self):
        self.test_ratings = [5, 5, 5, 4, 4]
        cake = Cake.objects.create(**valid_cake_arguments)
        for rating in self.test_ratings:
            YumRating.objects.create(
                cake=cake,
                rating=rating
            )

    def test_yumfactor_is_int(self):
        self.assertEqual(Cake.objects.count(), 1)
        self.assertEqual(YumRating.objects.count(), len(self.test_ratings))

        cake = Cake.objects.first()
        self.assertEqual(
            cake.yumFactor,
            round(sum(self.test_ratings) / len(self.test_ratings))
        )

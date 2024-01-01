from app.const import CAKE_NAME_MAX_LENGTH
from app.models import Cake, YumRating
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

valid_cake_arguments = {
    'name': 'name',
    'comment': 'comment',
    'imageUrl': 'https://www.valid.com/url.png'
}
valid_cake_rating = 5
dummy_cache = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}


class CakesAPITestCase(APITestCase):

    def _dummy_data(self):
        for _ in range(2):
            Cake.objects.create(**valid_cake_arguments)
        example_cake = Cake.objects.first()
        YumRating.objects.create(**{
            'cake': example_cake,
            'rating': valid_cake_rating
        })

    def test_cake_create_missing_attributes(self):
        self.assertEqual(Cake.objects.count(), 0)
        missing_cake_arguments = {
            'comment': 'comment',
            'imageUrl': 'http://www.google.com/img.jpg'
        }
        response = self.client.post(
            '/api/cakes/create/',
            missing_cake_arguments,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.data['name'][0].title(),
            'This Field Is Required.'
        )
        self.assertEqual(Cake.objects.count(), 0)

    def test_cake_create_wrong_attribute(self):
        self.assertEqual(Cake.objects.count(), 0)
        wrong_cake_arguments = {
            'name': 'name' * CAKE_NAME_MAX_LENGTH,  # too long
            'comment': 'comment',
            'imageUrl': 'https://www.valid.com/url.png'
        }
        response = self.client.post(
            '/api/cakes/create/',
            wrong_cake_arguments,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['name'][0].title(),
            'Ensure This Field Has No More Than %s Characters.' % (
                CAKE_NAME_MAX_LENGTH
            )
        )
        self.assertEqual(Cake.objects.count(), 0)

    def test_cake_create_success(self):
        self.assertEqual(Cake.objects.count(), 0)
        response = self.client.post(
            '/api/cakes/create/',
            valid_cake_arguments,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cake.objects.count(), 1)

    def test_cake_delete_non_existing_id(self):
        does_not_exist_pk = 123
        response = self.client.delete(
            '/api/cakes/delete/%s' % does_not_exist_pk,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['detail'].title(),
            'Not Found.'
        )

    def test_cake_delete_success(self):
        Cake.objects.create(**valid_cake_arguments)
        self.assertEqual(Cake.objects.count(), 1)

        cake_id = Cake.objects.first().pk
        response = self.client.delete(
            '/api/cakes/delete/{}'.format(cake_id),
            format='json')

        self.assertEqual(Cake.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_yum_vote_non_existing_cake_id(self):
        does_not_exist_pk = 123
        self.assertEqual(YumRating.objects.count(), 0)
        response = self.client.post(
            '/api/yum/create/',
            {'cake': does_not_exist_pk, 'rating': valid_cake_rating},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['cake'][0].title(),
            'Invalid Pk "%s" - Object Does Not Exist.' % (
                does_not_exist_pk
            )
        )
        self.assertEqual(YumRating.objects.count(), 0)

    def test_yum_vote_success(self):
        self.assertEqual(YumRating.objects.count(), 0)
        Cake.objects.create(**valid_cake_arguments)
        self.assertEqual(Cake.objects.count(), 1)

        cake_id = Cake.objects.first().pk
        response = self.client.post(
            '/api/yum/create/',
            {'cake': cake_id, 'rating': valid_cake_rating},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(YumRating.objects.count(), 1)

    def test_yum_vote_no_rating_defaults_to_1(self):
        self.assertEqual(YumRating.objects.count(), 0)
        Cake.objects.create(**valid_cake_arguments)
        self.assertEqual(Cake.objects.count(), 1)

        cake_id = Cake.objects.first().pk
        response = self.client.post(
            '/api/yum/create/',
            {'cake': cake_id},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(YumRating.objects.count(), 1)
        self.assertEqual(YumRating.objects.first().rating, 1)

    @override_settings(CACHES=dummy_cache)
    def test_cake_list(self):
        self._dummy_data()

        response = self.client.get(
            '/api/cakes/list/',
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        objects = response.data['results']

        self.assertEqual(len(objects), 2)
        self.assertEqual(objects[0]['yumFactor'], valid_cake_rating)
        self.assertEqual(objects[1]['yumFactor'], 1)

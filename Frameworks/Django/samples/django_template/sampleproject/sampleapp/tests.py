from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve

from sampleapp.models import Sample
from sampleapp.views import sample_edit

UserModel = get_user_model()


class CreateSampleTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username='test_user',
            email='test@sample.com',
            password='password@12345',
        )
        self.client.force_login(self.user)

    def test_render_creation_form(self):
        response = self.client.get('/sampleapp/new/')
        self.assertContains(response, 'sampleappの登録画面', status_code=200)

    def test_create_sample(self):
        data = {'title': 'タイトル', 'text': 'テキスト'}
        self.client.post('/sampleapp/new/', data)
        sample = Sample.objects.get(title='タイトル')
        self.assertEqual('テキスト', sample.text)


class EditSampleTest(TestCase):
    def test_should_resolve_sample_edit(self):
        found = resolve('/sampleapp/1/edit/')
        self.assertEqual(sample_edit, found.func)

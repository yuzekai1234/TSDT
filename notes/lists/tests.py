from django.test import TestCase
from django.urls import resolve
from .views import home_page
from django.http import HttpRequest
# Create your tests here.
class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'home.html')
    def test_can_save_a_POST_request(self):
        response=self.client.post('/',data={'item_text':'A new list item'})
        self.assertIn('A new list item',response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
    def test_home_page_return_correct_html(self):
        request =HttpRequest()
        response=home_page(request)
        html=response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>',html)
        self.assertTrue(html.endswith('</html>'))
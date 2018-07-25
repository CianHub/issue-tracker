from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
import os

class TestViews(TestCase):

    def test_charts_page(self):
            """Test that charts page works, is accessible to logged in users 
            and is using the correct template"""
            
            user = User.objects.create_user(username='Test', first_name='test',
            last_name='tester', password='123password123',
            email='test@test.com')
            user.save()
            self.client.login(username='Test', password='123password123')
            
            response = self.client.get("/charts/charts/", follow=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "charts.html")
    
    def test_charts_page_logged_out(self):
            #Test that charts page cannot be accessed by logged out users
            
            response = self.client.get("/charts/charts/", follow=True)
            self.assertRedirects(response,
            expected_url='/accounts/login/?next=/charts/charts/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)
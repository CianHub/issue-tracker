from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
class TestModels(TestCase):
    
    def test_create_user(self):
        #Test if a new user can be created 
        
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        self.assertEqual(user.username,'Test')
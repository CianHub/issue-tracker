from django.test import TestCase
from .models import CustomUser

# Create your tests here.
class TestModels(TestCase):
    def test_is_active_default(self):
        #Test if is_active is set to true by default when a new user is created
        
        user = CustomUser(username="Test", password="123password123", first_name='test', last_name='test', email='test@test.com')
        user.save()
        self.assertEqual(user.username,'Test')
        self.assertEqual(user.is_active, True)
    
    def test_create_user(self):
        #Test if a new user can be created 
        
        user = CustomUser(username="Test", password="123password123", first_name='test', last_name='test', email='test@test.com')
        user.save()
        self.assertEqual(user.username,'Test')
     
        
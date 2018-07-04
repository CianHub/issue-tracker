from django.test import TestCase
from .forms import UserForm, EditUserForm

# Create your tests here.
class TestForms(TestCase):
    
    def test_if_user_can_be_created(self):
        #Tests that a user can be created
        form = UserForm({'first_name': 'Test', 'last_name': 'Test', 'email': 'test@test.com', 'password': '123password123', 'username': 'TestUser'})
        self.assertTrue(form.is_valid())
    
    def test_if_user_requires_username(self):
        #Tests that a user requires a username to be created
        form = UserForm({'first_name': 'Test', 'last_name': 'Test', 'email': 'test@test.com', 'password': '123password123', 'username': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])
    
    def test_if_user_requires_password(self):
        #Tests that a user requires a password to be created
        form = UserForm({'first_name': 'Test', 'last_name': 'Test', 'email': 'test@test.com', 'password': '', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], [u'This field is required.'])
    
    def test_if_user_requires_first_name(self):
        #Tests that a user requires a first_name to be created
        form = UserForm({'first_name': '', 'last_name': 'test', 'email': 'test@test.com', 'password': '123password123', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], [u'This field is required.'])
        
    def test_if_user_requires_last_name(self):
        #Tests that a user requires a last_name to be created
        form = UserForm({'first_name': 'Test', 'last_name': '', 'email': 'test@test.com', 'password': '123password123', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['last_name'], [u'This field is required.'])
    
    def test_if_user_requires_email(self):
        #Tests that a user requires a first_name to be created
        form = UserForm({'first_name': 'test', 'last_name': 'test', 'email': '', 'password': '123password123', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [u'This field is required.'])
    
from django.test import TestCase
from .forms import UserRegistrationForm, UserLogin, EditUserForm
from django.contrib.auth.models import User

class TestForms(TestCase):
    
    # User Registration Form Tests
    
    def test_if_user_can_be_created(self):
        #Tests that a user can be created
        
        form = UserRegistrationForm({'first_name': 'Test', 'last_name': 'Test',
        'email': 'test@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser'})
        self.assertTrue(form.is_valid())
    
    def test_if_user_requires_unique_username_and_email(self):
        #Tests that a user must have a unique username and email
        
        form = UserRegistrationForm({'first_name': 'Test', 'last_name': 'Test',
        'email': 'test@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser'})
        form.save()
        self.assertTrue(form.is_valid())
        
        form2 = UserRegistrationForm({'first_name': 'Test', 'last_name': 'Test',
        'email': 'test2@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser'})
        self.assertFalse(form2.is_valid())
        
        form3 = UserRegistrationForm({'first_name': 'Test', 'last_name': 'Test',
        'email': 'test@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser2'})
        self.assertFalse(form3.is_valid())
    
    def test_if_user_requires_username(self):
        #Tests that a user requires a username to be created
        
        form = UserRegistrationForm({'first_name': 'Test', 'last_name': 'Test',
        'email': 'test@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])
    
    def test_if_user_requires_password(self):
        #Tests that a user requires a password to be created
        
        form = UserRegistrationForm({'first_name': 'Test', 'last_name': 'Test',
        'email': 'test@test.com', 'password1': '',
        'password2': '','username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password1'], [u'This field is required.'])
        self.assertEqual(form.errors['password2'], [u'This field is required.'])
    
    def test_if_user_requires_first_name(self):
        #Tests that a user requires a first_name to be created
        
        form = UserRegistrationForm({'first_name': '', 'last_name': 'Test',
        'email': 'test@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], [u'This field is required.'])
        
    def test_if_user_requires_last_name(self):
        #Tests that a user requires a last_name to be created
        form = UserRegistrationForm({'first_name': 'Test', 'last_name': '', 'email': 'test@test.com', 'password1': '123password123','password2': '123password123', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['last_name'], [u'This field is required.'])
    
    def test_if_user_requires_email(self):
        #Tests that a user requires a first_name to be created
        
        form = UserRegistrationForm({'first_name': 'Test', 'last_name': 'Test',
        'email': '', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [u'This field is required.'])
    
    # User Login Form Tests
    
    def test_if_user_can_be_logged_in(self):
        #Tests that a user can be logged in
        
        user = User.objects.create_user(username='Test',
        first_name='test', last_name='tester', password='123password123',
        email='test@test.com')
        user.save()
        
        form = UserLogin({'password': '123password123','username': 'Test'})
        
        self.assertTrue(form.is_valid())
        
        form = UserLogin({'password': '123password123','username': 'test@test.com'})
        
        self.assertTrue(form.is_valid())
    
    def test_if_login_requires_username_and_password(self):
        #Tests that a user can be logged in
        
        form = UserLogin({'password': '','username': 'Test'})
        self.assertFalse(form.is_valid())
        
        form = UserLogin({'password': 'password12345','username': ''})
        self.assertFalse(form.is_valid())
    
    # Edit User Form Tests
    
    def test_if_user_can_be_edited(self):
        #Tests that a user can be edited
        
        form = EditUserForm({'first_name': 'Test', 'last_name': 'Test',
        'email': 'test@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser'})
        self.assertTrue(form.is_valid())
    
    def test_if_edit_user_form_requires_username(self):
        #Tests that a user requires a username when being edited
        
        form = EditUserForm({'first_name': 'Test', 'last_name': 'Test',
        'email': 'test@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])
    
    def test_if_edit_user_form_requires_first_name(self):
        #Tests that a user requires a first_name when being edited
        
        form = EditUserForm({'first_name': '', 'last_name': 'Test',
        'email': 'test@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], [u'This field is required.'])
        
    def test_if_edit_user_form_requires_last_name(self):
        #Tests that a user requires a last_name when being edited
        form = EditUserForm({'first_name': 'Test', 'last_name': '', 
        'email': 'test@test.com', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['last_name'], [u'This field is required.'])
    
    def test_if_edit_user_form_requires_email(self):
        #Tests that a user requires an email when being edited
        
        form = EditUserForm({'first_name': 'Test', 'last_name': 'Test',
        'email': '', 'password1': '123password123',
        'password2': '123password123', 'username': 'TestUser'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [u'This field is required.'])
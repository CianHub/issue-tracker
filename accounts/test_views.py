from django.test import TestCase
from .views import index, user_list, register, edit_user, logout, login, profile
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse

class TestViews(TestCase):
    
    # Home Page

    def test_home_page(self):
        #Test that home page works and is using the correct template
        
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "index.html")
        
    # Register Page
    
    def test_register_page(self):
        #Test that the register page works and is using the correct template
         
        page = self.client.get("/accounts/register/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_user.html")
    
    def test_register_page_if_logged_in(self):
        #Test that logged in users cannot access the register page 
        
        user = User.objects.create_user(username='Test', password='123password123')
        user.save()
        self.client.login(username='Test', password='123password123')
         
        page = self.client.get("/accounts/register/")
        self.assertEqual(page.status_code, 302)
    
    # Edit User Page
    
    def test_edit_user_page(self):
        """Test that edit user page is generated for existing users, is using 
        the correct template and is only accessible to logged in users"""
         
        user = User.objects.create_user(username='Test',
        password='123password123')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/accounts/profile/edit/{0}".format(user.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "edit_user.html")
    
    def test_edit_user_page_for_user_that_doesnt_exist(self):
        #Test that edit user page is only generated when the user exists
        
        user = User.objects.create_user(username='Test',
        password='123password123', is_staff=True)
        
        user.save()
        
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/accounts/edit/2")
        self.assertEqual(page.status_code, 404)
    
    def test_edit_user_page_is_blocked_to_different_users(self):
        #Test that edit user page is blocked unless it belongs to the logged in user
         
        user = User.objects.create_user(username='Test', password='123password123')
        user.save()
        user2 = User.objects.create_user(username='Test2', password='123password123')
        user2.save()
        self.client.login(username='Test', password='123password123')
        
        response = self.client.get(
            "/accounts/profile/edit/{0}".format(user2.id),follow=True)
        
        for i in response.context['messages']:
            message = str(i)
        
        self.assertEqual(message,'You Do Not Have Permission To View This Page')
        self.assertRedirects(response, expected_url=reverse('index'),
        status_code=302, target_status_code=200, fetch_redirect_response=True)
        
     # Delete User Page
    
    # Delete User Page
    
    def test_delete_user_page(self):
        """Test that delete user page is generated for existing users
        and is only accessible to logged in users"""
         
        user = User.objects.create_user(username='Test',
        password='123password123', is_staff=True)
        
        user.save()
        
        user2 = User.objects.create_user(username='Test2',
        password='123password123')
        
        user2.save()
        
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/accounts/delete/{0}".format(user2.id))
        self.assertRedirects(page, expected_url=reverse('user_list'),
        status_code=302, target_status_code=200, fetch_redirect_response=True)
        
        page2 = self.client.get("/accounts/delete/{0}".format(user2.id))
        self.assertEqual(page2.status_code, 404)
        
    def test_delete_user_page_for_user_that_doesnt_exist(self):
        #Test that delete user page is only generated when the user exists
        
        user = User.objects.create_user(username='Test',
        password='123password123', is_staff=True)
        
        user.save()
        
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/accounts/delete/2")
        self.assertEqual(page.status_code, 404)
    
    # Login Page

    def test_login_page_if_logged_in(self):
        # Test that logged in users cant access the page
        
        user = User.objects.create_user(username='Test',
        password='123password123')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        response = self.client.get("/accounts/login/", follow=True)
    
        self.assertRedirects(response, expected_url=reverse('index'),
        status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_login_page_if_logged_out(self):
        # Test that logged out users can access the page
        
        page = self.client.get("/accounts/login/")
        self.assertEqual(page.status_code, 200)
        
    # Logout Page
    
    def test_logout_page_if_logged_in(self):
        # Test that logged in users can access the page  
        
        user = User.objects.create_user(username='Test',
        password='123password123')
        user.save()
        self.client.login(username='Test', password='123password123')
    
        response = self.client.get("/accounts/logout/",follow=True)
        
        for i in response.context['messages']:
            message = str(i)
        
        self.assertEqual(message,'You have successfully been logged out!')
        self.assertRedirects(response, expected_url=reverse('index'),
        status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_logout_page_if_logged_out(self):
        # Test that logged out users cant access the page
        
        page = self.client.get("/accounts/logout/")
        self.assertEqual(page.status_code, 302)
    
    # Profile Page
    
    def test_profile_page(self):
        """Test that profile page is generated for existing users,
        is using the correct template and is 
        only accessible to logged in users"""
         
        user = User.objects.create_user(username='Test', first_name='test',
        last_name='tester', password='123password123', email='test@test.com')
        user.save()
        
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/accounts/profile/{0}".format(user.id))
        
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "profile.html")
    
    def test_profile_page_if_logged_out(self):
        #Test that profile page is only generated when the user exists
        
        user = User.objects.create_user(username='Test', first_name='test',
        last_name='tester', password='123password123', email='test@test.com')
        user.save()
        
        response = self.client.get("/accounts/profile/{0}".format(user.id))
        
        self.assertRedirects(response,
        expected_url='/accounts/login/?next=/accounts/profile/{0}'.format(user.id),
        status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    # User List Page

    def test_user_list_page(self):
        #Test that user list page works and is using the correct template
        
        user = User.objects.create_user(username='Test',
        password='123password123', is_staff=True)
        user.save()
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/accounts/user_list/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "user_list.html")
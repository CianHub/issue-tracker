from django.test import TestCase
from .views import user_list, add_user, edit_user
from .models import CustomUser

# Create your tests here.
class TestViews(TestCase):
    
    def test_home_page(self):
        #Test that home page works and is using the correct template
        
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "user_list.html")
    
    def test_add_user_page(self):
        #Test that add user page works and is using the correct template
         
        page = self.client.get("/add_user")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_user.html")
    
    def test_edit_user_page(self):
        #Test that edit user page is generated for existing users and is using the correct template
         
        user = CustomUser.objects.create_user(username='TestUser', password='123password123')
        user.save()
        page = self.client.get("/edit/{0}".format(user.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_user.html")
    
    def test_edit_user_page_for_user_that_doesnt_exist(self):
        #Test that edit user page is only generated when the user exists
        
        page = self.client.get("/edit/1")
        self.assertEqual(page.status_code, 404)
       
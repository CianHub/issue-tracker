from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
from .models import Ticket, TicketType, Comment


class TestViews(TestCase):
    
    # Ticket Index Page
    
    def test_ticket_index(self):
        #Test that ticket index works and is using the correct template
        
        user = User.objects.create_user(username='Test', password='123password123')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/tickets/ticket_index/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "ticket_index.html")
    
    def test_ticket_index_if_logged_out(self):
        #Test that ticket index cant be accessed by logged out users
        
        response = self.client.get("/tickets/ticket_index/", follow=True)
        self.assertRedirects(response, expected_url='/accounts/login/?next=/tickets/ticket_index/', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    #Create ticket page

    def test_create_ticket(self):
        #Test that the create ticket page works and is using the correct template
         
        user = User.objects.create_user(username='Test', password='123password123')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/tickets/create_ticket/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "create_ticket.html")
    
    def test_create_ticket_bug_if_logged_in(self):
        #Test that logged out users cant create tickets
         
        response = self.client.get("/tickets/create_ticket/", follow=True)
        self.assertRedirects(response, expected_url='/accounts/login/?next=/tickets/create_ticket/', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    #Ticket Detail Page
    
    def test_ticket_detail_page(self):
        #Test that ticket detail page is generated for existing tickets, is using the correct template and is only accessible to logged in users
         
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        ticket = Ticket(title='test', author=user, username=user.username, description='test', ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        page = self.client.get("/tickets/ticket_index/view_ticket/{0}".format(ticket.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "ticket_detail.html")
    
    def test_ticket_detail_page_when_ticket_doesnt_exist(self):
        #Test that ticket detail page is not generated for tickets that dont exist
         
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/tickets/ticket_index/view_ticket/1")
        self.assertEqual(page.status_code, 404)

    def test_ticket_detail_page_when_logged_out(self):
        #Test that ticket detail page is blocked for logged out users
        
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        
        ticket = Ticket(title='test', author=user, username=user.username, description='test', ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        response = self.client.get("/tickets/ticket_index/view_ticket/{0}".format(ticket.id))

        self.assertRedirects(response, expected_url='/accounts/login/?next=/tickets/ticket_index/view_ticket/1', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    # Edit Ticket Page
    
    def test_edit_ticket_page(self):
        #Test that edit ticket page is generated for existing users, iss using the correct template and is only accessible to logged in users
         
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        ticket = Ticket(title='test', author=user, username=user.username, description='test', ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        page = self.client.get("/tickets/ticket_index/edit_ticket/{0}".format(ticket.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "edit_ticket.html")
    
    def test_edit_ticket_page_for_ticket_that_doesnt_exist(self):
        #Test that edit ticket page is only generated when the ticket exists
        
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/tickets/ticket_index/edit_ticket/1")
        self.assertEqual(page.status_code, 404)
    
    def test_edit_ticket_page_is_blocked_to_different_users(self):
        
        #Test that edit ticket page is blocked unless it belongs to the logged in user
         
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        
        user2 = User.objects.create_user(username='Test2', first_name='test', last_name='tester', password='123password123', email='test2@test.com')
        user2.save()

        ticket = Ticket(title='test', author=user, username=user.username, description='test', ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        self.client.login(username='Test2', password='123password123')
        
        page = self.client.get("/tickets/ticket_index/edit_ticket/{0}".format(ticket.id))
        
        self.assertRedirects(page, expected_url=reverse('index'), status_code=302, target_status_code=200, fetch_redirect_response=True)
    

    
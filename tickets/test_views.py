from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
from .models import Ticket, TicketType, Comment
import os
from django.contrib.sessions.middleware import SessionMiddleware


class TestViews(TestCase):
    
    # Ticket Index Page
    
    def test_ticket_index(self):
        #Test that ticket index works and is using the correct template
        
        user = User.objects.create_user(username='Test',
        password='123password123')
        user.save()
        self.client.login(username='Test',
        password='123password123')
        
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
         
        user = User.objects.create_user(username='Test',
        password='123password123')
        user.save()
        self.client.login(username='Test',
        password='123password123')
        
        page = self.client.get("/tickets/create_ticket/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "create_ticket.html")
    
    def test_create_ticket_bug_if_logged_in(self):
        #Test that logged out users cant access the page
         
        response = self.client.get("/tickets/create_ticket/", follow=True)
        self.assertRedirects(response, expected_url='/accounts/login/?next=/tickets/create_ticket/', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    #Ticket Detail Page
    
    def test_ticket_detail_page(self):
        """Test that ticket detail page is generated for existing tickets, is 
        using the correct template and is only accessible to logged in users"""
         
        user = User.objects.create_user(username='Test',
        first_name='test', last_name='tester',
        password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        ticket = Ticket(title='test', author=user,
        username=user.username, description='test',
        ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        ticket_type = TicketType(ticket=ticket, ticket_type=ticket.ticket_type,
        match_ticket_id=ticket.id,
        ticket_title=ticket.title, bug_or_request='bug', value=0.00)
        ticket_type.save()
        
        page = self.client.get(
            "/tickets/ticket_index/view_ticket/{0}".format(ticket.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "ticket_detail.html")
    
    def test_ticket_detail_page_when_ticket_doesnt_exist(self):
        #Test that a page is not generated for tickets that dont exist
         
        user = User.objects.create_user(username='Test', first_name='test',
        last_name='tester', password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/tickets/ticket_index/view_ticket/1")
        self.assertEqual(page.status_code, 404)

    def test_ticket_detail_page_when_logged_out(self):
        #Test that ticket detail page is blocked for logged out users
        
        user = User.objects.create_user(username='Test',
        first_name='test', last_name='tester',
        password='123password123', email='test@test.com')
        user.save()
        
        ticket = Ticket(title='test', author=user,
        username=user.username, description='test',
        ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        response = self.client.get(
            "/tickets/ticket_index/view_ticket/{0}".format(ticket.id))

        self.assertRedirects(
            response,
            expected_url='/accounts/login/?next=/tickets/ticket_index/view_ticket/1',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
            )
    
    # Edit Ticket Page
    
    def test_edit_ticket_page(self):
        """Test that edit ticket page is generated for existing tickets, 
        is using the correct template and is 
        only accessible to logged in users"""
         
        user = User.objects.create_user(
            username='Test', first_name='test',
            last_name='tester',
            password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        ticket = Ticket(
            title='test', author=user, username=user.username,
            description='test', ticket_type=2,
            status=1, comment_num=0, upvotes=0
            )
        ticket.save()
        
        page = self.client.get(
            "/tickets/ticket_index/edit_ticket/{0}".format(ticket.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "edit_ticket.html")
    
    def test_edit_ticket_page_for_ticket_that_doesnt_exist(self):
        #Test that edit ticket page is only generated when the ticket exists
        
        user = User.objects.create_user(username='Test',
        first_name='test', last_name='tester',
        password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/tickets/ticket_index/edit_ticket/1")
        self.assertEqual(page.status_code, 404)
    
    # Delete Ticket Page
    
    def test_delete_ticket_page(self):
        """Test that delete ticket page is generated for existing tickets,
        and is only accessible to logged in users"""
         
        user = User.objects.create_user(
            username='Test', first_name='test',
            last_name='tester', password='123password123',
            email='test@test.com'
            )
        user.save()
        self.client.login(username='Test', password='123password123')
        
        ticket = Ticket(title='test', author=user,
        username=user.username, description='test',
        ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        page = self.client.get(
            "/tickets/ticket_index/delete_ticket/{0}".format(ticket.id))
        self.assertEqual(page.status_code, 302)

    def test_delete_ticket_page_for_ticket_that_doesnt_exist(self):
        #Test that delete ticket url is only generated when the ticket exists
        
        user = User.objects.create_user(
            username='Test', first_name='test',
            last_name='tester',
            password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        page = self.client.get("/tickets/ticket_index/delete_ticket/1")
        self.assertEqual(page.status_code, 404)
        
    # Ticket Payment Page
    
    def test_ticket_payment_page(self):
        """Test that the ticket payment page requires a dictionary 
        to be passed via session data to be accessible to logged in users"""
         
        user = User.objects.create_user(
            username='Test', first_name='test',
            last_name='tester', password='123password123',
            email='test@test.com'
            )
        user.save()
        self.client.login(username='Test', password='123password123')
        
        ticket = Ticket(title='test', author=user,
        username=user.username, description='test',
        ticket_type=1, status=1, comment_num=0, upvotes=0)
        ticket.save()

        response = self.client.get("/tickets/pay_for_ticket/")
        
        self.assertEqual(response.status_code, 302)

    # Ticket Upvote Payment Page
    
    def test_upvote_ticket_payment_page(self):
        """Test that the upvote ticket payment page is 
        using the correct template and is only accessible to logged in users"""
         
        user = User.objects.create_user(
            username='Test', first_name='test',
            last_name='tester', password='123password123',
            email='test@test.com'
            )
        user.save()
        self.client.login(username='Test', password='123password123')
        
        ticket = Ticket(
            title='test', author=user,
            username=user.username, description='test',
            ticket_type=1, status=1, comment_num=0, upvotes=0
            )
        ticket.save()
        
        ticket_type = TicketType(
            ticket=ticket, ticket_type=ticket.ticket_type,
            match_ticket_id=ticket.id, ticket_title=ticket.title,
            bug_or_request='bug', value=0.00
            )
        ticket_type.save()
            
        response = self.client.get(
            "/tickets/view_ticket/{0}?".format(ticket.id)
            )

        self.assertEqual(response.status_code, 200)
        
    # Delete Comment Page
    
    def test_delete_comment_page(self):
        """Test that delete comment url is generated only for 
        existing comments, and is only accessible to logged in users"""
         
        user = User.objects.create_user(
            username='Test', first_name='test', last_name='tester',
            password='123password123', email='test@test.com',
            is_superuser=True
            )
        user.save()
        self.client.login(username='Test', password='123password123')

        ticket = Ticket(
            title='test', author=user,
            username=user.username, description='test',
            ticket_type=2, status=1, comment_num=0, upvotes=0
            )
        ticket.save()
        
        comment = Comment(
            username=user.username, ticket=ticket,
            ticket_owner_id=user.id, comment='test'
            )
        comment.save()
        
        ticket_type = TicketType(
            ticket=ticket, ticket_type=ticket.ticket_type,
            match_ticket_id=ticket.id, ticket_title=ticket.title,
            bug_or_request='bug', value=0.00
            )
        ticket_type.save()
        
        response = self.client.get(
            "/tickets/delete_comment/{0}".format(comment.id), follow=True)
        
        self.assertRedirects(
            response, 
            expected_url='/tickets/view_ticket/{0}'.format(ticket.id),
            status_code=302, 
            target_status_code=200, 
            fetch_redirect_response=True
            )
        
        #Shows that comment is deleted
        page = self.client.get(
            "/tickets/delete_comment/{0}".format(comment.id),
            follow=True)
        self.assertEqual(page.status_code, 404)

    def test_delete_comment_page_for_logged_out_users(self):
        #Test that delete comment url is only accessible to logged out users
        
        user = User.objects.create_user(
            username='Test', first_name='test',
            last_name='tester', password='123password123',
            email='test@test.com'
            )
        user.save()
        
        ticket = Ticket(
            title='test', author=user, username=user.username,
            description='test', ticket_type=2, status=1,
            comment_num=0, upvotes=0
            )
        ticket.save()
        
        comment = Comment(
            username=user.username, ticket=ticket,
            ticket_owner_id=user.id, comment='test'
            )
        comment.save()
        
        ticket_type = TicketType(
            ticket=ticket, ticket_type=ticket.ticket_type,
            match_ticket_id=ticket.id, ticket_title=ticket.title,
            bug_or_request='bug', value=0.00
            )
        ticket_type.save()
        
        response = self.client.get(
            "/tickets/delete_comment/{0}".format(comment.id),
            follow=True
            )

        #Redirects a logged out user to login page
        self.assertRedirects(
            response, 
            expected_url='/accounts/login/?next=/tickets/delete_comment/{0}'.format(comment.id),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
            )
    
    # Edit Comment Page
    
    def test_edit_comment_page(self):
        """Test that edit comment page is generated only for existing comments,
        uses the correct template and is only accessible to logged in users"""
         
        user = User.objects.create_user(
            username='Test', first_name='test',
            last_name='tester', password='123password123',
            email='test@test.com', is_superuser=True
            )
        user.save()
        self.client.login(username='Test', password='123password123')

        ticket = Ticket(
            title='test', author=user,
            username=user.username, description='test',
            ticket_type=2, status=1, comment_num=0, upvotes=0
        )
        ticket.save()
        
        comment = Comment(
            username=user.username, ticket=ticket,
            ticket_owner_id=user.id, comment='test'
            )
        comment.save()
        
        ticket_type = TicketType(
            ticket=ticket, ticket_type=ticket.ticket_type,
            match_ticket_id=ticket.id, ticket_title=ticket.title,
            bug_or_request='bug', value=0.00
            )
        ticket_type.save()
        
        response = self.client.get(
            "/tickets/edit_comment/{0}".format(comment.id),
            follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_comment.html")
        
    def test_edit_comment_page_if_user_logged_out(self):
        #Test that edit comment page is only accessible to logged in users
         
        user = User.objects.create_user(
            username='Test', first_name='test',
            last_name='tester', password='123password123',
            email='test@test.com', is_superuser=True
            )
        user.save()

        ticket = Ticket(
            title='test', author=user,
            username=user.username, description='test',
            ticket_type=2, status=1, comment_num=0, upvotes=0
            )
        ticket.save()
        
        comment = Comment(
            username=user.username, ticket=ticket,
            ticket_owner_id=user.id, comment='test'
            )
        comment.save()
        
        ticket_type = TicketType(
            ticket=ticket, ticket_type=ticket.ticket_type,
            match_ticket_id=ticket.id,
            ticket_title=ticket.title, bug_or_request='bug', value=0.00
            )
        ticket_type.save()
        
        response = self.client.get(
            "/tickets/edit_comment/{0}".format(comment.id), follow=True
            )
        
        #Redirects a logged out user to login page
        self.assertRedirects(
            response,
            expected_url='/accounts/login/?next=/tickets/edit_comment/{0}'.format(
                comment.id), 
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True
                )
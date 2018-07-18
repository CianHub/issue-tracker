from django.test import TestCase
from django.contrib.auth.models import User
from .forms import TicketForm, CommentForm
from .models import Ticket, TicketType, Comment


class TestForms(TestCase):
    
    # Ticket Form Tests
    
    def test_if_ticket_can_be_created(self):
        #Tests that a ticket can be created
        
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        instance = Ticket(author=user, username=user.username, ticket_type=2, status=1, comment_num=0, upvotes=0)
        
        form = TicketForm({'title': 'Test Ticket Title', 'description': 'Test', 'ticket_type': '2'}, instance=instance)
        form.save()
        
        self.assertTrue(form.is_valid())
    
    def test_ticket_form_requirements(self):
        #Tests that a ticket must have its requirements met to be created
        
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        self.client.login(username='Test', password='123password123')
        
        instance = Ticket(author=user, username=user.username, ticket_type=2, status=1, comment_num=0, upvotes=0)
        
        form = TicketForm({'title': '', 'description': 'Test'}, instance=instance)
        self.assertFalse(form.is_valid())
        
        form2 = TicketForm({'title': 'Test title', 'description': ''}, instance=instance)
        self.assertFalse(form2.is_valid())
        
        form3 = TicketForm({'title': 'Test title', 'description': 'Test','ticket_type': '2'})
        self.assertTrue(form3.is_valid())
        
        form4 = TicketForm({'title': 'Test title', 'description': 'Test', 'ticket_type': '2'}, instance=instance)
        self.assertTrue(form4.is_valid())
    
# Comment Form Tests
    
    def test_if_comment_can_be_created(self):
        #Tests that a comment can be created
        
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        
        self.client.login(username='Test', password='123password123')
        
        ticket = Ticket(author=user, username=user.username, ticket_type=2, status=1, comment_num=0, upvotes=0, title='Test', description='test')
        ticket.save()

        instance = Comment(username=user.username, ticket=ticket, ticket_owner_id=ticket.id)
        
        form = CommentForm({'comment': 'test comment'}, instance=instance)
        form.save()

        self.assertTrue(form.is_valid())
    
    def test_comment_form_requirements(self):
        #Tests that a comment can be created if requirements arent met
        
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        
        self.client.login(username='Test', password='123password123')
        
        ticket = Ticket(author=user, username=user.username, ticket_type=2, status=1, comment_num=0, upvotes=0, title='Test', description='test')
        ticket.save()
        
        instance = Comment(username=user.username, ticket=ticket, ticket_owner_id=ticket.id)
        
        form = CommentForm({'comment': ''}, instance=instance)
        
        form2 = CommentForm({'comment': 'test comment'}, instance=instance)
        form2.save()

        self.assertFalse(form.is_valid())
        
        self.assertTrue(form2.is_valid())
  
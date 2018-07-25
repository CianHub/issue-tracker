from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ticket, TicketType, Comment

class TestModels(TestCase):
    
    def test_create_ticket(self):
        #Test if a new ticket can be created
        
        user = User.objects.create_user(username='Test',
        first_name='test', last_name='tester',
        password='123password123', email='test@test.com')
        user.save()
        
        ticket = Ticket(title='test', author=user,
        username=user.username, description='test',
        ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        self.assertEqual(ticket.username,'Test')
        self.assertEqual(ticket.author, user)
    
    def test_create_ticket_type(self):
        #Test if a new ticket type entry can be created
        
        user = User.objects.create_user(username='Test',
        first_name='test', last_name='tester',
        password='123password123', email='test@test.com')
        user.save()
        
        ticket = Ticket(title='test', author=user,
        username=user.username, description='test',
        ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        ticket_type = TicketType(ticket=ticket,
        ticket_type=ticket.ticket_type, match_ticket_id=ticket.id,
        ticket_title=ticket.title, bug_or_request='bug', value=0.00)
        ticket_type.save()
        
        self.assertEqual(ticket_type.ticket_type,2)
        self.assertEqual(ticket_type.ticket, ticket)
        
    def test_create_comment(self):
        # Test if a new comment can be created
         
         user = User.objects.create_user(username='Test',
         first_name='test', last_name='tester',
         password='123password123', email='test@test.com')
         user.save()
        
         ticket = Ticket(title='test', author=user,
         username=user.username, description='test',
         ticket_type=2, status=1, comment_num=0, upvotes=0)
         ticket.save()
         
         comment = Comment(comment = 'test', username='test',
         ticket=ticket, ticket_owner_id = ticket.id)
        
         self.assertEqual(comment.comment, 'test')
         self.assertEqual(comment.username, 'test')
         self.assertEqual(comment.ticket_owner_id, ticket.id)
    
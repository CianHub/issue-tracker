from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ticket_Time
from tickets.models import Ticket

# Create your tests here.
class TestModels(TestCase):
    
    def test_ticket_time(self):
        #Test if a new ticket_time object can be created
        
        user = User.objects.create_user(username='Test', first_name='test', last_name='tester', password='123password123', email='test@test.com')
        user.save()
        
        ticket = Ticket(title='test', author=user, username=user.username, description='test', ticket_type=2, status=1, comment_num=0, upvotes=0)
        ticket.save()
        
        time = Ticket_Time(ticket=ticket, match_ticket_id=ticket.id)
        time.save()
        
        self.assertEqual(time.ticket,ticket)
        self.assertEqual(time.match_ticket_id, ticket.id)
    
    
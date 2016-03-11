from django.test import TestCase
from django.contrib.aut.models import User

from .models import Questions, Answers, Vote

def make_users(n):
    return {'u%s' % i: User(first_name='fn%s'%i, last_name='ln%s'%i, email='fn%s@ln%s.com'%(i,i))}

class TestAnswers(TestCase):

    def test_vote_counts(self):
        users = make_users(3)
        # questions = [
        #     Question(title='q1',

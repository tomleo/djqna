from django.test import TestCase
from django.contrib.auth.models import User

from .models import Question, Answer, Vote

def make_users(n):
    return {'u%s' % i: User(first_name='fn%s'%i,
                            last_name='ln%s'%i,
                            username='fn%sln%s'%(i,i),
                            email='fn%s@ln%s.com'%(i,i)) for i in range(1,n+1)}
def save_users(user_dict):
    for user in user_dict.values():
        user.save()
    return user_dict

class TestAnswers(TestCase):

    def test_positive_vote_counts(self):
        users = save_users(make_users(4))
        q1 = Question.objects.create(title='a', user=users['u1'], text='a')
        v1 = Vote.objects.create(user=users['u2'], content_object=q1)
        v2 = Vote.objects.create(user=users['u3'], content_object=q1)
        v3 = Vote.objects.create(user=users['u4'], content_object=q1)
        self.assertEqual(v1.object_id, q1.id)
        self.assertEqual(v1.content_type.name, 'question')
        self.assertEqual(v1.content_object, q1)
        q1 = Question.objects.get(pk=q1.pk) # CREAM
        self.assertEqual(q1.up_votes, 3)
        self.assertEqual(q1.down_votes, 0)

    def test_negative_vote_counts(self):
        users = save_users(make_users(4))
        q1 = Question.objects.create(title='a', user=users['u1'], text='a')
        v1 = Vote.objects.create(user=users['u2'], content_object=q1, is_positive=False)
        v2 = Vote.objects.create(user=users['u3'], content_object=q1, is_positive=False)
        v3 = Vote.objects.create(user=users['u4'], content_object=q1, is_positive=False)
        self.assertEqual(v1.object_id, q1.id)
        self.assertEqual(v1.content_type.name, 'question')
        self.assertEqual(v1.content_object, q1)
        q1 = Question.objects.get(pk=q1.pk) # CREAM
        self.assertEqual(q1.up_votes, 0)
        self.assertEqual(q1.down_votes, 3)


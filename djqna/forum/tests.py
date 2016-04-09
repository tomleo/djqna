from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import Question, Answer, Vote
from .views import questions, question, answers, answer


def make_users(n):
    return {
        'u%s' % i: User(first_name='fn%s' % i,
                        last_name='ln%s' % i,
                        username='fn%sln%s' % (i, i),
                        email='fn%s@ln%s.com' % (i, i)) for i in range(1, n+1)
    }


def save_users(user_dict):
    for user in user_dict.values():
        user.save()
    return user_dict


# Model Tests

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


class TestQuestions(TestCase):
    pass


# View Tests

class TestQuestionsView(TestCase):

    def test_questions(self):
        users = save_users(make_users(1))
        q1 = Question.objects.create(title='a', user=users['u1'], text='a')
        response = self.client.get(reverse('questions'))
        tmpl_questions = response.context['questions']
        self.assertSetEqual(set(tmpl_questions.values_list('pk', flat=True)),
                            set([q1.id]))


class TestQuestionView(TestCase):

    def test_question(self):
        users = save_users(make_users(1))
        q1 = Question.objects.create(title='a', user=users['u1'], text='a')
        response = self.client.get(reverse('question', kwargs={'question_id': q1.id}))
        tmpl_question = response.context['question']
        self.assertEqual(tmpl_question.id, q1.id)


class TestAnswersView(TestCase):

    def test_answers(self):
        users = save_users(make_users(2))
        q1 = Question.objects.create(title='a', user=users['u1'], text='a')
        a1 = Answer.objects.create(title='b', user=users['u2'], text='b', question=q1)
        response = self.client.get(reverse('answers', kwargs={'question_id': q1.id}))
        self.assertSetEqual(set(response.context['answers'].values_list('pk', flat=True)), set([a1.id]))


class TestAnswerView(TestCase):

    def test_answer(self):
        users = save_users(make_users(2))
        q1 = Question.objects.create(title='a', user=users['u1'], text='a')
        a1 = Answer.objects.create(title='b', user=users['u2'], text='b', question=q1)
        response = self.client.get(reverse('answer', kwargs={'answer_id': a1.id}))
        self.assertEqual(response.context['answer'].id, a1.id)

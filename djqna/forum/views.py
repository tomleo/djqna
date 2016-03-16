from django.shortcuts import render, get_object_or_404

from .models import Question, Answer

def questions(request):
    # TODO: add pagination
    _questions = Question.objects.all()
    context = {
        'questions': _questions
    }
    return render(request, 'forum/questions.html', context)

def question(request, question_id):
    _question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': _question,         
    }
    return render(request, 'forum/question.html', context)

def answers(request, question_id):
    # TODO: add pagination
    _answers = Answer.objects.all()
    context = {
        'answers': _answers
    }
    return render(request, 'forum/answers.html', context)

def answer(request, answer_id):
    _answer = get_object_or_404(Answer, pk=answer_id)
    context = {
            'answer': _answer
    }
    return render(request, 'forum/answer.html', context)


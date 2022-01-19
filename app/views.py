from django.shortcuts import render

# Create your views here.
from django.http import request
from django.core.paginator import Paginator
from .models import Tag, Profile, LikesForQuestion, Question, LikesForAnswer, Answer


# Help function
def paginate(objects, request, object_on_page=5):
    paginator = Paginator(objects, object_on_page)
    page = request.GET.get('page')
    return paginator.get_page(page)


def login(request):
    popular_tags = Tag.objects.popular()[:3]
    content = {
        'popular_tags': popular_tags,
    }
    return render(request, "html/login.html", content)


def new_question(request):
    return render(request, "html/new_question.html", {})


def question(request, id):
    popular_tags = Tag.objects.popular()[:5]
    question = Question.objects.get(id=id)
    answers = Answer.objects.get_answers(question)
    answers_by_page = paginate(answers, request)
    content = {
        'popular_tags': popular_tags,
        'question': question,
        'objects': answers_by_page
    }
    return render(request, "html/question.html", content)


def questions(request):
    popular_tags = Tag.objects.popular()[:5]
    questions = Question.objects.new()
    new_questions_per_page = paginate(questions, request)
    content = {
        'popular_tags': popular_tags,
        'objects': new_questions_per_page,
    }
    return render(request, "html/questions.html", context=content)


def hot(request):
    popular_tags = Tag.objects.popular()[:3]
    hot_questions = Question.objects.popular()
    hot_questions_per_page = paginate(hot_questions, request)
    content = {
        'popular_tags': popular_tags,
        'objects': hot_questions_per_page,
    }
    return render(request, "html/hot.html", context=content)


def reg(request):
    popular_tags = Tag.objects.popular()[:5]
    content = {
        'popular_tags': popular_tags,
    }
    return render(request, "html/registration.html", context=content)


def settings(request):
    popular_tags = Tag.objects.popular()[:5]
    content = {
        'popular_tags': popular_tags,
    }
    return render(request, "html/settings.html", context=content)


def tag(request, id):
    popular_tags = Tag.objects.popular()[:5]
    tag = Tag.objects.get(id=id)
    questions = Question.objects.tag(tag)
    questions_per_page = paginate(questions, request)
    content = {
        'tag': tag,
        'popular_tags': popular_tags,
        'questions_count': questions.count,
        'objects': questions_per_page
    }
    return render(request, "html/tag.html", content)


def wrong_new_question(request):
    popular_tags = Tag.objects.popular()[:10]
    content = {
        'popular_tags': popular_tags,
    }
    return render(request, "html/wrong_new_question.html", context=content)

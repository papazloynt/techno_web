from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator

questions_ = [
    {
        "title": f"Title {i}",
        "text": f"Text gen in {i}"
    } for i in range(100)
]

question_ = {
                "title": f"Title for question",
                "text": f"Text"
            }


questions_answer = [
    {
        "text": f"{i} answer on question"
    } for i in range(7)
]

# Help function
def paginate(request, objects):
    paginator = Paginator(objects, 5)
    page = request.GET.get('page')
    return paginator.get_page(page)


def login(request):
    return render(request, "html/login.html", {})


def new_question(request):
    return render(request, "html/new_question.html", {})


def question(request):
    return render(request, "html/question.html",
                  {'question': question_,
                   'objects': paginate(request, questions_answer)})


def questions(request):
    return render(request, "html/questions.html",
                  {'objects': paginate(request, questions_)})


def reg(request):
    return render(request, "html/registration.html", {})


def settings(request):
    return render(request, "html/settings.html", {})


def tag(request):
    return render(request, "html/tag.html",
                  {'questions': paginate(request, questions_)})


def wrong_new_question(request):
    return render(request, "html/wrong_new_question.html", {})

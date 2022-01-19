from django.shortcuts import render, redirect, reverse
from django.http import request
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction


from .models import Tag, Profile, LikesForQuestion, Question, LikesForAnswer, Answer
from app.forms import *



# Help function
def paginate(objects, request, object_on_page=5):
    paginator = Paginator(objects, object_on_page)
    page = request.GET.get('page')
    return paginator.get_page(page)

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


def question(request, id):
    try:
        question = Question.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request, "html/404_not_found.html")

    popular_tags = Tag.objects.popular()[:5]
    answers = Answer.objects.get_answers(question)
    answers_by_page = paginate(answers, request)

    if not request.user.is_authenticated:
        return render(request, "html/question.html", {
            'popular_tags': popular_tags,
            'question': question,
            'objects': answers_by_page
        })

    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.question = question
            answer.save()
            response = redirect(reverse("question", kwargs={'id': question.id}))
            response['Location'] += f'#ans{answer.id}'
            return response

    return render(request, "html/question.html", {
        'popular_tags': popular_tags,
        'question': question,
        'objects': answers_by_page,
        'form': form
    })


def tag(request, id):
    popular_tags = Tag.objects.popular()[:5]
    tag = Tag.objects.get(id=id)
    questions = Question.objects.tag(tag)
    questions_per_page = paginate(questions, request)
    content = {
        'tag': tag,
        'popular_tags': popular_tags,
        'objects': questions_per_page
    }
    return render(request, "html/tag.html", content)


@login_required
def new_question(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()
            tags = list(set(form.cleaned_data['tag'].split()))
            with transaction.atomic():
                tags_objects = [Tag.objects.get_or_create(tag_name=tag)[0] for tag in tags]
            question.tags.set(tags_objects)
            return redirect(reverse("question", kwargs={'id': question.id}))

    return render(request, "html/new_question.html", {'form': form})


def login(request):
    if request.method == 'GET':
        request.session['next_page'] = request.GET.get('next', '/')
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.session.pop('next_page', '/questions'))

    popular_tags = Tag.objects.popular()[:3]
    return render(request, 'html/login.html', {'form': form, 'popular_tags': popular_tags})


def logout(request):
    auth.logout(request)
    return redirect('/')


def reg(request):
    if request.method == 'GET':
        request.session['next_page'] = request.GET.get('next', '/')
        form = SignupForm()
    else:
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'])
            profile = Profile.objects.create(user=user)
            if form.cleaned_data['profile_pic'] is not None:
                profile.profile_pic = form.cleaned_data['profile_pic']
                profile.save()
            auth.login(request, user)
            return redirect(request.session.pop('next_page', '/questions'))

    popular_tags = Tag.objects.popular()[:5]
    return render(request, 'html/registration.html', {'form': form, 'popular_tags': popular_tags})


@login_required
def settings(request):
    if request.method == 'GET':
        form = EditForm(initial={"username": request.user.username})
    else:
        form = EditForm(request.POST, request.FILES, initial={"username": request.user.username})
        if form.is_valid():
            user = request.user
            profile = user.profile
            if 'username' in form.changed_data:
                user.username = form.cleaned_data['username']
            if 'profile_pic' in form.changed_data:
                profile.profile_pic = form.cleaned_data['profile_pic']
            profile.save()
            user.save()
    popular_tags = Tag.objects.popular()[:5]
    return render(request, 'settings.html', {'form': form, 'popular_tags': popular_tags})


def wrong_new_question(request):
    popular_tags = Tag.objects.popular()[:10]
    content = {
        'popular_tags': popular_tags,
    }
    return render(request, "html/wrong_new_question.html", context=content)

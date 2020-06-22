from .forms import *

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator


def paginate(objects, request, n):
    paginator = Paginator(objects, n)
    page = request.GET.get('page')
    objects_page = paginator.get_page(page)
    return objects_page


def show_questions(request):
    questions = Question.objects.new()
    return render(request, 'questions.html', {'questions': paginate(questions, request, 3)})


def show_hot(request):
    questions = Question.objects.top()
    return render(request, 'hot.html', {'questions': paginate(questions, request, 3)})


def show_tag(request, id):
    questions = Question.objects.tag(id)
    template = loader.get_template('tag.html')
    context = {
        'questions': paginate(questions, request, 4),
        'tag': Tag.objects.get(id=id)
    }
    return HttpResponse(template.render(context, request))


def show_base(request):
    return render(request, "base.html", {})


def show_ask(request):
    return render(request, "ask.html", {})


def show_question(request):
    return render(request, "question.html", {})


def show_settings(request):
    return render(request, "settings.html", {})


def show_login(request):
    return render(request, "login.html", {})


def show_register(request):
    return render(request, "register.html", {})


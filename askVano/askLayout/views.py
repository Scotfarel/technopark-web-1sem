from django.shortcuts import render
from django.http import HttpResponse


def show_questions(request):
    return render(request, "questions.html", {})


def show_base(request):
    return render(request, "base.html", {})


def show_ask(request):
    return render(request, "ask.html", {})


def show_question(request):
    return render(request, "question.html", {})


def show_tag(request):
    return render(request, "tag.html", {})


def show_settings(request):
    return render(request, "settings.html", {})


def show_login(request):
    return render(request, "login.html", {})


def show_register(request):
    return render(request, "register.html", {})

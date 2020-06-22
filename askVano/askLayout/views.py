from django.contrib.auth import logout, login, authenticate
from django.db import connection
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import permission_required, login_required
from django.template import loader
from .forms import *
from django.contrib import messages, auth


def paginate(objects, request, n):
    paginator = Paginator(objects, n)
    page = request.GET.get('page')
    objects_page = paginator.get_page(page)
    return objects_page


@login_required(login_url='login')
def show_ask(request):
    if (request.method == 'POST'):
        form = AskForm(data=request.POST)
        if form.is_valid:
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            for tag in form['tag_list'].data.split():
                new_tag = Tag.objects.get_or_create(name=tag)
                print(new_tag)
                question.tag.add(new_tag[0])
            question.save()
            return redirect('question', question.id)
    if (request.method == 'GET'):
        form = AskForm()
    return render(request, 'ask.html', {'form': form})


def show_index(request):
    questions = Question.objects.new()
    return render(request, 'index.html', {'questions': paginate(questions, request, 4)})
    pass


def show_my_questions(request):
    questions = Question.objects.my_question(id=request.user.id)
    return render(request, 'my_questions.html', {'questions': paginate(questions, request, 4)})
    pass


def show_hot(request):
    questions = Question.objects.top()
    return render(request, 'hot.html', {'questions': paginate(questions, request, 5)})


def show_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def fillErrors(formErrors, errors):
    for i in formErrors:
        formattedFieldName = i.replace('_', ' ')
        errors.append(f' {formattedFieldName} field error: {formErrors[i][0]}')


def show_registration(request):
    errors = []
    form = SignupForm
    if request.method == 'POST':
        form = form(request.POST)
        if request.POST['password'] != request.POST['password_confirmation']:
            errors.append('Passwords don\'t match')
        elif form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')
        else:
            fillErrors(form.errors, errors)
    else:
        logout(request)

    return render(request, 'register.html', {'form': form, 'messages': errors})


def show_question(request, id, page=1):
    if (request.method == 'POST'):
        form = AnswerForm(data=request.POST)
        if form.is_valid:
            answer = form.save(commit=False)
            answer.author = request.user
            answer.is_correct = 0
            answer.question = Question.objects.get(id=id)
            answer.save()
            paginator = Paginator(Answer.objects.answer(id), 3)
            return redirect('question', id, paginator.num_pages)
    if (request.method == 'GET'):
        form = AnswerForm()
        template = loader.get_template('question.html')
        answers = Answer.objects.answer(id)
        context = {'answers': paginate(answers, request, 3),
                   'question': Question.objects.get(id=id),
                   'form': form, }
        return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def show_settings(request):
    if (request.method == 'POST'):
        form = SettingsForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid:
            user = form.save(commit=False)
            user.save()
        return render(request, 'settings.html', {'form': form})
    if (request.method == 'GET'):
        form = SettingsForm(instance=request.user)
        return render(request, 'settings.html', {'form': form})


def show_tag(request, id):
    questions = Question.objects.tag(id)
    template = loader.get_template('tag.html')
    context = {
        'questions': paginate(questions, request, 4),
        'tag': Tag.objects.get(id=id)
    }
    return HttpResponse(template.render(context, request))


def show_logout(request):
    if not request.user.is_authenticated:
        raise Http404
    logout(request)
    return redirect('index')

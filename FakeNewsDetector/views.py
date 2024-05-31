import csv

from django.shortcuts import render, redirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from .forms import UserForm, AdminForm, NewsForm
from .models import User, Admin, News
from django.core.files.storage import FileSystemStorage
from textblob import TextBlob
import re
import nltk

name = ""


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})


def Login(request):
    if request.method == 'GET':
        return render(request, 'Login.html', {})


def UploadNews(request):
    if request.method == 'GET':
        return render(request, 'UploadNews.html', {})


#
# def AdminLogin(request):
#     if request.method == 'POST':
#         username = request.POST.get('t1', False)
#         password = request.POST.get('t2', False)
#         if username == 'sudeepthi' and password == 'myself':
#             context = {'data': 'welcome ' + username}
#             return render(request, 'AdminScreen.html', context)
#         else:
#             context = {'data': 'login failed'}
#             return render(request, 'Login.html', context)

def AdminLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        login = User.objects.filter(email=email, password=password)
        if login.exists():
            request.session['email'] = email
            return render(request, "AdminScreen.html", {"msg": "login sucess"})
        else:
            return render(request, "Login.html", {"msg": "invalid data"})
    return render(request, "Login.html", {})


def UploadNewsDocument(request):
    global name
    if request.method == 'POST' and request.FILES['t1']:
        output = ''
        myfile = request.FILES['t1']
        fs = FileSystemStorage()
        name = str(myfile)
        filename = fs.save(name, myfile)
        name = filename
        print("name = ", name)
        context = {'data': name + ' news document loaded'}
        return render(request, 'UploadNews.html', context)


def getQuotes(paragraph):  # checking paragraph contains quotes or not
    score = 0
    match = re.findall('(?:"(.*?)")', paragraph)
    if match:
        score = len(match)
    return score


def checkVerb(paragraph):  # checking paragraph contains verbs or not
    score = 0
    b = TextBlob(paragraph)
    list = b.tags
    for i in range(len(list)):
        arr = str(list[i]).split(",")
        verb = arr[1].strip();
        verb = verb[1:len(verb) - 2]
        if verb == 'VBG' or verb == 'VBN' or verb == 'VBP' or verb == 'VBD':
            score = score + 1
    return score


def nameEntities(paragraph):  # getting names from paragraphs
    score = 0
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(paragraph))):
        if hasattr(chunk, 'label'):
            name = ' '.join(c[0] for c in chunk)
            score = score + 1
    return score


def naiveBayes(quotes_score, verb_score, name, paragraph):  # Naive Bayes to calculate score
    score = quotes_score + verb_score + name
    arr = nltk.word_tokenize(paragraph)
    total = (score / len(arr) * 10)
    return total


def DetectorAlgorithm(request):  # detector and classifier algorithm
    global name
    if request.method == 'GET':
        strdata = '<table border=1 align=center width=100%><tr><th>News Text</th><th>Classifier Detection Result</th><th>Fake Rank Score</th></tr><tr>'
        with open(name, "r") as file:
            for line in file:
                line = line.strip('\n')
                line = line.strip()
                quotes_score = getQuotes(line)
                verb_score = checkVerb(line)
                entity_name = nameEntities(line)
                score = naiveBayes(quotes_score, verb_score, entity_name, line)
                if score > 0.90:
                    strdata += '<td>' + line + '</td><td>Real News</td><td>' + str(score) + '</td></tr>'
                else:
                    strdata += '<td>' + line + '</td><td>Fake News</td><td>' + str(score) + '</td></tr>'

    context = {'data': strdata}
    return render(request, 'ViewFakeNewsDetector.html', context)


def addnews(request):
    if request.method == 'POST':
        text_data = request.POST.get('text_data')
        with open('News custom.csv', 'a', newline='') as csvfile:
            fieldnames = ['text_data']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'text_data': text_data})
        return render(request, 'addnews.html', {"msg": "Data Stored Successfully"})
    return render(request, 'addnews.html', {})


# def ViewNews1(request):
#     if request.method == 'GET':
#         return render(request, 'ViewNews1.html', {})


def admin(request):
    if request.method == 'GET':
        return render(request, 'admin.html', {})


# def LoginAdmin(request):
#     if request.method == 'POST':
#         username = request.POST.get('t1', False)
#         password = request.POST.get('t2', False)
#         if username == 'admin' and password == 'admin':
#             context = {'data': 'welcome ' + username}
#             return render(request, 'AdminPage.html', context)
#         else:
#             context = {'data': 'login failed'}
#             return render(request, 'admin.html', context)


def LoginAdmin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        login = Admin.objects.filter(username=username, password=password)
        if login.exists():
            request.session['username'] = username
            return render(request, "AdminPage.html", {"msg": "login sucess"})
        else:
            return render(request, "admin.html", {"msg": "invalid data"})
    return render(request, "admin.html", {})


def ChngPassword(request):
    print("hii")
    if admin_is_login(request):
        print("hii1")
        if request.method == 'POST':
            print("hii2")
            username = request.session['username']
            password = request.POST['password']
            newpassword = request.POST['newpassword']
            try:
                form = Admin.objects.get(username=username, password=password)
                form.password = newpassword
                form.save()
                return render(request, 'admin.html', {"msg": "pwd update success"})
            except Exception as e:
                print(e)
                return render(request, 'ChngPassword.html', {"msg": "Not save"})
        return render(request, "ChngPassword.html", {})
    return render(request, "ChngPassword.html", {})


def admin_is_login(request):
    if request.session.__contains__('username'):
        return True
    else:
        return False


def userreg(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                return render(request, "userreg.html", {"msg": "This Email already exists"})
            else:
                form.save()
                return render(request, "Login.html", {"msg": "Registration successful"})
        return render(request, "userreg.html", {"msg": "Data saved"})
    return render(request, "userreg.html", {})


# views.py

import csv
from django.shortcuts import render


def ViewNews1(request):
    new = News.objects.all()
    return render(request, "ViewNews1.html", {"news": new})


def ViewNews(request):
    new = News.objects.all()
    return render(request, "ViewNews.html", {"news": new})


def addnews1(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            text_data = request.POST.get('description')
            with open('admin_news.csv', 'a', newline='') as csvfile:
                fieldnames = ['description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow({'description': text_data})
            form.save()
            return render(request, "addnews1.html", {"msg": "Data saved"})
        return render(request, "addnews1.html", {"msg": "Data not saved"})
    return render(request, "addnews1.html", {})


def edit_news(request, id):
    new = News.objects.get(id=id)
    return render(request, "update.html", {"x": new})


def update_news(request):
    if request.method == "POST":
        id = request.POST['id']
        users = News.objects.get(id=id)
        user = NewsForm(request.POST, request.FILES, instance=users)
        if user.is_valid():
            user.save()
            return redirect('/ViewNews1')
        return redirect('/ViewNews1')
# def update_news(request):
#     if request.method == "POST":
#         id = request.POST['id']
#         users = News.objects.get(id=id)
#         user = NewsForm(request.POST, request.FILES, instance=users)
#         if user.is_valid():
#             user.save()
#             return redirect('/ViewNews')
#         return redirect('/ViewNews')

def delete(request,id):
    dels = News.objects.get(id=id)
    dels.delete()
    return redirect('/ViewNews1')

def delete(request,id):
    dels = News.objects.get(id=id)
    dels.delete()
    return redirect('/ViewNews')

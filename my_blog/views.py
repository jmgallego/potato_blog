from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth import authenticate,login, logout
from django.views.decorators.csrf import csrf_exempt
from my_blog.models import Article,Blog
from my_blog.forms import ArticleForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse,HttpResponseRedirect 

import json

def home(request):
    blog=Blog.get_blog()
    login_form=AuthenticationForm()
    filters = blog.get_filters()
    if request.method =='POST':
        login_form=AuthenticationForm(data=request.POST)
        if login_form.is_valid(): 
            user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
    return render_to_response("home.html",{'login_form':login_form,'blog':blog, 'filters':filters},context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    blog=Blog.get_blog()
    login_form=AuthenticationForm()
    return render_to_response("home.html",{'login_form':login_form,'blog':blog},context_instance=RequestContext(request))

 
def do_article(request):
    form = ArticleForm()
    if request.method == 'POST': #update an article
        if 'id' in request.POST:
            article=Article.objects.get(id=request.POST['id'])
            form = ArticleForm(request.POST,instance=article)
        else: #save an article
            form = ArticleForm(request.POST)
        if form.is_valid():
            art=form.save()
        return HttpResponseRedirect("/")
    else:
        if 'art_id' in request.GET: #get an article form  with instance to update 
            art_id=request.GET['art_id']
            article=Article.objects.get(id=art_id)
            form = ArticleForm(instance=article)
        else: #get an article form without instance to save new one
            form = ArticleForm()
        return HttpResponse( render_to_string('article_form.html', {'form':form },context_instance=RequestContext(request)))

@csrf_exempt        
def delete_article(request):
    deleted = False
    if request.user.is_authenticated() and request.method == 'POST' and 'id_art' in request.POST:
       
        try:
            article = Article.objects.get(id=request.POST['id_art'])
            if article.blog.owner== request.user:
                article.delete()
                deleted = True
        except:
            pass
        
    return HttpResponse(deleted)

@csrf_exempt    
def pull_articles(request):
    articles = []
    if 'last_id' in request.POST.keys():
        for art in Blog.get_blog().get_articles_before(before_id=request.POST['last_id']):
            articles.append(art.to_dict())
    return HttpResponse(json.dumps({"authenticated":request.user.is_authenticated(),"articles":articles}))

@csrf_exempt    
def get_article(request):
    articles = []
    if 'id' in request.POST.keys():
        for art in Blog.get_blog().get_articles_before(before_id=int(request.POST['id'])+1, quantity=1):
            articles.append(art.to_dict())
    return HttpResponse(json.dumps({"authenticated":request.user.is_authenticated(),"articles":articles}))

from django.shortcuts import render, get_object_or_404,HttpResponseRedirect
from .models import Article, Comment, Poll, NewUser
from .forms import CommentForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from urllib.parse import urljoin
import markdown2


def log_in(request):
    error = 'password or username is not true'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            res = HttpResponseRedirect('/image/')
            res.set_cookie('username', username)
            return res
        else:
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')


def image(request):
    username = request.user
    user = NewUser.objects.all().order_by('last_login')
    poll_article = username.poll_set.all().count()
    user_list = [c.username for c in user]
    latest_list = Article.objectes.query_by_time()
    return render(request, 'image.html', {'name': username, 'latest_list': latest_list, 'user_list': user_list, 'poll_num': poll_article})


def register(request):
    error = 'this name is alreay exist'
    valid = 'this password is not valid'
    if request.method == 'POST':
        username = request.POST['username']
        userresult = NewUser.objects.filter(username=username)
        if len(userresult) > 0:
            return render(request, 'register.html', {'error': error})
        else:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                return render(request, 'register.html', {'valid': valid})
            else:
                email = request.POST['email']
                NewUser.objects.create_user(username=username, password=password1, email=email)
                return HttpResponseRedirect('/')
    return render(request, 'register.html')


@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def article_page(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    content = markdown2.markdown(article.content, extras=["code-friendly", "fenced-code-blocks", "header-ids", "toc", "metadata"])
    commentform = CommentForm()
    comments = article.comment_set.all()
    com_num = article.comment_set.all().count()
    username = request.user
    return render(request, 'image_page.html', {'article': article,
            'content': content, 'commentform': commentform,
            'comments': comments,'username': username, 'com_num': com_num})


@login_required
def comment(request, article_id):
    form = CommentForm(request.POST)
    url = urljoin('/image/', article_id)
    if form.is_valid():
        article = Article.objectes.get(id=article_id)
        new_comment = form.cleaned_data['comment']
        user = request.user
        Comment.objects.create(user=user, content=new_comment, article_id=article_id)
        article.comment_num += 1
        article.save()
    return HttpResponseRedirect(url)


@login_required
def keep(request, article_id):
    user = request.user
    article = get_object_or_404(Article, id=article_id)
    articles = user.article_set.all()
    if article not in articles:
        Article.objectes.create(title=article.title, author=user, column=article.column, image=article.image, content=article.content)
        article.keep_num += 1
        article.save()
        return HttpResponseRedirect('/image/')
    else:
        url = urljoin('/image/', article_id)
        return HttpResponseRedirect(url)


@login_required
def poll(request, article_id):
    user = request.user
    article = get_object_or_404(Article, id=article_id)
    polls = user.poll_set.all()
    articles = []
    for pol in polls:
        articles.append(pol.article)

    if article in articles:
        url = urljoin('/image/', article_id)
        return HttpResponseRedirect(url)
    else:
        article.poll_num += 1
        article.save()
        Poll.objects.create(user=user, article=article)
        return HttpResponseRedirect('/image/')


def post(request):
    form = PostForm()
    return render(request, 'post.html', {'form': form})


def post_image(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            column = form.cleaned_data['column']
            title = form.cleaned_data['title']
            imag = form.cleaned_data['image']
            content = form.cleaned_data['content']
            poll_num = form.cleaned_data['poll_num']
            keep_num = form.cleaned_data['keep_num']
            comment_num = form.cleaned_data['comment_num']
            author = form.cleaned_data['author']
            c = Article.objectes.create(column=column, title=title, author=author, image=imag,
                                   content=content, poll_num=poll_num, keep_num=keep_num,
                                   comment_num=comment_num)
            c.save()
        return HttpResponseRedirect('/image/')
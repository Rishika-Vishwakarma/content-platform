from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Article, Blog, Content, Comment, BlogComment, ContentComment
from .forms import ArticleForm, BlogForm, ContentForm
from .models import Profile
from django.contrib import messages
from .models import HireRequest
from .models import Chat, Message
from django.db.models import Count, Q
from django.db.models import Avg
from .models import (
    Article, Blog, Content,
    Comment, BlogComment, ContentComment,
    Review
)

# =========================
# HOME / AUTH
# =========================

def home(request):

    top_writers = Profile.objects.filter(
        role='writer'
    )

    writer_data = []

    for writer in top_writers:

        avg_rating = Review.objects.filter(
            writer=writer.user
        ).aggregate(Avg('rating'))['rating__avg']

        writer_data.append({
            'user': writer.user,
            'rating': round(avg_rating or 0, 1)
        })

    writer_data = sorted(
        writer_data,
        key=lambda x: x['rating'],
        reverse=True
    )[:3]

    return render(request, 'main/home.html', {
        'top_writers': writer_data
    })

def about(request):
    return render(request, 'main/about.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        role = request.POST['role']

        # 🔥 CHECK USER EXISTS
        if User.objects.filter(username=username).exists():
            return render(request, 'main/signup.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(username=username,email=email, password=password)
        Profile.objects.create(user=user, role=role, phone=phone)

        return redirect('/login/')

    return render(request, 'main/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 ADMIN
            if user.is_superuser:
                return redirect('/admin/')

            # 🔥 WRITER
            elif user.profile.role == 'writer':
                return redirect('portfolio')

            # 🔥 CLIENT → homepage या portfolio
            elif user.profile.role == 'client':
                return redirect('portfolio')   

            return redirect('/')

        else:
            return render(request, 'main/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'main/login.html')

def user_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')
# =========================
# CREATE POSTS
# =========================

@login_required
def article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('/portfolio/?tab=articles')
    else:
        form = ArticleForm()

    return render(request, 'main/article.html', {'form': form})


@login_required
def blog_view(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('/portfolio/?tab=blogs')
    else:
        form = BlogForm()

    return render(request, 'main/blog.html', {'form': form})


@login_required
def content_view(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.user = request.user
            content.save()
            return redirect('/portfolio/?tab=contents')
    else:
        form = ContentForm()

    return render(request, 'main/content.html', {'form': form})


# =========================
# PORTFOLIO
# =========================

def portfolio(request):

    query = request.GET.get('q')

    
    articles = Article.objects.all()
    blogs = Blog.objects.all()
    contents = Content.objects.all()

    
    if request.user.is_authenticated:

        if request.user.profile.role == 'writer':

            articles = Article.objects.filter(
                user=request.user
            )

            blogs = Blog.objects.filter(
                user=request.user
            )

            contents = Content.objects.filter(
                user=request.user
            )

    # 🔍 SEARCH
    if query:

        articles = articles.filter(
            title__icontains=query
        )

        blogs = blogs.filter(
            title__icontains=query
        )

        contents = contents.filter(
            title__icontains=query
        )

    return render(request, 'main/portfolio.html', {
        'articles': articles,
        'blogs': blogs,
        'contents': contents
    })

@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == 'POST':

        profile.bio = request.POST.get('bio')
        profile.skills = request.POST.get('skills')
        profile.experience = request.POST.get('experience')

        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES.get('profile_image')

        profile.save()

        return redirect('profile')

    return render(request, 'main/edit_profile.html', {
        'profile': profile
    })
# =========================
# LIKE
# =========================

def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.likes += 1
    article.save()
    return redirect('/portfolio/?tab=articles')


def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.likes += 1
    blog.save()
    return redirect('/portfolio/?tab=blogs')


def like_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    content.likes += 1
    content.save()
    return redirect('/portfolio/?tab=contents')


# =========================
# COMMENTS
# =========================

def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        text = request.POST['comment']
        Comment.objects.create(article=article, text=text)

    return JsonResponse({'success': True})

def add_blog_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        text = request.POST['comment']
        BlogComment.objects.create(blog=blog, text=text)

    return JsonResponse({'success': True})    


def add_content_comment(request, content_id):
    content = get_object_or_404(Content, id=content_id)

    if request.method == 'POST':
        text = request.POST['comment']
        ContentComment.objects.create(content=content, text=text)

    return JsonResponse({'success': True})
    


# =========================
# EDIT
# =========================

def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user != article.user:
        return redirect('/portfolio/?tab=articles')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('/portfolio/?tab=articles')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'main/article.html', {'form': form})


def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.user != blog.user:
        return redirect('/portfolio/?tab=blogs')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('/portfolio/?tab=blogs')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'main/blog.html', {'form': form})


def edit_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)

    if request.user != content.user:
        return redirect('/portfolio/?tab=contents')

    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            return redirect('/portfolio/?tab=contents')
    else:
        form = ContentForm(instance=content)

    return render(request, 'main/content.html', {'form': form})


# =========================
# DELETE
# =========================

def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user == article.user:
        article.delete()

    return redirect('/portfolio/?tab=articles')


def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.user == blog.user:
        blog.delete()

    return redirect('/portfolio/?tab=blogs')


def delete_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)

    if request.user == content.user:
        content.delete()

    return redirect('/portfolio/?tab=contents')


@login_required
def hire_writer(request, user_id):
    writer = User.objects.get(id=user_id)

    chat, created = Chat.objects.get_or_create(
        client=request.user,
        writer=writer
    )

    return redirect(f'/chat/{chat.id}/')   # 🔥 FINAL FIX

@login_required
def chat_page(request, chat_id):
    chat = Chat.objects.get(id=chat_id)

    # 🔥 unread messages ko read karo
    Message.objects.filter(
        chat=chat,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    messages = Message.objects.filter(chat=chat)

    return render(request, 'main/chat.html', {
        'chat': chat,
        'messages': messages
    })


def send_message(request, chat_id):
    if request.method == 'POST':
        text = request.POST.get('message')

        # 🔥 YAH ADD KARO
        if not text:
            return JsonResponse({'success': False})

        chat = Chat.objects.get(id=chat_id)

        msg = Message.objects.create(
            chat=chat,
            sender=request.user,
            text=text
        )

        return JsonResponse({
            'success': True,
            'message': msg.text
        })

    return JsonResponse({'success': False})

def get_messages(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    messages = chat.message_set.all().order_by('id')

    data = []
    for msg in messages:
        data.append({
            'text': msg.text,
            'sender': msg.sender.username
        })

    return JsonResponse({'messages': data})



@login_required
def inbox(request):
    chats = Chat.objects.filter(
        Q(client=request.user) | Q(writer=request.user)
    )

    chat_data = []

    for chat in chats:
        # last message
        last_msg = chat.message_set.order_by('-id').first()

        # unread count
        unread_count = chat.message_set.filter(
            is_read=False
        ).exclude(sender=request.user).count()

        # other user
        other_user = chat.writer if chat.client == request.user else chat.client

        chat_data.append({
            'chat_id': chat.id,
            'username': other_user.username,
            'last_message': last_msg.text if last_msg else "No messages yet",
            'unread': unread_count,
        })

    return render(request, 'main/inbox.html', {
        'chat_data': chat_data
    })


@login_required
def writer_requests(request):
    requests = HireRequest.objects.filter(writer=request.user)

    return render(request, 'main/requests.html', {
        'requests': requests
    })

@login_required
def handle_request(request, request_id, action):
    req = HireRequest.objects.get(id=request_id)

    if action == 'accept':
        req.status = 'accepted'

        # chat create
        chat, created = Chat.objects.get_or_create(
            client=req.client,
            writer=req.writer
        )

        req.save()
        return redirect('chat_page', chat.id)

    elif action == 'reject':
        req.status = 'rejected'
        req.save()

    return redirect('writer_requests')


@login_required
def add_review(request, writer_id):
    writer = User.objects.get(id=writer_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            writer=writer,
            client=request.user,
            rating=rating,
            comment=comment
        )

    return redirect('/writers/')

def writers_list(request):
    writers = Profile.objects.filter(role='writer')

    data = []

    for w in writers:
        avg = Review.objects.filter(writer=w.user).aggregate(Avg('rating'))['rating__avg']

        data.append({
            'user': w.user,
            'avg_rating': avg or 0
        })

    return render(request, 'main/writers.html', {'writers': data})
# views.py



@login_required
def profile(request):
    user = request.user
    profile = user.profile

    # posts count
    articles = Article.objects.filter(user=user)
    blogs = Blog.objects.filter(user=user)
    contents = Content.objects.filter(user=user)

    # reviews (agar writer hai)
    reviews = Review.objects.filter(writer=user)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    context = {
        'user': user,
        'profile': profile,
        'articles': articles,
        'blogs': blogs,
        'contents': contents,
        'reviews': reviews,
        'avg_rating': avg_rating or 0
    }

    return render(request, 'main/profile.html', context)

@login_required
def hired_writers(request):

    chats = Chat.objects.filter(client=request.user)

    return render(request,
                  'main/hired_writers.html',
                  {'chats': chats})
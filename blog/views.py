from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def home(request):
  blogs = Post.objects.filter(author = request.user)
  context = {
    'blogs' : blogs,
  }
  return render(request, 'home.html', context)

def registerPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if password1 != password2:
      return HttpResponse('Passwords do not match. Try again!')
    else:
      if User.objects.filter(username=username).exists():
        return HttpResponse("Username already taken!")
      else:
        user = User.objects.create_user(username, email, password1)
        return redirect('login')

    print(username, password1, email )
  return render(request, 'register.html')

def loginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password = password)
    if user:
      login(request, user)
      return redirect('home')
    else:
      return HttpResponse('Username or password is incorrect!')
    
  return render(request, 'login.html')

def logoutPage(request):
  logout(request)
  return redirect("login")

@login_required(login_url='login')
def post_form(request):
  if request.method == 'POST':
    title = request.POST.get('title')
    content = request.POST.get('content')

    post = Post(title=title, content=content, author=request.user)
    post.save()
    return redirect('home')
  return render(request, 'post_form.html')

@login_required(login_url='login')
def edit_form(request, id):
  blog = get_object_or_404(Post, id=id)
  if request.method == 'POST':
    title = request.POST.get('title')
    content = request.POST.get('content')
    blog.title = title
    blog.content = content
    blog.save()
    return redirect('home')
  return render(request, 'post_form.html', {'blog': blog})

@login_required(login_url='login')
def post_detail(request, id):
  blog = get_object_or_404(Post, id=id)
  context = {
    'blog':blog,
  }
  return render(request, 'post_detail.html', context)

@login_required(login_url='login')
def delete_post(request, id):
  blog = get_object_or_404(Post, id=id)
  blog.delete()
  
  return redirect('home')

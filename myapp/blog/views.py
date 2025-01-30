from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, Http404
from django.urls import reverse
import logging
from .models import Post,AboutUs
from django.core.paginator import Paginator
from .forms import ContactForm,RegisterForm,LoginForm,ForgotPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
#static demo data
# posts = [
#     {'id':1,'title':'Post 1', 'content':'Content of Post 1'},
#     {'id':2,'title':'Post 2', 'content':'Content of Post 2'},
#     {'id':3,'title':'Post 3', 'content':'Content of Post 3'},
#     {'id':4,'title':'Post 4', 'content':'Content of Post 4'},
# ]#we need to connect database to store these data

def index(request):
    # return HttpResponse("Hello world, You are at blog's index")
    blog_title = "Latest Posts"
    #getting data from post model
    all_posts = Post.objects.all()
    #we want use paginator
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request,'blog/index.html',{'blog_title':blog_title,'page_obj':page_obj})

def detail(request, slug):
    # return HttpResponse(f"You are viewing post detail page and ID is {post_id}")
    # static data
    # post = next((item for item in posts if item['id'] == int(post_id)),None)
    
    #getting data from model by post id
    try:
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)
        
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    
    # logger = logging.getLogger("TESTING")
    # logger.debug(f'post variable is {post}')
    return render(request,'blog/detail.html',{'post':post,'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))


def new_url_view(request):
    return HttpResponse("This is the new URL")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # form.cleaned_data['Name']
        logger = logging.getLogger("TESTING")
        if form.is_valid():
            #send email or save in database
            success_message = 'Your Email has been sent!'
            logger.debug("Form Validation success!")
            logger.debug(f'POST DATA is {form.cleaned_data['name']} \n{form.cleaned_data['email']}\n{form.cleaned_data['message']}')
            return render(request,'blog/contact.html',{'form':form, 'success_message':success_message})
        else:
            logger.debug("Form Validation failure!")  
        return render(request,'blog/contact.html',{'form':form, 'name':name, 'email':email, 'message':message})  
    return render(request,'blog/contact.html')

def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "No content available" #Default text
    else:
        about_content = about_content.content
    return render(request,'blog/about.html',{'about_content':about_content})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)#user data creating
            user.set_password(form.cleaned_data['password'])#set password as hash
            user.save()
            # print('Register success!')
            messages.success(request, 'Registration succesful. You can log in!')
            return redirect("blog:login")
        else:
            print('Register failure!')
    return render(request,'blog/register.html',{'form':form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        #login form 
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request,user)
                print("LOGIN SUCCESS!")
                return redirect("blog:dashboard")#redirect to dashboard 
        else:
            print("LOGIN FAILURE!")
        
    return render(request,'blog/login.html',{'form':form})


def dashboard(request):
    blog_title = "My Posts"
    return render(request,'blog/dashboard.html', {'blog_title':blog_title})



def logout(request):
    auth_logout(request)
    return redirect("blog:index")#redirect to home page 

def forgot_password(request):
    if request.method == 'POST':
        #form
        form =ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            #send email to reset password
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_side(request)#127.0.0.1:8000
            subject = "Reset Password Requested"
            message = 
            
            
    return render(request,'blog/forgot_password.html')

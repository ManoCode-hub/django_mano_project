from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, Http404
from django.urls import reverse
import logging
from .models import Post
from django.core.paginator import Paginator
from .forms import ContactForm
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

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # form.cleaned_data['Name']
        logger = logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f'POST DATA is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            #send email or save in database
            success_message = 'Your Email has been sent!'
            return render(request,'blog/contact.html',{'form':form, 'success_message':success_message})

        else:
            logger.debug("Form Validation failure!")
            
        return render(request,'blog/contact.html',{'form':form, 'name':name, 'email':email, 'message':message})
        
    return render(request,'blog/contact.html')

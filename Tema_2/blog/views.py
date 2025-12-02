from django.shortcuts import render
from .models import Post

def index(request):
    return render(request,'index.html',{})

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    return render(request,'blog/post_list.html',{"posts_mostrar":posts})
from django.contrib import admin
from my_blog.models import Blog
from my_blog.forms import BlogForm



class BlogAdmin(admin.ModelAdmin):
    form=BlogForm

admin.site.register(Blog,BlogAdmin)
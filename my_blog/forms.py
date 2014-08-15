from django.forms import ModelForm,ValidationError
from my_blog.models import Article,Blog

class BlogForm(ModelForm):
   
    class Meta:
       model=Blog
    
    def clean(self):
        
        """Controls that user cant make
        more than one blog instance"""
        
        cleaned_data = super(BlogForm, self).clean()
        blog = Blog.objects.all()[0]
        form_blog_id =  self.instance.id
        if blog:
            if not form_blog_id or form_blog_id != blog.id:
                raise ValidationError("You can't make more than one blog.")
        return cleaned_data
       
class ArticleForm(ModelForm):
   
    class Meta:
       model=Article
       exclude=('blog',)
        

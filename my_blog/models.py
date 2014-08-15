from django.db import models
from django.contrib.auth.models import User #AbstractUser
from django.conf import settings

    
class Blog(models.Model):
    
    title = models.CharField(max_length=124)
    description = models.TextField(max_length=124)
    owner = models.ForeignKey(User,related_name='blogs')
    created = models.DateTimeField(auto_now_add=True)
    
    """Singleton method"""
    @classmethod
    def get_blog(cls,**kwargs): 
        blog = None
        if cls.objects.count() < 1:
            if ['title','description','owner'] in kwargs.keys():
                blog = cls.objects.create(title=kwargs['title'],description=kwargs['description'],owner=kwargs['owner'])
        else:
            blog = cls.objects.all()[0]
        return blog
    
    def __unicode__(self):
        return u'Title: %s by %s'%(self.title,self.owner)

    def get_articles_before(self, before_id=None, quantity=3):
        if not before_id:
            before_id = Article.objects.latest('id').id + 1
        articles = Article.objects.filter(id__lt=before_id).order_by('-id')
        if articles:
            articles = articles[:quantity]
        else:
            articles = Article.objects.none()
        return articles
    
    def get_filters(self):
        months=['January', 'February','March','April','May','June','July',
                'August','September','October','November','December']
        filters = {}
        articles = Article.objects.order_by('-created')
        for article in articles:
            date = article.created
            year = date.year
            if not year in filters.keys():
                filters[year] = {}
            month = months[date.month-1]
            if not month in filters[year].keys():
                filters[year][month] = []    
            filters[year][month].append({'id':article.id, 'title':article.title})
        return filters
        

class Article(models.Model):
    
    title = models.CharField(max_length=124)
    content = models.TextField(max_length=124)
    created = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog,related_name='posts')
    
    def save(self, *args, **kwargs):
        _blog = Blog.get_blog()
        self.blog = _blog
        super(Article, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "content":self.content,
            "created":self.created.strftime(' %b. %d, %Y, %I:%M %P'),
            "blog": self.blog.id
        }
 
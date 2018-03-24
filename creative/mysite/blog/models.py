from django.db import models
from django.contrib import admin



# Create your models here.
class BlogsPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp')


admin.site.register(BlogsPost, BlogPostAdmin)



class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    essay=models.TextField(default='null')

class fiction(models.Model):
    name=models.TextField(primary_key=True)
    words=models.IntegerField()
    wordfre=models.TextField()
    sl=models.FloatField()
    wl=models.FloatField()
    RE=models.FloatField()
    TFIDF=models.TextField()
    reArticle=models.TextField()

class history(models.Model):
    user=models.TextField()
    readinglist=models.TextField()
    score=models.TextField()

class word(models.Model):
    name=models.TextField()
    words = models.TextField()
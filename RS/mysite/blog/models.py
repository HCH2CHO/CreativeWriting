from django.db import models
#
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

#KGRS
class UserClass(models.Model):
    userId = models.TextField(primary_key=True)
    user_Recommand = models.TextField()
    user_History = models.TextField()

class MovieClass(models.Model):
    movieId = models.TextField(primary_key=True)
    movie_info = models.TextField(max_length=1000)
    movie_src = models.TextField()
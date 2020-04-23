from django.db import models
from django.contrib.auth.models import AbstractUser


class PostManager(models.Manager):
    def best_posts(self):
        return self.filter()

    def top(self):
        return self.filter()

    def answer(self):
        return self.filter()


class User(AbstractUser):
    nickname = models.CharField(20)
    rating = models.IntegerField(default=0)
    avatar = models.ImageField(
        upload_to='avatar/',
        default='avatar/Vano.jpg'
    )


class Tag(models.Model):
    name = models.CharField(20)


class Question(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    objects = PostManager()


class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    objects = PostManager()


class Like(models.Model):
    pass

from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Sum, ImageField
from django.shortcuts import get_object_or_404


class ModelManager(models.Manager):
    def init(self):
        self.qs = self.get_queryset()
        return self

    def get_query(self):
        return self.qs

    def with_answers_count(self):
        return self.annotate(answers_count=Count('answer__id', distinct=True))

    def top(self):
        return self.init().order_by('-rate')

    def tag(self, id):
        tags = get_object_or_404(Tag, pk=int(id))
        return self.filter(tags__id=tags.id)

    def my_question(self, id):
        return self.filter(author__id=id)

    def answer(self, id):
        question = get_object_or_404(Question, pk=int(id))
        return self.filter(question__id=question.id)

    def new(self):
        return self.order_by()[::-1]

    def sum_for_question(self, q):
        res = self.self.filter(question=q).aggregate(sum=Sum('value'))['sum']
        return res if res else 0

    def add_or_update(self, owner, question, value):
        obj, new = self.update_or_create(
            owner=owner,
            question=question,
            defaults={'value': value}
        )

        question.rate = self.sum_for_question(question)
        question.save()
        return new


class Tag(models.Model):
    name = models.CharField(max_length=200)


class Profile(AbstractUser):
    nickname = models.CharField(max_length=200)
    avatar_path = models.ImageField(upload_to='avatars', default='cat_wanna_know.jpg')

    class Meta:
        verbose_name = 'Profile'

    def get_avatar(self):
        return str(self.avatar_path)


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = ((DISLIKE, 'Не нравится'), (LIKE, 'Нравится'))

    vote = models.SmallIntegerField(choices=VOTES)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = ModelManager()

    def save(self, *args, **kwargs):
        self.content_object.like(self)
        super(LikeDislike, self).save(*args, **kwargs)

    # class Meta:
    #     unique_together = (('author', 'content_type', 'object_id'),)


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    likes = GenericRelation(LikeDislike, related_query_name='questions')
    rate = models.IntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    objects = ModelManager()

    def like(self, like_object):
        if like_object not in LikeDislike.objects.all():
            self.likes_count += 1
            self.save()


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    likes = GenericRelation(LikeDislike, related_query_name='answers')
    is_correct = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)
    objects = ModelManager()
    likes_count = models.PositiveIntegerField(default=0)

    def like(self, like_object):
        if like_object not in LikeDislike.objects.all():
            self.rate += 1
            self.save()

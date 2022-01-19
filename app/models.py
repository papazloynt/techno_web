from django.contrib.auth.models import User
from django.db import models
import datetime


class TagManager(models.Manager):
    def popular(self):
        return self.order_by('-rating')


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    rating = models.IntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    image = models.ImageField(upload_to="uploads/avatars/", default="../static/img/200.jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'login: ' + self.user.username + ', email: ' + self.user.email


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-date')

    def popular(self):
        return self.order_by('-rating')

    def tag(self, tag):
        return self.select_related().filter(tags=tag.id).order_by('-rating')


class Question(models.Model):
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="question")
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True)
    name = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateField(auto_now=False, auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return self.name


class LikesForQuestion(models.Model):
    LIKE = 1
    DISLIKE = -1
    LIKES_CHOICES = [
        (LIKE, "like"),
        (DISLIKE, "dislike")
    ]

    likes = models.IntegerField(choices=LIKES_CHOICES)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('author', 'question')

    def __str__(self):
        return self.author.user.username + " reputation: " + str(
            self.likes) + "on question: " + self.question.name

    def update_rating(self):
        self.question.rating += self.likes


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.select_related().filter(question=question.id).order_by('-rating')


class Answer(models.Model):
    rating = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField()
    date = models.DateField(auto_now=False, auto_now_add=True)

    objects = AnswerManager()

    def __str__(self):
        return self.author.user.username + " answered to the question: " + self.question.name


class LikesForAnswer(models.Model):
    LIKE = 1
    DISLIKE = -1
    LIKES_CHOICES = [
        (LIKE, "like"),
        (DISLIKE, "dislike")
    ]

    likes = models.IntegerField(choices=LIKES_CHOICES)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('author', 'answer')

    def update_rating(self):
        self.answer.rating += self.likes

    def __str__(self):
        return self.author.user.username + " reputation: " + str(
            self.likes) + "on answer to the question: " + self.answer.question.name
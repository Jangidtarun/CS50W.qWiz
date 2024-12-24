from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    photo = models.ImageField(upload_to='photos/', default='key.png')
    about = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        # Delete the photo file if it exists and is not the default profile picture
        if self.photo and self.photo.url != settings.MEDIA_URL + 'key.png':
            self.photo.delete(save=False)
        super().delete(*args, **kwargs)


class Topic(models.Model):
    """
    This model represents a tag that users can associate with a question for the purpose of categorizing it
    """
    name = models.CharField(max_length=50, unique=True, blank=False)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def count_by_user(user):
        return Topic.objects.filter(created_by=user).count()

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    """
    This model represents a question created by user
    """

    body = models.CharField(max_length=500, blank=False)
    points = models.PositiveIntegerField(default=2)
    created_by = models.ForeignKey(User, models.CASCADE, related_name='questions_by')
    topics = models.ManyToManyField(Topic)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.body[:40]


class Vote(models.Model):
    """
    This model represents a vote (either upvote or downvote) made by a user on a particular question
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    voteval = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'vote #{self.pk}'


class View(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='views')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uviews')

  def __str__(self) -> str:
    return f'view by user #{self.user.pk} to question #{self.question.pk}'


class Choice(models.Model):
    """
    This model represents an mcq answer associated with a question
    """
    body = models.CharField(max_length=500, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.body[:40]


class Quiz(models.Model):
    """
    This model represents a quiz that is created automatically when user attempts to give a quiz
    """

    questions = models.ManyToManyField(Question)
    is_finished = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)


class Result(models.Model):
    """
    This model represents the result of a quiz that user will attempt
    """

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='result')
    questions = models.ManyToManyField(Question, related_name='tresult')
    obtained_score = models.IntegerField(default=0)
    total_score = models.PositiveIntegerField(default=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.obtained_score}/{self.total_score}'


class UserAnswer(models.Model):
    """
    This model represents the Answer that user selected for a question at the time of quiz
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_ans')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='user_answers')
    selected_option = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'#{self.pk}'


class Comment(models.Model):
    """
    This model represents a comment made by user on a particular question
    """
    body = models.CharField(max_length=500, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='qcomments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[:40]
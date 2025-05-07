from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404


class TagManager(models.Manager):
    def get_top(self):
        return (
            self.get_queryset()
            .annotate(count=Count('questions'))
            .order_by('-count')
            [:7]
        )
    
    def get_all(self):
        return self.get_queryset().values_list('tag', flat=True)

    def get(self, tag_id):
        return get_object_or_404(Tag, pk=tag_id)


class QuestionManager(models.Manager):
    def get_by_tag(self, tag_id):
        return self.filter(tags=tag_id)
    
    def get_by_user(self, user_id):
        return self.filter(author=user_id)
    
    def get_hot(self):
        return (
            self.get_queryset()
            .annotate(count=Count('answers'))
            .order_by('-count')
            [:100]
        )
    
    def get(self, question_id):
        return get_object_or_404(Question, pk=question_id)


class ProfileManager(models.Manager):
    def get_top(self):
        return (
            User.objects
            .annotate(count=Count('answers'))
            .order_by('-count')
            [:5]
        )
    
    def exist(self, login):
        return User.objects.filter(username=login).exists()


class Tag(models.Model):
    tag = models.CharField(max_length=255)
    # questions
    objects = TagManager()


class Question(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    tags = models.ManyToManyField(
        Tag, 
        related_name="questions"
    )
    score = models.ManyToManyField(
        User, 
        through="app.QuestionLike", 
        related_name="questionliked"
    )

    objects = QuestionManager()

    def get_likes(self):
        likes = QuestionLike.objects.filter(type=True, question=self).count()
        dislikes = QuestionLike.objects.filter(type=False, question=self).count()
        return likes - dislikes
    
    class Meta:
        ordering = ['-created_at']


class AnswerManager(models.Manager):
    def get_by_question(self, question):
        return self.filter(question=question)
    
    def get_amount(self, question):
        return Answer.objects.filter(question=question).count()


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="answers"
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name="answers"
    )
    is_checked = models.BooleanField()
    score = models.ManyToManyField(
        User, 
        through="app.AnswerLike", 
        related_name="answerliked"
    )

    objects = AnswerManager()

    def get_likes(self):
        likes = AnswerLike.objects.filter(type=True, answer=self).count()
        dislikes = AnswerLike.objects.filter(type=False, answer=self).count()
        return likes - dislikes
    
    class Meta:
        ordering = ['-created_at']


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    type = models.BooleanField()

    class Meta:
        unique_together = ["user", "answer"]


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    type = models.BooleanField()

    class Meta:
        unique_together = ["user", "question"]


class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    avatar = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, default='')

    objects = ProfileManager()

    def questions_num(self):
        return Question.objects.filter(author=self.user).count()

    def answers_num(self):
        return Answer.objects.filter(author=self.user).count()
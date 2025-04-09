from django.core.management.base import BaseCommand
from app.models import Tag, Profile, Question, Answer, AnswerLike, QuestionLike
from django.contrib.auth.models import User
from django.apps import apps
from app import models
from django.conf import settings
import csv
import random


names_path = settings.BASE_DIR / "users.csv"
names_len = 1000
names = []
tandt_path = settings.BASE_DIR / "titlesandtexts.csv"
tandt_len = 200
tandt = []

def clear_database():
    
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        admin_user = None
    
    all_models = apps.get_models()
    
    for model in all_models:
        if model == User:
            if admin_user:
                User.objects.exclude(pk=admin_user.pk).delete()
            else:
                User.objects.all().delete()
        else:
            model.objects.all().delete()
    

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        len1 = ratio * 10
        len2 = ratio * 100

        clear_database()

        with open(names_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                names.append(row[0])

        with open(tandt_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                tandt.append(row)

        users = [User(username=(names[i%names_len] + str(i)), email='email@gmail.com', password='pass1234') for i in range(ratio)]
        User.objects.bulk_create(users)

        profiles = []
        for user in users:  
            profiles.append(Profile(avatar='/img/avatar.jpg', user=user))
        Profile.objects.bulk_create(profiles)

        self.stdout.write("Added users")

        tags = [Tag(tag=i) for i in range(ratio)]
        Tag.objects.bulk_create(tags)

        self.stdout.write("Added tags")

        questions = []
        for i in range(len1):
            question = Question(title=tandt[i%tandt_len][0], text=tandt[i%tandt_len][1], author=users[random.randint(0, ratio - 1)])
            questions.append(question)
        created_questions = Question.objects.bulk_create(questions)

        for question in created_questions:
            question.tags.set(random.sample(list(tags), min(3, len(tags))))

        self.stdout.write("Added questions")

        answers = []
        for i in range(len2):
            answers.append(Answer(text=tandt[i%tandt_len][1], author=users[i % len(users)], question=questions[random.randint(0, len1  - 1)], is_checked = False))
        Answer.objects.bulk_create(answers)

        self.stdout.write("Added answers")

        i = 0
        questionlikes = []
        used = set()
        while i < len2:
            user_id = random.randint(0, ratio - 1)
            question_id = random.randint(0, len1 - 1)
            if (user_id, question_id) not in used:
                questionlike = QuestionLike(
                    user=users[user_id],
                    question=questions[question_id],
                    type=bool(random.randint(0, 1)),
                )
                questionlikes.append(questionlike)
                used.add((user_id, question_id))
                i += 1
        
        self.stdout.write("Added questionlikes")

        i = 0
        answerlikes = []
        used = set()
        while i < len2:
            user_id = random.randint(0, ratio - 1)
            answer_id = random.randint(0, len2 - 1)
            if (user_id, answer_id) not in used:
                answerlike = AnswerLike(
                    user=users[user_id],
                    answer=answers[answer_id],
                    type=bool(random.randint(0, 1)),
                )
                answerlikes.append(answerlike)
                used.add((user_id, answer_id))
                i += 1;


        models.QuestionLike.objects.bulk_create(questionlikes)
        models.AnswerLike.objects.bulk_create(answerlikes)

        self.stdout.write("Added answerlikes")
        self.stdout.write("ok")
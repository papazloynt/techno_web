from django.core.management.base import BaseCommand
from app.models import Tag, Profile, LikesForQuestion, Question, LikesForAnswer, Answer, User
from random import choice, sample, randint


class Command(BaseCommand):
    def _create_all(self):
        # ~~~~~~~~~~~~~~~~~  tags ~~~~~~~~~~~~~~~~~
        tags_to_create = [
            Tag(
                name=f"tag #{i}"
            ) for i in range(1, 1100)
        ]
        Tag.objects.bulk_create(tags_to_create)
        # ~~~~~~~~~~~~~~~~~  users ~~~~~~~~~~~~~~~~~
        users_to_create = [
            User(
                username=f"user #{i}",
                first_name=f"name {i}",
                last_name=f"lastname {i}",
                password=f"{i}a{i // 10}Mty{i // 100}Q",
                email=f"email_of_user{i}@mail.com"
            ) for i in range(1, 1100)
        ]
        User.objects.bulk_create(users_to_create)
        # ~~~~~~~~~~~~~~~~~  profiles ~~~~~~~~~~~~~~~~~
        profiles_to_create = [
            Profile(
                image=f"../../static/img/200.jpg",
                user_id=i
            ) for i in range(1, 1100)
        ]
        Profile.objects.bulk_create(profiles_to_create)
        # ~~~~~~~~~~~~~~~~~  questions ~~~~~~~~~~~~~~~~~
        author_ids = Profile.objects.values_list('id', flat=True)

        questions_to_create = [
            Question(
                author_id=choice(author_ids),
                name=f"Question name {i}",
                text=f"Some text for {i} question"
            ) for i in range(1, 1100)
        ]

        Question.objects.bulk_create(questions_to_create)

        tags_ids = list(Tag.objects.values_list('id', flat=True))
        questions_ids = Question.objects.values_list('id', flat=True)

        tags_questions_rels = []

        for question_id in questions_ids:
            for tag_id in sample(tags_ids, k=randint(1, 5)):
                tags_questions_rels.append(Question.tags.through(tag_id=tag_id, question_id=question_id))
        Question.tags.through.objects.bulk_create(tags_questions_rels, batch_size=10000)

        for tag in Tag.objects.all():
            tag.rating = Question.objects.tag(tag).count()
            tag.save()

        # ~~~~~~~~~~~~~~~~~  answers ~~~~~~~~~~~~~~~~~
        question_ids = Question.objects.values_list('id', flat=True)

        answers_to_create = [
            Answer(
                question_id=choice(question_ids),
                author_id=choice(author_ids),
                text=f"Some text for {i}answer"
            ) for i in range(1, 10010)
        ]
        Answer.objects.bulk_create(answers_to_create)
        # ~~~~~~~~~~~~~~~~~  likes for questions ~~~~~~~~~~~~~~~~~
        likes4question_to_create = [
            LikesForQuestion(
                likes=choice([-1, 1]),
                author_id=i // 200 + 1,
                question_id=i % 1100 + 1
            ) for i in range(2000)
        ]
        LikesForQuestion.objects.bulk_create(likes4question_to_create, batch_size=1000)

        for question in Question.objects.all():
            likes_sum = sum(list(LikesForQuestion.objects.filter(question=question).values_list('likes', flat=True)))
            question.rating = likes_sum
            question.save()

        # ~~~~~~~~~~~~~~~~~  likes for answers ~~~~~~~~~~~~~~~~~
        answer_ids = Answer.objects.values_list('id', flat=True)
        likes4answer_to_create = [
            LikesForAnswer(
                likes=choice([-1, 1]),
                author_id=i // 100 + 1,
                answer_id=i % 1000 + 1
            ) for i in range(1000)
        ]
        LikesForAnswer.objects.bulk_create(likes4answer_to_create, batch_size=1000)

        for answer in Answer.objects.all():
            likes_sum = sum(list(LikesForAnswer.objects.filter(answer=answer).values_list('likes', flat=True)))
            answer.rating = likes_sum
            answer.save()

    def handle(self, *args, **options):
        self._create_all()
from askLayout.models import Question, Tag, Profile, Answer, LikeDislike

import random

from faker import Faker
from django.core.management.base import BaseCommand

USER_COUNT = 10
TAG_COUNT = 10
QUESTION_COUNT = 10
ANSWER_COUNT = 200


def create_tags():
    tags = []
    faker = Faker()
    for i in range(TAG_COUNT):
        tag = Tag(name=faker.word() + str(i))
        tags.append(tag)

    Tag.objects.bulk_create(tags, batch_size=500)


def create_profiles():
    profiles = []
    faker = Faker()
    for i in range(USER_COUNT):
        profile = Profile(username=faker.user_name(),
                          email=faker.email(),
                          nickname=faker.user_name(),
                          avatar_path="https://gamepedia.cursecdn.com/stalker_ru_gamepedia/thumb/f/f5/Vano_face.jpg"
                                      "/300px-Vano_face.jpg?version=76de5b552f817c469f5f7a1d5dee6c6e")
        profile.set_password(faker.word())
        profiles.append(profile)

    Profile.objects.bulk_create(profiles)


def create_questions(profiles, tags):
    questions = []
    faker = Faker()
    for _ in range(QUESTION_COUNT):
        question = Question(title=faker.sentence()[:random.randint(20, 100)],
                            text=faker.text(),
                            author=random.choice(profiles))
        questions.append(question)

    Question.objects.bulk_create(questions, batch_size=500)


def create_answers(profiles, questions):
    answers = []
    faker = Faker()
    for _ in range(ANSWER_COUNT):
        answer = Answer(author=random.choice(profiles),
                        question=random.choice(questions),
                        text=faker.text(),
                        is_correct=False)
        answers.append(answer)

    Answer.objects.bulk_create(answers, batch_size=500)


def add_tag_question_relations(questions, tags):
    for question in questions:
        tags_for_questions = []
        for _ in range(random.randint(1, 3)):
            tag = random.choice(tags)
            if tag.pk not in tags_for_questions:
                tags_for_questions.append(tag.pk)
        question.tags.add(*tags_for_questions)


def create_likes(questions, answers, profiles):
    likes = []
    for p in profiles:
        for q in questions:
            if random.randint(0, 1) == 1:
                que = random.choice(questions)
                like = LikeDislike(content_object=Question.objects.get(id=que.id),
                                   object_id=que.id,
                                   vote=1,
                                   author=random.choice(profiles))
                likes.append(like)
                que.likes_count += 1
                que.rate += 1

            if random.randint(0, 1) == 1:
                que = random.choice(questions)
                like = LikeDislike(content_object=Question.objects.get(id=que.id),
                                   vote=-1,
                                   author=random.choice(profiles))
                likes.append(like)
                que.likes_count += 1
                que.rate -= 1

        for a in answers:
            if random.randint(0, 1) == 1:
                ans = random.choice(answers)
                like = LikeDislike(content_object=Answer.objects.get(id=ans.id),
                                   vote=1,
                                   author=random.choice(profiles))
                likes.append(like)
                ans.likes_count += 1
                ans.rate += 1

            if random.randint(0, 1) == 1:
                ans = random.choice(answers)
                like = LikeDislike(content_object=Answer.objects.get(id=ans.id),
                                   vote=-1,
                                   author=random.choice(profiles))
                likes.append(like)
                ans.likes_count += 1
                ans.rate -= 1

    Question.objects.bulk_update(questions, ['rate', 'likes_count'])
    Answer.objects.bulk_update(answers, ['rate', 'likes_count'])
    LikeDislike.objects.bulk_create(likes, batch_size=500)
    LikeDislike.objects.bulk_create(likes, batch_size=500)


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_tags()
        create_profiles()
        tags = Tag.objects.all()
        profiles = Profile.objects.all()
        create_questions(profiles, tags)
        questions = Question.objects.all()
        add_tag_question_relations(questions=questions, tags=tags)
        create_answers(profiles, questions)
        answers = Answer.objects.all()
        create_likes(questions=questions, answers=answers, profiles=profiles)

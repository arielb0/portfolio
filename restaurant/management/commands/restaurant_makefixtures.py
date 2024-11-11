from django.core.management.base import BaseCommand
from restaurant.models import Answer
from scull_suite.settings import BASE_DIR
from django.core.serializers import serialize

class Command(BaseCommand):
    requires_migrations_checks = True
    help = 'Generates fixtures that contains default answers'

    def handle(self, *args, **options):

        DEFAULT_BODY = 'Answer by default. You need to write your own answers.'
        answers = []

        for topic_number in range(0, 19):
            answers.append(Answer(body = DEFAULT_BODY, topic = topic_number))

        Answer.objects.bulk_create(objs = answers)

        serialized_answers = serialize(format = 'json', queryset=Answer.objects.all())

        with open(f'{BASE_DIR}/restaurant/fixtures/restaurant/answers.json', 'w') as answer_fixture:
            answer_fixture.write(serialized_answers)

        self.stdout.write(self.style.SUCCESS('Restaurant answer fixtures are generated successfully.'))
from django.core.cache import cache
from django.core.management import BaseCommand
from app.models import Tag, Profile

class Command(BaseCommand):
    def handle(self, *args, **options):
        popular_tags = Tag.objects.get_top()
        popular_users = Profile.objects.get_top()
        cache.set('popular_tags', popular_tags, 60)
        cache.set('popular_users', popular_users, 60)
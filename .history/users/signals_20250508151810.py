from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            name='이름없음',
            birth_date='2000-01-01',
            gender='미정',
            sexual_orientation='미정',
            communication_styles=[],
            latitude=0.0,
            longitude=0.0,
            match_distance_km=5,
        )

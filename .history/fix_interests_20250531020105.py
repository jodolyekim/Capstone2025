# fix_interests.py

import os
import django

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # config.settings는 settings.py 위치에 맞게 변경하세요
django.setup()

from users.models import Profile
from interest.models import Interest

def fix_profile_interests():
    for profile in Profile.objects.all():
        interest_ids = Interest.objects.filter(user=profile.user).values_list('id', flat=True)
        profile.interests.set(interest_ids)
        profile.save()
        print(f"✔️ {profile.user.email} → {profile.interests.count()}개 관심사 연결 완료")

if __name__ == "__main__":
    fix_profile_interests()

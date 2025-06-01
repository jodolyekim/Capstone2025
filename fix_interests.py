import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

# 아래에 기존 코드 작성
from users.models import Profile
from interest.models import Interest

def fix_profile_interests():
    for profile in Profile.objects.all():
        interest_ids = profile.interests.values_list('id', flat=True)
        valid_interest_ids = Interest.objects.filter(id__in=interest_ids, user=profile.user).values_list('id', flat=True)
        profile.interests.set(valid_interest_ids)
        profile.save()
        print(f"✔️ {profile.user.email} → {len(valid_interest_ids)}개 관심사 연결 완료")

if __name__ == "__main__":
    fix_profile_interests()

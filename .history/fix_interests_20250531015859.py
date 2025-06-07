import os
import django

# 프로젝트의 settings.py 모듈 경로로 바꿔주세요.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  

django.setup()

from users.models import Profile
from interest.models import Interest

def run():
    for profile in Profile.objects.all():
        user_interest_ids = profile.interests.values_list('id', flat=True)
        valid_interest_ids = Interest.objects.filter(id__in=user_interest_ids).values_list('id', flat=True)

        profile.interests.set(valid_interest_ids)
        print(f"✔️ {profile.user.email} → {len(valid_interest_ids)}개 연결 완료")

if __name__ == "__main__":
    run()

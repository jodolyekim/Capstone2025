import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # settings 경로 확인 필요
django.setup()

from users.models import Profile
from interest.models import Interest

def fix_profile_interests():
    for profile in Profile.objects.all():
        # 현재 profile.interests에 있는 Interest id들 가져오기
        current_interest_ids = profile.interests.values_list('id', flat=True)

        # Interest 중 실제 DB에 존재하는 id만 필터링
        valid_interest_ids = Interest.objects.filter(id__in=current_interest_ids).values_list('id', flat=True)

        # 기존 연결 모두 삭제
        profile.interests.clear()

        # 유효한 Interest만 재연결
        profile.interests.add(*valid_interest_ids)
        profile.save()
        print(f"✔️ {profile.user.email} → {profile.interests.count()}개 관심사 연결 완료")

if __name__ == "__main__":
    fix_profile_interests()

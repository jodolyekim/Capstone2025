from users.models import Profile
from interest.models import Interest

for profile in Profile.objects.all():
    # 현재 Profile.interests에 연결된 Interest id들을 가져옴
    interest_ids = profile.interests.values_list('id', flat=True)

    # 실제 Interest 테이블에 존재하고, user가 profile.user인 관심사 ID만 필터링
    valid_interest_ids = Interest.objects.filter(id__in=interest_ids, user=profile.user).values_list('id', flat=True)

    # M2M을 클린업된 valid_interest_ids로 교체
    profile.interests.set(valid_interest_ids)
    profile.save()

    print(f"✔️ {profile.user.email} → {len(valid_interest_ids)}개 관심사 연결 완료")

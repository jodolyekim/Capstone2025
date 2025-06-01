from math import radians, sin, cos, asin, sqrt
from django.utils import timezone
from users.models import Profile
from matching.models import Match  # ✅ 수정된 import

# 거리 계산 함수 (하버사인)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 지구 반지름 (km)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# 성별 조건 일치 여부 판단
def matches_pref(gender, preference, target_gender):
    if preference == '이성을 만나고 싶어요':
        return gender != target_gender
    elif preference == '동성을 만나고 싶어요':
        return gender == target_gender
    elif preference == '모두 만나고 싶어요':
        return True
    return False

# 두 프로필이 서로 조건에 부합하는지 여부
def is_mutually_acceptable(user1, user2):
    return (
        matches_pref(user1._gender, user1._sex_orientation, user2._gender) and
        matches_pref(user2._gender, user2._sex_orientation, user1._gender)
    )

# 후보 목록 필터링
def get_gender_match_candidates(user_profile):
    all_profiles = Profile.objects.exclude(id=user_profile.id)
    return [profile for profile in all_profiles if is_mutually_acceptable(user_profile, profile)]

# Match 생성 유틸 함수
def create_match(user_a, user_b, matched_keywords=None):
    if user_a == user_b:
        raise ValueError("자기 자신과 매칭할 수 없습니다.")
    user1, user2 = sorted([user_a, user_b], key=lambda u: u.id)
    matched_keywords = matched_keywords or []

    match, created = Match.objects.get_or_create(
        user1=user1,
        user2=user2,
        defaults={
            'matched_keywords': matched_keywords,
            'status_user1': 'pending',
            'status_user2': 'pending',
            'requested_at': timezone.now()
        }
    )
    return match, created

# 매칭 응답 문자열 매핑
MAPPING = {
    '승낙': 'accepted',
    '거절': 'rejected',
    'accept': 'accepted',
    'reject': 'rejected',
}

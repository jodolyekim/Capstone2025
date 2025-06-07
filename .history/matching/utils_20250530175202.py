# matching/utils.py

from math import radians, sin, cos, asin, sqrt
from users.models import Profile

# ✅ 거리 계산 함수 (하버사인 공식을 이용한 거리 계산)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 지구 반지름 (km)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# ✅ 성별 및 성적 지향 기반 필터링 함수
def get_gender_match_candidates(user_profile):
    user_gender = user_profile._gender
    user_pref = user_profile._sex_orientation

    all_profiles = Profile.objects.exclude(id=user_profile.id)
    matched_profiles = []

    for profile in all_profiles:
        # 서로의 조건이 맞는지 확인
        if is_mutually_acceptable(user_profile, profile):
            matched_profiles.append(profile)

    return matched_profiles

def is_mutually_acceptable(user1, user2):
    # 성별 조건
    def matches_pref(gender, preference, target_gender):
        if preference == '이성을 만나고 싶어요':
            return gender != target_gender
        elif preference == '동성을 만나고 싶어요':
            return gender == target_gender
        elif preference == '모두 만나고 싶어요':
            return True
        return False

    return (
        matches_pref(user1._gender, user1._sex_orientation, user2._gender) and
        matches_pref(user2._gender, user2._sex_orientation, user1._gender)
    )

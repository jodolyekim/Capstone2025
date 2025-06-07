# users/utils/matching.py

from users.models import Profile

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

from .models import UserProfile, Match
from django.contrib.auth.models import User

def find_best_matches(current_user):
    current_keywords = set(current_user.userprofile.keywords)
    other_profiles = UserProfile.objects.exclude(user=current_user)
    
    scored_users = []
    for profile in other_profiles:
        overlap = current_keywords & set(profile.keywords)
        score = len(overlap)
        scored_users.append({
            'user_id': profile.user.id,
            'username': profile.user.username,
            'common_keywords': list(overlap),
            'score': score
        })
    
    # 점수 높은 순 정렬
    scored_users.sort(key=lambda x: x['score'], reverse=True)
    return scored_users

# 자기 자신 제외한 사용자들 대상으로 교집합 개수 계산
# 점수 순으로 정렬해 추천 리스트 반환
from users.models import Match
from django.utils import timezone

def create_match(user_a, user_b, matched_keywords=None):
    """
    두 사용자(user_a, user_b) 사이의 Match를 생성하거나 기존 Match를 반환합니다.
    - ID 기준으로 user1, user2 순서를 고정합니다.
    - matched_keywords는 리스트 형태여야 하며 기본값은 빈 리스트입니다.
    """
    if user_a == user_b:
        raise ValueError("자기 자신과 매칭할 수 없습니다.")

    # ID 순서 고정 (항상 작은 ID를 user1으로)
    user1, user2 = sorted([user_a, user_b], key=lambda u: u.id)

    # 기본값 세팅
    matched_keywords = matched_keywords or []

    # 기존 Match가 있으면 가져오고, 없으면 생성
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

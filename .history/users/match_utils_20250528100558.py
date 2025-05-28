def create_match(user1, user2, keywords):
    if user1 == user2:
        raise ValueError("자기 자신과 매칭할 수 없습니다.")

    # ID 순서 고정
    user1, user2 = sorted([user1, user2], key=lambda u: u.id)

    match, created = Match.objects.get_or_create(
        user1=user1,
        user2=user2,
        defaults={'matched_keywords': keywords}
    )
    return match

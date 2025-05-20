# 매칭 생성 함수
def create_match(requester, receiver, keywords):
    if requester == receiver:
        raise ValueError("자기 자신과 매칭할 수 없습니다.")  # 자기 자신과의 매칭 방지

    match, created = Match.objects.get_or_create(
        requester=requester,
        receiver=receiver,
        defaults={'matched_keywords': keywords}  # 키워드 정보 초기 저장
    )
    return match  # 이미 존재해도 반환


from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Profile, Interest, SuggestedInterest
import random
from datetime import date, timedelta

User = get_user_model()

GENDERS = ['남성', '여성']
ORIENTATIONS = ['이성을 만나고 싶어요', '동성을 만나고 싶어요', '모두 만나고 싶어요']
COMMUNICATION_STYLES = [
    '짧은 문장으로 대화하고 싶어요', '답장이 빠르면 좋겠어요', '답장이 느려도 괜찮아요',
    '관심사만 이야기 하고 싶어요', '천천히 알아가고 싶어요', '대화가 끊기기 전에 미리 말해줬으면 좋겠어요',
    '문자로 대화하는 걸 좋아해요', '부드럽게 대화하고 싶어요', '서로의 말에 공감의 메시지를 주고받고 싶어요'
]

class Command(BaseCommand):
    help = '테스트 계정 ForTest1~20 + 프로필 + 키워드 생성'

    def handle(self, *args, **kwargs):
        password = "TestPassword123!"
        keywords_pool = list(SuggestedInterest.objects.filter(is_active=True))

        for i in range(1, 21):
            email = f"fortest{i}@example.com"
            name = f"ForTest{i}"

            # 사용자 생성
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                self.stdout.write(self.style.WARNING(f'⚠️ {email} 이미 존재함'))
            else:
                user = User.objects.create_user(email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'✅ {email} 생성 완료'))

            # 프로필 생성
            if not hasattr(user, 'profile'):
                birthdate = date.today() - timedelta(days=random.randint(20 * 365, 35 * 365))
                gender = random.choice(GENDERS)
                orientation = random.choice(ORIENTATIONS)
                comm_styles = random.sample(COMMUNICATION_STYLES, k=3)

                Profile.objects.create(
                    user=user,
                    _name=name,
                    _birthYMD=birthdate,
                    _gender=gender,
                    _sex_orientation=orientation,
                    _communication_way=comm_styles,
                    _match_distance=random.choice([3, 5, 10]),
                    _current_location_lat=37.5665,
                    _current_location_lon=126.9780,
                    is_approved=True,
                )
                self.stdout.write(self.style.SUCCESS(f'🧾 {email} 프로필 생성 완료'))

            # 키워드 추가
            existing_keywords = Interest.objects.filter(user=user).count()
            if existing_keywords == 0:
                selected_keywords = random.sample(keywords_pool, k=random.randint(5, 10))
                for kw in selected_keywords:
                    Interest.objects.create(
                        user=user,
                        keyword=kw.keyword,
                        source='테스트'
                    )
                self.stdout.write(self.style.SUCCESS(f'🏷️ {email} 키워드 {len(selected_keywords)}개 추가 완료'))

        self.stdout.write(self.style.SUCCESS("🎯 ForTest 계정 20개 + 키워드 생성 완료"))

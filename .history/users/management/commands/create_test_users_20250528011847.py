from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Profile
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
    help = '테스트 사용자 10명을 생성하고 기본 프로필을 설정합니다.'

    def handle(self, *args, **kwargs):
        base_email = "testuser{}@example.com"
        password = "TestPassword123!"

        for i in range(1, 11):
            email = base_email.format(i)

            # 1. 사용자 생성
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                self.stdout.write(self.style.WARNING(f'⚠️ {email} 이미 존재함'))
            else:
                user = User.objects.create_user(email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'✅ {email} 생성 완료'))

            # 2. 프로필 자동 생성
            if not hasattr(user, 'profile'):
                birthdate = date.today() - timedelta(days=random.randint(20 * 365, 35 * 365))  # 20~35세
                gender = random.choice(GENDERS)
                orientation = random.choice(ORIENTATIONS)
                communication_styles = random.sample(COMMUNICATION_STYLES, k=3)

                profile = Profile.objects.create(
                    user=user,
                    _name=f"테스트유저{i}",
                    _birthYMD=birthdate,
                    _gender=gender,
                    _sex_orientation=orientation,
                    _communication_way=communication_styles,
                    _match_distance=random.choice([3, 5, 10]),
                    _current_location={'lat': 37.5665, 'lon': 126.9780},  # 서울
                    is_verified=True  # 보호자 승인된 상태로 간주
                )
                self.stdout.write(self.style.SUCCESS(f'🧾 {email} 프로필 생성 완료'))
            else:
                self.stdout.write(f'🔄 {email} 이미 프로필 있음')

        self.stdout.write(self.style.SUCCESS('🎉 테스트 계정 + 프로필 생성 완료'))

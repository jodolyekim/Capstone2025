# Capstone2025
Dankook Univ. Capstone Project 2025 1st semester.

Django, PostgreSQL, Redis를 기반으로 한 개발 환경을 Docker로 구성한 템플릿으로
팀원 누구나 빠르게 동일한 환경에서 개발할 수 있습니다.

## infra/base-setup 디렉토리 구조
```
Capstone2025
├── app/              
│ ├── manage.py            
│ └── Capstone2025/	        		
│   ├── settings.py
│   └── ...            
├── Dockerfile          
├── docker-compose.yml  
├── requirements.txt  
├── .env.example        
└── README.md 
```

---

## ⚙️ 사용 기술
```yaml
- Python 3.10
- Django 4.x
- PostgreSQL 15
- Redis 7
- Docker & docker-compose
```

---

## 🚀 실행 방법

### 1. 프로젝트 클론

```bash
git clone https://github.com/jodolyekim/Capstone2025.git
cd Capstone2025
```

---

### 2. .env 파일 생성
```bash
cp .env.example .env
```

---

### 3. Docker 컨테이너 실행
```bash
docker-compose up --build
```

---

### 4. Django 초기 마이그레이션 및 superuser 생성
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🧪 개발 팁

## 🧼 정리 및 종료
```bash
docker-compose down
```
---

## 📁 환경 변수 (.env)
| 변수명                 | 설명                    |
| ------------------- | --------------------- |
| DJANGO\_SECRET\_KEY | 장고 시크릿 키              |
| DJANGO\_DEBUG       | 디버그 모드 (True / False) |
| POSTGRES\_DB        | DB 이름                 |
| POSTGRES\_USER      | DB 사용자명               |
| POSTGRES\_PASSWORD  | DB 비밀번호               |

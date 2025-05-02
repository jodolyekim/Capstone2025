# Capstone2025
Dankook Univ. Capstone Project 2025 1st semester.

Django, PostgreSQL, Redis를 기반으로 한 개발 환경을 Docker로 구성한 템플릿으로 팀원 누구나 빠르게 동일한 환경에서 개발할 수 있습니다.

#### 이하 모든 작업은 WSL2(Window Subsystem for Linux)에서 작업했습니다.
#### Docker 특성 상 Linux 기본 문법이 요구됩니다. 

## 시작하기 전 

### 1. Docker Desktop 설치
#### 아래 페이지에 접속해서 Docker Desktop 설치
> <https://www.docker.com/>

#### 설치 과정은 아래 페이지를 참고
> Windows <https://myanjini.tistory.com/entry/%EC%9C%88%EB%8F%84%EC%9A%B0%EC%97%90-%EB%8F%84%EC%BB%A4-%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91-%EC%84%A4%EC%B9%98>

> MAC <https://goddaehee.tistory.com/312>

---

## infra/base-setup 디렉토리 구조
```
Capstone2025
├── app/                  # 실제 소스코드
│ ├── manage.py           
│ └── Capstone2025/	        		
│   ├── settings.py
│   └── ...            
├── Dockerfile            # 실행 환경 정의
├── docker-compose.yml    # 전체 서비스 구성
├── requirements.txt      # 의존성 목록  
├── .env.example          # 환경변수 예시
└── README.md             # 실행 방법 설명 (현재 페이지)
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

+ Django 코드는 app/ 디렉토리에서 작업합니다.
+ 코드 수정 시 컨테이너는 자동 반영됩니다 (volumes 사용 중).
+ requirements.txt 수정 시 docker-compose build 다시 실행



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

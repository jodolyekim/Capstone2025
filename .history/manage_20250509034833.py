#!/usr/bin/env python
"""
Django 관리 명령어를 실행하는 메인 진입점 파일입니다.
예: python manage.py runserver, python manage.py migrate 등
"""

import os
import sys

def main():
    """Django 명령어 실행용 메인 함수"""
    # 환경 변수 설정: Django 설정 모듈 경로 지정
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        # Django 명령어 실행 함수 로드
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Django가 설치되지 않았거나 가상환경 문제가 있을 때 에러 발생
        raise ImportError(
            "Django를 불러올 수 없습니다. 가상환경이 활성화되었는지, "
            "PYTHONPATH에 Django가 설치되어 있는지 확인하세요."
        ) from exc

    # 명령어 실행 (예: runserver, makemigrations 등)
    execute_from_command_line(sys.argv)

# 이 파일이 메인으로 실행되었을 때만 main() 호출
if __name__ == '__main__':
    main()

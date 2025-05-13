#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Django 관리 명령어를 실행하는 메인 함수"""
    # 환경 변수 설정: Django 설정 파일 경로 지정
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        # Django 명령어 실행 모듈 import
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Django가 설치되지 않았을 경우 에러 메시지 출력
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # 명령어 실행 (예: runserver, migrate 등)
    execute_from_command_line(sys.argv)

# 이 파일이 직접 실행되었을 때만 main() 실행
if __name__ == '__main__':
    main()

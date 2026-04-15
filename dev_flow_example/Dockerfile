# 1. 베이스 이미지: Python 3.11 (슬림 버전)
FROM python:3.11-slim

# 2. 컨테이너 안에서 작업할 디렉토리 지정
WORKDIR /app

# 3. 의존성 먼저 설치 (코드보다 먼저 — 캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 게임 코드 복사
COPY orin/ ./orin/
COPY configs/ ./configs/

# 5. 기본 실행 명령
CMD ["python3", "-m", "orin.core.coordinator"]

# KnowHalu: AI Hallucination Detection

KnowHalu는 AI가 생성한 응답에서 발생할 수 있는 할루시네이션(허위 정보)을 감지하고 분석하는 도구입니다.

## 주요 기능

- 2단계 할루시네이션 검사
  - Phase 1: 질문-답변 관련성 검사
  - Phase 2: 지식 기반 판단
- 한국어 결과 제공 (DeepL 번역)
- 직관적인 웹 인터페이스
- 상세한 분석 결과 제공

## 기술 스택

- Backend
  - FastAPI
  - Python 3.12
  - OpenAI GPT-4
  - DeepL API

- Frontend
  - React
  - TypeScript
  - TailwindCSS
  - Heroicons

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/hwankhai/SNU-BigFin-9th-Capstone-KPMG.git
cd SNU-BigFin-9th-Capstone-KPMG
```

2. 백엔드 설정
```bash
cd backend
python -m venv env
source env/bin/activate  # Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

3. 프론트엔드 설정
```bash
cd frontend
npm install
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가:
```
OPENAI_API_KEY=your_openai_api_key
DEEPL_API_KEY=your_deepl_api_key
```

5. 실행
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend (새 터미널에서)
cd frontend
npm start
```

## 사용 방법

1. 웹 브라우저에서 http://localhost:3000 접속
2. 질문, 지식베이스, 답변을 입력
3. "Evaluate" 버튼 클릭
4. 분석 결과 확인

## API 엔드포인트

- POST `/evaluate`
  - 입력: 질문, 지식베이스, 답변
  - 출력: 할루시네이션 분석 결과

## 라이선스

MIT License

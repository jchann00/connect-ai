# 🧬 Monolog Studio OS — 자가 매뉴얼

## 이 워크스페이스는 무엇인가요?
Monolog Studio(대표: jcan)의 두뇌이자 작업 공간입니다. 코다리를 비롯한 AI 에이전트 팀이 여기서 제품을 개발하고 비즈니스를 운영합니다.

## 폴더 구조
- `_shared/` — 모든 에이전트가 매번 읽는 공동 메모리
  - `identity.md` — Monolog Studio 정체성 (이름, 톤, 가치)
  - `goals.md` — 공동 목표 (장기/단기)
  - `decisions.md` — 의사결정 로그 (최우선 순위 메모리)
  - `agent_models.json` — 에이전트별 최적 모델 배정 (Ollama 기반)
  - `tracker.json` — 작업 추적 및 태스크 큐
- `_agents/<id>/` — 각 에이전트 개인 공간
  - `memory.md` — 자가학습 기록
  - `prompt.md` — 맞춤형 페르소나 지시사항
  - `config.md` — API 키 및 시크릿 (.gitignore로 보호)
  - `skills/` — 검증된 재사용 패턴
- `sessions/` — 세션별 산출물
- `approvals/` — 승인 대기/완료 작업

## 에이전트 팀 구성
- 🧭 **CEO**: Monolog Studio 총괄 기획 & 제품 로드맵 디렉터
- 💻 **코다리**: 시니어 풀스택 엔지니어 (Lead) — 코드 개발, 아키텍처, 검증
- 💼 **현빈**: Head of Business & SaaS 전략 — BM, 가격 정책, 시장 분석
- 📱 **영숙**: 비서 (Executive Assistant) — 일정, 할 일, 텔레그램 데일리 보고
- 🎨 **디자이너**: UI/UX & 제품 디자이너 — 웹/앱 인터페이스, 디자인 시스템
- ✍️ **카피라이터**: Technical Copywriter — 기술 문서, 랜딩페이지 카피
- 🔍 **리서처**: Tech & Trend Researcher — 최신 오픈소스, 스택 리서치
- 📺 **레오**: Head of Media — 데모 영상 및 기술 쇼케이스
- 🎵 **루나**: Sound Producer — 데모 BGM 및 사운드 효과
- 📷 **인스타그램**: SNS 마케터 — 빌드인퍼블릭 및 개발 일지

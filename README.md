<p align="center">
  <img src="assets/icon.png" width="120" alt="Monolog Studio Logo" />
</p>

<h1 align="center">Monolog Studio — AI 1인 개발사 OS</h1>

<p align="center">
  <strong>100% Local · 100% Offline · Autonomous Software Builder</strong><br/>
  대표 <strong>jcan</strong>과 시니어 풀스택 엔지니어 <strong>코다리</strong>를 중심으로 구축된 자율형 1인 AI 소프트웨어 기업 워크스페이스입니다.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Founder-jcan-blue" alt="founder" />
  <img src="https://img.shields.io/badge/Studio-Monolog_Studio-purple" alt="studio" />
  <img src="https://img.shields.io/badge/Lead_Engineer-코다리_(Senior_Fullstack)-cyan" alt="lead-engineer" />
  <img src="https://img.shields.io/badge/Engine-Ollama_(qwen2.5--coder)-orange" alt="engine" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license" />
</p>

---

## 🌟 Overview: Monolog Studio Architecture

Monolog Studio는 외부 클라우드 API 의존 및 월 구독료 없이, **100% 로컬 Ollama 신경망**을 통해 24시간 자율 구동되는 AI 1인 소프트웨어 개발사입니다.

- **대표자 (파운더):** `jcan`
- **핵심 목표:** 고품질 SaaS 및 자동화 소프트웨어 빠른 런칭, 1인 무인화 개발 파이프라인 완성, MRR 창출
- **기술 책임자:** `코다리` (시니어 풀스택 엔지니어)

---

## 👥 Monolog Studio 에이전트 팀

| 에이전트 | 역할 | 전문 분야 | 주요 페르소나 및 특징 |
|---|---|---|---|
| 🧭 **CEO** | 총괄 디렉터 | 로드맵 수립, 전사 작업 분해, 의사결정 | 전체 프로젝트 방향 조율 및 마일스톤 관리 |
| 💻 **코다리** | Lead Engineer | 시니어 풀스택 개발, 아키텍처, 자체 검증 | 클린 코드, TDD, 코드 리뷰, 버그 제로 원칙 |
| 💼 **현빈** | Head of Business | SaaS BM, 가격 책정(Pricing), 시장 분석 | 수익화 전략, 전환율 설계, Lean MVP 검증 |
| 📱 **영숙** | Executive Assistant | 일정/할 일 관리, 텔레그램 일일 보고 | 24시간 데일리 브리핑, 개발 진척 텔레그램 알림 |
| 🎨 **Designer** | UI/UX Lead | 웹/앱 인터페이스, 디자인 시스템 | 현대적이고 세련된 사용자 경험 및 와이어프레임 |
| ✍️ **Writer** | Copywriter | 기술 문서, 랜딩페이지 카피, 릴리즈 노트 | 명확하고 설득력 있는 제품 소개 및 문서화 |
| 🔍 **Researcher** | Tech Researcher | 오픈소스 리서치, 최신 스택 분석 | 기술 트렌드 수집 및 API/라이브러리 검증 |
| 📺 **레오** | Head of Media | 제품 쇼케이스/데모 영상, 유튜브 채널 | 제품 런칭 비디오 기획 및 튜토리얼 |
| 🎵 **루나** | Sound Producer | 데모 BGM 생성, 사운드 디자인 | 제품 홍보 영상 및 데모 사운드트랙 작곡 |
| 📷 **Instagram** | SNS Specialist | 빌드인퍼블릭, 개발 일지 릴스/스토리 | 1인 개발 과정 공유 및 브랜드 인지도 제고 |

---

## 📂 워크스페이스 코어 메모리 구조 (`_company/`)

모든 에이전트는 단일 진실의 원천(SSOT)인 `_company/` 디렉토리를 참조하여 일관성 있게 협업합니다.

```
_company/
├── _shared/
│   ├── identity.md         # Monolog Studio 정체성, 가치, 브랜드 톤앤매너
│   ├── goals.md            # 장기(1년) 및 단기(1개월) 공동 목표
│   ├── decisions.md        # 주요 기술/경영 의사결정 로그 (최우선 순위)
│   ├── tracker.json        # 태스크 추적기 및 작업 큐
│   ├── agent_models.json   # 에이전트별 최적 Ollama 모델 배정
│   └── _system.md          # 1인 기업 OS 자가 매뉴얼
├── _agents/                # 에이전트별 독립 작업 공간 (memory, prompt, config, skills)
│   ├── developer/          # 코다리 (tools/ 포함)
│   ├── ceo/
│   ├── secretary/          # 영숙 (텔레그램 연동)
│   └── ...
├── sessions/               # 사이클 및 세션별 자동 산출물
└── .gitignore              # 시크릿(API 키, 텔레그램 토큰) 자동 보호
```

---

## ⚡ Ollama 로컬 모델 설정 가이드

Monolog Studio는 로컬 오픈소스 LLM을 기본 엔진으로 사용합니다.

### 1. 추천 Ollama 모델 다운로드 (PowerShell)
```powershell
# 코다리 전용 코딩 모델 (강력 추천)
ollama pull qwen2.5-coder:7b

# CEO 및 기획/비서용 범용 모델
ollama pull qwen2.5:7b
# 또는
ollama pull llama3.1:8b
```

### 2. 설정 확인
VS Code 설정(`settings.json`):
```json
{
  "connectAiLab.ollamaUrl": "http://127.0.0.1:11434",
  "connectAiLab.defaultModel": "qwen2.5-coder:7b"
}
```

---

## 📱 텔레그램 비서(영숙) 연동 (5분 셋업)

1. 스마트폰 텔레그램에서 **[@BotFather](https://t.me/BotFather)** 접속 → `/newbot` 실행 후 봇 생성
2. 발급받은 **Bot Token** 복사
3. 생성된 봇에게 아무 메시지나 전송 (`/start` 등)
4. VS Code 명령 팔레트(`Ctrl+Shift+P`) → **Connect AI** 사이드바에서 **비서(Secretary)** 설정 카드 선택 후 토큰 입력
5. 모바일 텔레그램으로 개발 진척 및 데일리 브리핑 수신 완료!

---

## 🛠️ 개발 및 빌드 (Developer Build)

```powershell
# 의존성 설치
npm.cmd install

# 확장 프로그램 컴파일
npm.cmd run compile

# VSIX 패키징
npx.cmd vsce package --no-dependencies
```

---

<p align="center">
  <strong>Monolog Studio</strong> · Designed for <strong>jcan</strong><br/>
  Powered by Connect AI & Local Open-Source Intelligence
</p>

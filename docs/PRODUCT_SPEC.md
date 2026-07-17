# Intent-Preserving Development Skills Product Spec

[English mirror](en/PRODUCT_SPEC.md)

## Document control

- Status: accepted
- Last reviewed: 2026-07-18
- Working language: Korean

## Product intent

- Why this exists: 같은 AI 도구를 사용하더라도 사용자의 암묵적 의도, 가치 판단, 직접 개입 이유가 구현과 세션 전환 과정에서 사라지지 않게 한다.
- User intent to preserve: 구현 전에 중요한 제품 결정을 라운드별 질문으로 명시화한다. 결정이 완료될 때까지 총 질문 수 제한 없이 반복하되, 사용자가 위임한 구현 영역은 에이전트 소유로 종료하고 목표·현재 상태·미래 순서·결정 근거를 분리해 보존하여 다음 에이전트가 대화 기록 없이도 같은 의도로 작업을 이어가게 한다.
- Priority values: 사용자 의도 보존, 실제 저장소 증거, 승인 전 무변경, 세션 독립 인수인계, 불필요한 문서 churn 방지.
- Non-negotiable tradeoffs: 사소한 작업까지 무겁게 만들지 않으며, 구현 속도를 위해 제품·안전·개인정보 결정을 추측하거나 과거 결정 근거를 덮어쓰지 않는다.
- Reconsider these choices when: 다른 시스템이 동일하거나 더 강한 의도·근거·현재 상태·인수인계 보장을 더 낮은 운영 비용으로 제공한다는 반복 가능한 증거가 생긴다.

## Product definition

`manage-project-intent`는 소프트웨어 프로젝트의 의도 추출, 계획 승인, 네 개의 정식 문서, 현재 상태 추적, 결정 변경, 단일 Next task 실행, 검증과 Goldfish 인수인계를 관리하는 공개 오픈소스 Codex Skill이다. 실제 코딩·디자인·GitHub·배포 전문 절차는 설치된 전문 Skill에 위임하고, 이 Skill은 제품 운영 제어층을 담당한다.

## Users and problems

- Primary user: 여러 세션과 프로젝트에서 Codex를 사용하는 개인 개발자, 제품 제작자, 소규모 개발팀.
- Problem: 채팅에만 남은 의도와 결정 근거가 다음 세션에서 사라지고, 문서의 목표 상태와 실제 구현 상태가 섞이며, 완료 주장과 다음 작업이 검증 증거 없이 흔들린다.
- Job: 새 프로젝트는 중요한 결정이 완료될 때까지 충분히 질문한 뒤 시작하고, 기존 프로젝트는 실제 저장소와 문서에서 재개하며, 중요한 개입 이유를 미래 에이전트가 보존하게 한다.

## Goals and success criteria

- 모호한 새 제품을 Full로 분류하고 승인 전 저장소를 변경하지 않는다.
- Full 인터뷰는 라운드당 1~3개의 중요한 질문을 반복하고, 모든 material route가 `answered`, `deferred`, `agent-owned`, `not applicable` 중 하나가 될 때까지 임의의 총량 제한으로 끝내지 않는다.
- Full·Delta·Lite를 구분해 필요한 질문과 문서 갱신만 수행한다.
- `PRODUCT_SPEC.md`, `ROADMAP.md`, `PROJECT_STATUS.md`, `DECISION_LOG.md`의 소유권을 분리한다.
- 현재 동작은 코드·테스트·실행 결과에서, 목표 동작은 Product Spec에서 판단하고 충돌을 drift로 보존한다.
- 정확히 하나의 검증 가능한 Next task로 세션을 재개한다.
- fresh agent가 의도, 보호 결정, 현재 상태, 다음 작업과 완료 증거를 복원한다.
- 단위 테스트와 행동 평가가 승인된 수용 시나리오를 반복 검증한다.
- 공개 저장소에서 공식 Skill installer로 설치 가능한 원본을 제공한다.
- 공개 사용자가 실제 프로젝트 운영 기록을 읽을 수 있도록 네 canonical 문서의 영문 미러를 제공한다.
- 효용을 보장된 생산성 향상으로 과장하지 않고 문서 유지 비용과 적용 경계를 함께 설명한다.

## Scope

### In scope

- GitHub 공개 저장소와 전역 설치본을 분리하고 신규 설치와 기여자용 로컬 동기화 경로를 제공한다.
- MIT 라이선스, 영문·한국어 README와 `docs/en/` 영문 문서 미러를 제공한다.
- 인터뷰, 문서 계약, lifecycle, Spec Kit 선택적 adapter, 템플릿을 유지·강화한다.
- bootstrap의 신규·legacy·부분 문서 상태와 임의 작업 언어를 안전하게 처리한다.
- validator가 로드맵·상태·결정의 구조 및 의미 충돌을 검사한다.
- 단위 fixture, fresh-agent 행동 평가 케이스, 익명화된 real-world project backtest를 제공한다.
- 후속 Skill 분리 후보와 진입 조건을 로드맵에 보존한다.

### Out of scope

- 공개 Plugin·Marketplace 배포, 모든 대화에 개입하는 메타 Skill, 자동 훅.
- Notion·Jira·외부 이슈 트래커 동기화.
- 이번 단계에서 `elicit-*`, `audit-*`, `revise-*`, `advance-*`, `validate-*` 하위 Skill을 실제로 분리하는 작업.
- 특정 개인 프로젝트의 문서, 이름, 경로, 기능 또는 결정 공개.

## User experience

- 관련 요청 또는 프로젝트 opt-in 신호가 있을 때만 자동 선택되고, 사소한 질문·번역·단일 코드 수정에는 암묵적으로 개입하지 않는다.
- Full은 저장소 조사 후 한 번에 1~3개의 중요한 질문을 묻고, 답변이 바꾼 계약과 다음 material gap을 확인하며 결정 완료까지 반복한다. 사용자가 명시적으로 위임한 구현·배포 영역은 `agent-owned`로 종료하고, 결정 완료 계획의 승인 뒤에만 문서와 코드를 변경한다.
- Delta는 기존 계약 안의 영향만 확인하고, Lite는 영구 문서 churn을 피한다.
- `status`와 `audit`은 읽기 전용이며, `continue`는 단 하나의 Next task만 범위로 삼는다.

## Functional requirements

- Skill metadata는 의도·가치·개입 이유, 장기 운영, 결정 변경, drift 감사 트리거와 명시적 비트리거를 포함한다.
- Full 인터뷰는 질문 수가 아니라 결정 범위로 종료한다. 라우트별 임시 결정 inventory는 `answered`, `deferred`(담당자·재개 조건 포함), `agent-owned`, `not applicable` 상태를 보존하며 다섯 번째 정식 문서로 materialize하지 않는다.
- 사용자가 기술·배포·일상 구현 영역을 위임하면 해당 영역의 routine 질문을 중단하고, 보호된 제품 결정과 material 충돌이 생길 때만 그 이유를 설명하고 다시 연다.
- bootstrap은 기본 dry-run이고 기존 파일을 덮어쓰지 않는다. Legacy 3문서의 적용은 명시적 migration flag를 요구하며 불명확한 부분 문서 집합은 중단한다.
- validator는 필수 문서·heading·placeholder·링크·ID·Next task·phase 상태·완료 증거·decision supersede·프로젝트 완료 충돌을 검사한다.
- 중요한 사용자 개입만 Decision Log에 보존하며 사소한 문구·구현 수정은 영구 결정으로 승격하지 않는다.
- Spec Kit이 있으면 선택된 한 작업의 실행 계층으로만 사용하고 결과를 네 정식 문서에 수렴한다.
- 공식 Skill installer는 공개 `main` 경로에서 신규 설치를 제공한다. 저장소의 기여자용 동기화 도구는 원본과 설치 대상의 차이를 먼저 보여주고 명시적 적용을 요구한다.
- `docs/`의 한국어 네 문서를 canonical 원본으로 유지하고 `docs/en/`의 영문 미러를 같은 변경에서 갱신한다. 두 언어는 phase, task, decision ID, 상태와 검증 증거를 동일하게 유지한다.

## Safety, privacy, and data

- 사용자 저장소와 기존 문서를 기본 보존하며 자동 덮어쓰기·자동 마이그레이션을 하지 않는다.
- status·audit·Goldfish·real-world project backtest는 읽기 전용이다.
- 검증 중 채팅의 의도된 답을 fresh agent에 노출하지 않는다.
- 외부 서비스·자격 증명·개인 데이터를 요구하거나 동기화하지 않는다.
- 공개 저장소에는 특정 개인 프로젝트의 식별자, 로컬 경로, 원본 데이터 또는 비공개 결정을 포함하지 않는다.

## Non-functional requirements

- Skill 본문은 짧은 라우터로 유지하고 세부 지식은 한 단계 참조와 실행 스크립트로 분리한다.
- runtime 스크립트는 Python 표준 라이브러리만 사용하고 Windows 경로와 UTF-8 문서를 지원한다.
- 명령은 실패 이유와 구체적인 issue code를 제공하고 JSON 출력을 유지한다.
- 설치·bootstrap은 반복 실행해도 같은 결과를 내며 승인되지 않은 삭제를 하지 않는다.
- 영문 미러는 별도의 제품 상태나 결정 원본으로 사용하지 않으며 canonical 문서와 구조적으로 비교할 수 있어야 한다.

## Acceptance criteria

- 공식 Skill 패키지 validator와 전체 단위 테스트가 통과한다.
- 새 프로젝트의 다중 라운드 Full 인터뷰, 명시적 위임 경계, Delta, Lite, status/audit, continue, revise, Spec Kit 양쪽, Goldfish 행동 평가 케이스가 모두 정의되고 대표 fresh-agent 실행이 통과한다.
- 익명화된 real-world project backtest가 예상된 호환 결과를 보고하며 대상 작업 트리를 변경하지 않는다.
- 공개 `main` 경로에서 임시 Codex 홈으로 설치되고 다음 fresh turn에서 발견된다.
- 공개 README, MIT 라이선스와 비로그인 접근이 검증된다.
- README에서 실제 네 운영 문서의 한국어 원본과 영문 미러에 직접 접근할 수 있고, 두 언어의 ID·상태·Next task가 일치한다.
- 공개 저장소에서 특정 개인 프로젝트명과 개인 경로 검색 결과가 0건이다.
- 원본 저장소에는 정확히 하나의 Next task와 최종 검증 증거가 남는다.

## Open questions

None.

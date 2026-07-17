# Intent-Preserving Development Skills Roadmap

[English mirror](en/ROADMAP.md)

## Document control

- Status: active
- Last reviewed: 2026-07-18
- Working language: Korean

## Status vocabulary

- `planned`: accepted future work that has not started.
- `active`: the one phase currently being executed.
- `blocked`: accepted work that cannot progress until a named condition changes.
- `done`: exit criteria and verification evidence are complete.
- `superseded`: intentionally replaced by a linked phase or decision.

## Current phase

- Phase: PHASE-002
- Outcome: 실제 사용 증거가 있는 workflow 단계만 독립 Skill 후보로 평가한다.

## Phases

### PHASE-001 — Harden and rename the core Skill

- Status: done
- Outcome: 기존 Skill의 의도 보존 계약을 유지하면서 이름, 안전 장치, validator와 평가 체계를 강화한다.
- Dependencies: Approved implementation plan and existing `manage-project-specs` source.
- Entry criteria: 사용자가 `manage-project-intent` 완전 교체, 개인 opt-in, 하이브리드 제어층을 승인했다.
- Exit criteria: 패키지·단위·행동·real-world project·설치 검증이 통과하고 문서가 최종 상태로 수렴한다.
- Verification evidence: Official package validation passed; 15 Skill tests and 3 installer tests passed; new-product forward-test, real-world project validator/Goldfish, installed Skill discovery, and exact installation passed on 2026-07-18.

Tasks:

- [x] TASK-001: 정식 프로젝트 문서를 materialize하고 구현 계약을 고정한다.
- [x] TASK-002: 기존 Skill을 Git 원본으로 이전·개명하고 bootstrap·validator·템플릿을 강화한다.
- [x] TASK-003: 설치 도구와 반복 가능한 단위·행동 평가 자산을 추가한다.
- [x] TASK-004: 전체 검증 후 새 전역 Skill을 설치하고 기존 설치를 제거한다.

### PHASE-003 — Publish the Skill

- Status: done
- Outcome: 사용자 의도 보존 방법론과 재사용 가능한 Skill을 개인 프로젝트 정보 없이 공개한다.
- Dependencies: PHASE-001 completion and the approved public-upload plan.
- Entry criteria: 공개 저장소 이름, MIT 라이선스와 영문·한국어 문서 범위가 승인됐다.
- Exit criteria: 로컬 검사가 통과하고 공개 페이지와 `main` 경로 원격 설치가 검증된다.
- Verification evidence: English and Korean READMEs passed fresh-agent first-use review; MIT and public GitHub `main` are available; official remote installation, official package validation, source hash comparison, anonymous README access, public hygiene checks, and English canonical-document mirror parity passed on 2026-07-18.

Tasks:

- [x] TASK-007: 공개 문서와 라이선스를 구현하고 `seolbbb/manage-project-intent`에 Skill을 게시한다.
- [x] TASK-008: 네 실제 운영 문서의 영문 미러를 추가하고 양언어 README에서 직접 연결한다.

### PHASE-004 — Make the decision-completion loop explicit

- Status: done
- Outcome: 반복 질문이 부차적인 단계가 아니라 사용자 의도를 추출하는 핵심 루프임을 Skill, 공개 문서와 행동 평가에서 일관되게 드러낸다.
- Dependencies: PHASE-001 and PHASE-003 completion plus a user-confirmed need to make the interview loop more explicit.
- Entry criteria: 실제 Full 인터뷰가 다중 라운드의 consequential 질문으로 의도와 보호 가치를 결정했다는 증거를 확인했다.
- Exit criteria: Full 인터뷰에 총량 제한 없음, route terminal state, 명시적 위임 경계가 Skill·README·평가에 반영되고 package, unit, document validation과 설치본 동기화가 통과한다.
- Verification evidence: Official package validation passed; 16 Skill tests and 3 installer tests passed; canonical document validation passed with errors=0 and warnings=0; README and document local-link check passed; the installed Skill passed package validation and all 16 Skill tests; source/installed manifest was UP-TO-DATE on 2026-07-18.

Tasks:

- [x] TASK-009: 결정 완료까지 반복 질문하는 핵심 루프와 사용자 위임 경계를 Skill·공개 문서·행동 평가에 반영한다.

### PHASE-002 — Extract independently valuable intent Skills

- Status: planned
- Outcome: 반복 평가에서 독립 호출 가치가 확인된 workflow 단계만 별도 Skill로 분리한다.
- Dependencies: PHASE-001 and PHASE-003 completion plus evidence of repeated independent triggers or irrelevant context loading.
- Entry criteria: 최소 한 후보가 독립 사용자 요청과 fresh-agent 평가를 갖는다.
- Exit criteria: 분리된 각 Skill이 자체 trigger, contract, tests를 가지며 루트 라우터와 중복·순환 없이 동작한다.
- Verification evidence: Not available until the phase is done.

Tasks:

- [ ] TASK-005: `elicit-project-intent`와 `audit-project-intent`의 분리 필요성을 실제 사용 기록으로 평가한다.
- [ ] TASK-006: `revise-project-intent`, `advance-project-intent`, `validate-intent-handoff` 후보와 전문 Skill adapter 경계를 평가한다.

## Change policy

- Change phase order only after recording the reason and downstream effects.
- Mark work done only from verification evidence.
- Keep future work here; keep only one executable Next task in `PROJECT_STATUS.md`.

# Intent-Preserving Development Skills Roadmap

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
- Verification evidence: English and Korean READMEs passed fresh-agent first-use review; MIT and public GitHub `main` are available; official remote installation, official package validation, source hash comparison, anonymous README access, and public hygiene checks passed on 2026-07-18.

Tasks:

- [x] TASK-007: 공개 문서와 라이선스를 구현하고 `seolbbb/manage-project-intent`에 Skill을 게시한다.

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

# Intent-Preserving Development Skills Project Status

## Snapshot

- Last verified: 2026-07-18
- Working language: Korean
- Current phase: PHASE-003
- State: active
- Repository state: Git source contains the canonical project record, `manage-project-intent`, installer, and tests; the approved public upload is in progress and GitHub has not yet been created.

## Implemented

- `skills/manage-project-intent`가 Git 원본으로 구성되고 frontmatter, UI metadata, AGENTS marker, Goldfish prompt가 새 이름으로 수렴했다.
- Skill은 의도·가치·중대한 개입, 프로젝트 opt-in, Full/Delta/Lite, 네 정식 문서, 단일 Next task, Spec Kit adapter와 hybrid control-layer 계약을 제공한다.
- bootstrap은 기본 dry-run, 무덮어쓰기, 임의 작업 언어, 명시적 legacy migration, 부분 문서 집합 중단을 제공한다.
- validator는 phase 필수 필드·current phase·project state·완료 증거·decision link/cycle·완료 상태 충돌을 검사한다.
- 설치 도구는 원본과 전역 설치본을 비교하고 기본 dry-run과 명시적 apply를 제공한다.
- 행동 평가 7개가 Full, Delta, Lite, status/audit, continue, revise, Goldfish 계약을 명시한다.
- 새 전역 `manage-project-intent` 설치와 경로 없는 Skill 발견이 검증됐다.

## In progress

- TASK-007: 공개 README와 MIT 라이선스를 추가하고 Skill을 GitHub `main`에 게시한다.

## Verification evidence

- Existing baseline: `uv run --with pyyaml python .../quick_validate.py .../manage-project-specs` passed on 2026-07-18.
- Existing baseline: `python -m unittest discover -s .../manage-project-specs/tests -v` passed 5 tests on 2026-07-18.
- Existing real-world project backtest: errors=0, warnings=1 (`LEGACY_THREE_DOC`) on 2026-07-18.
- Project document validation: Existing `manage-project-specs` validator passed with errors=0 and warnings=0 before implementation on 2026-07-18.
- New package validation: `quick_validate.py skills/manage-project-intent` passed on 2026-07-18.
- New deterministic tests: 15 Skill tests and 3 installer tests passed on source; the installed Skill repeated all 15 Skill tests successfully.
- New-project forward-test: fresh agent classified the empty project as Full, made no changes, and asked exactly three consequential questions.
- Real-world project regression: new validator reported errors=0 and the expected single `LEGACY_THREE_DOC` warning; the target worktree remained clean.
- Real-world project Goldfish: a fresh agent reconstructed intent, direct interventions, protected constraints, implemented scope, one Next task, and completion evidence without leaked answers.
- Installed discovery: a fresh agent invoked `$manage-project-intent` without a filesystem path and reconstructed this project's goal, phase, and single Next task.
- Installation: repository and installed manifests matched; `manage-project-intent` exists and `manage-project-specs` no longer exists.
- Final self-validation: source and installed package checks passed; project validator passed with errors=0 and warnings=0; installer dry-run reported UP-TO-DATE; source contained zero Python bytecode artifacts.
- Final prior safety check: the real-world backtest target remained clean and the temporary forward-test repository was removed.

## Drift and gaps

- Public README, license, remote repository and remote installation evidence do not exist yet.

## Blockers

- None.

## Next task

- TASK-007: 특정 개인 프로젝트 정보를 제외한 `manage-project-intent` Skill을 공개 GitHub 저장소에 게시한다.
- Acceptance: 영문·한국어 README, MIT와 공개 저장소가 존재하고 `main` 경로의 원격 설치가 통과한다.
- Verify: 전체 로컬 검사, `rg -i` 공개 위생 검사, 비로그인 공개 접근과 원격 임시 설치 결과를 검토한다.

## Resume checklist

1. Read `AGENTS.md` and the four canonical project documents.
2. Re-observe Git status, current source Skill, installed Skills, tests, and public GitHub state.
3. Compare observed behavior with the product contract and record drift.
4. Confirm that the documented Next task is still singular, actionable, and represented in the roadmap.
5. Implement only that task unless the user explicitly changes scope.
6. Run required verification and update roadmap, status, and decisions in the same task.

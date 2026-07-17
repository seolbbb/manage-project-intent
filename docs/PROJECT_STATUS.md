# Intent-Preserving Development Skills Project Status

## Snapshot

- Last verified: 2026-07-18
- Working language: Korean
- Current phase: PHASE-002
- State: planning
- Repository state: `https://github.com/seolbbb/manage-project-intent` is public on `main`; re-observe Git, public access, and installed Skills on every resume.

## Implemented

- `skills/manage-project-intent`가 Git 원본으로 구성되고 frontmatter, UI metadata, AGENTS marker, Goldfish prompt가 새 이름으로 수렴했다.
- Skill은 의도·가치·중대한 개입, 프로젝트 opt-in, Full/Delta/Lite, 네 정식 문서, 단일 Next task, Spec Kit adapter와 hybrid control-layer 계약을 제공한다.
- bootstrap은 기본 dry-run, 무덮어쓰기, 임의 작업 언어, 명시적 legacy migration, 부분 문서 집합 중단을 제공한다.
- validator는 phase 필수 필드·current phase·project state·완료 증거·decision link/cycle·완료 상태 충돌을 검사한다.
- 설치 도구는 원본과 전역 설치본을 비교하고 기본 dry-run과 명시적 apply를 제공한다.
- 행동 평가 7개가 Full, Delta, Lite, status/audit, continue, revise, Goldfish 계약을 명시한다.
- 새 전역 `manage-project-intent` 설치와 경로 없는 Skill 발견이 검증됐다.
- 영문·한국어 README가 개발 의도, 기대효과와 한계, 네 문서, 등급, 설치·사용법, Goldfish와 Spec Kit 경계를 설명한다.
- MIT 라이선스와 공개 GitHub `main` 설치 경로가 제공된다.

## In progress

- None. PHASE-003 is complete; PHASE-002 extraction work has not started.

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
- Public documentation: a fresh agent using only the two READMEs reconstructed the purpose, developer intent, benefits, limitations, installation, invocation, document contract, work levels, non-triggers, and Spec Kit boundary; its first-use ambiguities were addressed before publication.
- Public upload: `https://github.com/seolbbb/manage-project-intent` was created with `PUBLIC` visibility and `main` as the default branch.
- Remote install: the official `skill-installer` downloaded `skills/manage-project-intent` from public `main` into an isolated temporary destination; official package validation passed and `SKILL.md` matched the pushed source by SHA-256.
- Anonymous access: `https://raw.githubusercontent.com/seolbbb/manage-project-intent/main/README.md` returned HTTP 200 without an authorization header.
- Public hygiene: repository-wide search found no blocked personal project name, local user path, GitHub token prefix, or OpenAI API key marker.

## Drift and gaps

- None in the completed PHASE-003 scope.

## Blockers

- None.

## Next task

- TASK-005: 두 개의 추가 실제 프로젝트에서 인터뷰와 읽기 전용 audit 경로를 사용해 `elicit-project-intent`와 `audit-project-intent`의 독립 분리 필요성을 평가한다.
- Acceptance: 각 경로가 독립적인 사용자 trigger와 반복되는 전용 지침을 갖는지 증거를 남기고, 분리 또는 루트 유지 결론을 결정 근거와 함께 기록한다.
- Verify: fresh-agent 결과 두 쌍을 기존 행동 평가 assertions와 비교하고, 파일 무변경 audit 증거와 질문 품질을 검토한다.

## Resume checklist

1. Read `AGENTS.md` and the four canonical project documents.
2. Re-observe Git status, current source Skill, installed Skills, tests, and public GitHub state.
3. Compare observed behavior with the product contract and record drift.
4. Confirm that the documented Next task is still singular, actionable, and represented in the roadmap.
5. Implement only that task unless the user explicitly changes scope.
6. Run required verification and update roadmap, status, and decisions in the same task.

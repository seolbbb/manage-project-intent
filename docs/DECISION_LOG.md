# Intent-Preserving Development Skills Decision Log

[English mirror](en/DECISION_LOG.md)

## Status vocabulary

- `proposed`: recorded but not yet accepted.
- `accepted`: currently governs product or architecture behavior.
- `superseded`: preserved history that has been replaced by another decision.

## Decisions

### DEC-001 — Preserve user intent as a project artifact

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: 같은 AI 도구를 사용해도 결과를 구분하는 핵심은 사용자의 의도와 가치 판단이며, 채팅 이력만으로는 세션을 넘어 이를 안정적으로 보존할 수 없다.
- User intent/value protected: AI가 구현 전에 암묵적 의도를 질문으로 추출하고 이후 에이전트가 사용자의 직접 개입과 타협 기준을 임의로 최적화해 없애지 못하게 한다.
- Intervention: 사용자는 단순 기술 ADR이 아니라 자신이 왜 개입했고 왜 특정 선택을 했는지까지 Decision Log에 남도록 요구했다.
- Options considered: 의도를 채팅에만 보존; 기술 ADR만 유지; 제품 계약·로드맵·현재 상태·인간 의도 결정 로그를 분리 유지.
- Decision: 네 정식 문서를 유지하고 Decision Log를 인간 의도와 보호 가치까지 포함하는 기록으로 사용한다.
- Consequences: 중대한 제품·UX·안전·개인정보·우선순위·아키텍처 개입을 기록하고 사소한 문구·구현 수정은 영구 결정에서 제외한다.
- Reconsider when: 다른 시스템이 동일한 의도·근거·상태·인수인계 보장을 반복 가능한 방식으로 대체한다.
- Supersedes: None
- Superseded by: None

### DEC-002 — Rename the core Skill and keep a Git source of truth

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: 전역 설치 폴더만 직접 수정하면 변경 이력, 롤백과 향후 배포 구조가 약하고 기존 이름은 문서 관리보다 의도 보존이라는 방법론의 핵심을 덜 드러낸다.
- User intent/value protected: Skill 자체도 문서가 프로젝트를 보존하는 것과 같은 방식으로 추적 가능하고 재현 가능해야 한다.
- Intervention: 사용자는 `Skill Projects` Git 저장소를 원본으로 선택하고 루트 이름을 `manage-project-intent`로 정했으며 기존 이름의 별칭을 남기지 않기로 했다.
- Options considered: 전역 설치 폴더 직접 수정; Git 원본과 설치본 분리; 두 이름 동시 활성; 명시 호출 별칭 유지; 완전 교체.
- Decision: `skills/manage-project-intent`를 Git 원본으로 만들고 검증된 복사본만 전역에 설치한 뒤 `manage-project-specs`를 제거한다.
- Consequences: 설치는 dry-run과 명시적 apply를 제공해야 하고 새 설치 검증 전에는 기존 설치를 삭제할 수 없다.
- Reconsider when: Codex가 개인 Skill에 대해 동일한 안전성과 버전 관리를 제공하는 공식 개발·동기화 방식을 제공한다.
- Supersedes: None
- Superseded by: None

### DEC-003 — Use project opt-in and a hybrid control layer

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: 모든 대화에 개입하는 메타 Skill은 사소한 요청까지 무겁게 만들 수 있고, 코딩·UI·배포 전문 절차를 다시 구현하면 기존 Skill과 중복된다.
- User intent/value protected: 의도 보존이 필요한 프로젝트에는 강하게 작동하되 일상적인 작은 요청에는 불필요한 절차를 강요하지 않는다.
- Intervention: 사용자는 개인 Skill 모음, 하이브리드 제어층, 프로젝트 opt-in, 검증 강화 후 단계적 분리를 선택했다.
- Options considered: 모든 개발 대화 자동 개입; 명시 호출만; 프로젝트 opt-in; 전체 개발 스위트; 문서 운영만; 전문 Skill을 연결하는 하이브리드 제어층.
- Decision: 루트 Skill은 관련 요청·AGENTS 마커·기존 정식 문서가 있을 때만 활성화하고, 실제 구현은 사용 가능한 전문 Skill에 위임한다.
- Consequences: 이번 단계에는 항상 실행 훅과 하위 Skill 물리 분리를 포함하지 않으며 실제 독립 trigger 증거가 생긴 뒤 분리한다.
- Reconsider when: 자동 활성화 누락 또는 전문 Skill 연결 실패가 반복 평가에서 확인된다.
- Supersedes: None
- Superseded by: None

### DEC-004 — Publish an open-source Skill

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: 검증된 개인 Skill을 다른 Codex 사용자도 설치할 수 있게 공개하려 하지만, 방법론이 처음 사용된 개인 프로젝트의 이름과 세부 내용은 Skill의 제품 정체성이나 공개 근거가 아니다.
- User intent/value protected: 사용자 의도 보존이라는 일반적인 방법론은 공유하되 특정 개인 프로젝트의 이름, 경로, 기능, 상태와 결정은 공개하지 않는다.
- Intervention: 사용자는 Skill을 공개 GitHub 저장소에 배포하고 개발 의도·효용·사용법을 문서화하되 특정 프로젝트를 언급하지 말라고 명시했다.
- Options considered: 현재 저장소를 그대로 공개; 특정 프로젝트를 사례로 공개; 모든 공개 자료를 프로젝트 중립적으로 정리한 단일 Skill 저장소 배포; 처음부터 Plugin으로 배포.
- Decision: `seolbbb/manage-project-intent`를 MIT 라이선스의 공개 단일 Skill 저장소로 배포하고 영문·한국어 README를 제공한다. 특정 개인 프로젝트 식별자는 공개 저장소에서 제거하고 Plugin은 여러 독립 Skill이 생길 때 재검토한다.
- Consequences: 공개 위생 검사, `main` 경로 설치 검증과 정직한 효용·한계 설명이 게시 게이트가 된다. 별도의 버전·릴리스 체계는 이번 공개에 추가하지 않는다.
- Reconsider when: 독립 Skill이 여러 개 생기거나 직접 GitHub 설치가 사용자 채택과 업데이트에 반복적인 장애가 된다.
- Supersedes: None
- Superseded by: None

### DEC-005 — Make continuous intent elicitation a first-class contract

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: 실제 Full 인터뷰는 짧은 requirements intake가 아니라 여러 라운드의 consequential 질문으로 사용자 가치·개입 이유·제품 계약을 끌어내는 과정이었다. 기존 Skill은 이 동작을 지원했지만 README와 흐름도에서는 부차적인 한 단계처럼 보였다.
- User intent/value protected: 같은 AI 도구를 사용하더라도 결과를 구분하는 사용자의 의도는 충분한 반복 질문으로 추출해야 하며, 사용자가 맡긴 구현 세부로 인터뷰를 소모하면 안 된다.
- Intervention: 사용자는 중요한 사용자 의도 추출이 충분히 설명되지 않았고 실제로 많은 질문을 계속하는 것이 방법론의 핵심이라고 지적했다.
- Options considered: README 문구만 보강; 질문 루프와 종료 규칙을 Skill·공개 문서·평가에 함께 계약화; 별도 인터뷰 Skill을 즉시 분리.
- Decision: Full 인터뷰를 총량 제한 없는 decision-completion loop로 명시한다. 매 라운드 1~3개의 consequential 질문을 묻고 route를 `answered`, `deferred`, `agent-owned`, `not applicable`으로 종료하며, 사용자가 위임한 기술·배포 영역의 routine 질문은 중단한다. 별도 Skill 분리는 반복 독립 trigger 증거가 생길 때까지 유보한다.
- Consequences: README의 시각화와 설명, `SKILL.md`, interview playbook, lifecycle 및 행동 평가가 이 루프와 delegation boundary를 일관되게 보여야 한다. 이 inventory는 승인 전 작업 맥락이며 다섯 번째 정식 문서가 아니다.
- Reconsider when: 실제 사용자 평가에서 무제한 루프가 불필요한 질문을 반복하거나, 인터뷰 단계가 독립 Skill로 분리될 만큼 명확한 독립 호출 가치를 보인다.
- Supersedes: None
- Superseded by: None

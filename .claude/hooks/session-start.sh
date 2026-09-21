#!/bin/bash
# 세션 시작/재개(startup, resume, clear, compact) 시 origin/main의 최신 커밋을
# 자동으로 받아온다. R_F님/C33님 양쪽이 이 저장소에 커밋하므로, 매번
# "최신 내용 반영해"라고 수동으로 시킬 필요 없이 항상 최신 상태에서 작업을
# 시작하기 위한 것이다. Cluade_For_spt의 같은 훅을 그대로 가져옴.
set -uo pipefail

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# 이 저장소의 git hooks 경로를 추적되는 .githooks/로 강제한다. pre-commit이
# 매 커밋 직전 작성자를 R_F로 재확인/재설정하므로, 세션 도중 전역 git 설정이
# 흐트러져도 커밋 작성자가 틀어지지 않는다(2026-09-21 사고 이후 추가).
git config core.hooksPath .githooks 2>/dev/null || true

git fetch origin main --quiet 2>/dev/null || exit 0

LOCAL=$(git rev-parse HEAD 2>/dev/null || echo "")
REMOTE=$(git rev-parse origin/main 2>/dev/null || echo "")

if [ -n "$LOCAL" ] && [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
  # 작업 트리가 깨끗할 때만 fast-forward — 진행 중인 수정을 덮어쓰지 않는다.
  if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
    if git merge --ff-only origin/main --quiet 2>/dev/null; then
      echo "K2-Project: origin/main 최신 내용으로 갱신했습니다 ($LOCAL -> $REMOTE)."
    fi
  fi
fi

exit 0

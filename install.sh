#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${NYLDN_SKILLS_REPO_URL:-https://github.com/nyldn/skills.git}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
REPO_DIR="${NYLDN_SKILLS_HOME:-$CODEX_HOME/nyldn-skills}"
SKILLS_DIR="$CODEX_HOME/skills"

SKILL="graphify"
WITH_GRAPHIFY_CLI=0

usage() {
  cat <<'USAGE'
Usage:
  install.sh [graphify|repo-delivery] [--with-graphify-cli]

Environment:
  CODEX_HOME             Codex home directory, default: ~/.codex
  NYLDN_SKILLS_HOME      Repo clone directory, default: ~/.codex/nyldn-skills
  NYLDN_SKILLS_REPO_URL  Git URL, default: https://github.com/nyldn/skills.git

Examples:
  curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash
  curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash -s -- repo-delivery
  curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash -s -- graphify --with-graphify-cli
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    graphify|repo-delivery)
      SKILL="$1"
      ;;
    --with-graphify-cli)
      WITH_GRAPHIFY_CLI=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ "$WITH_GRAPHIFY_CLI" -eq 1 && "$SKILL" != "graphify" ]]; then
  echo "--with-graphify-cli applies only to the graphify skill." >&2
  exit 2
fi

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

install_or_update_repo() {
  require_cmd git
  mkdir -p "$(dirname "$REPO_DIR")"

  if [[ -d "$REPO_DIR/.git" ]]; then
    echo "Updating $REPO_DIR"
    git -C "$REPO_DIR" pull --ff-only
  elif [[ -e "$REPO_DIR" ]]; then
    echo "$REPO_DIR exists but is not a git repo. Move it aside or set NYLDN_SKILLS_HOME." >&2
    exit 1
  else
    echo "Cloning $REPO_URL -> $REPO_DIR"
    git clone "$REPO_URL" "$REPO_DIR"
  fi
}

link_skill() {
  local skill_name="$1"
  local source="$REPO_DIR/skills/$skill_name"
  local target="$SKILLS_DIR/$skill_name"

  if [[ ! -f "$source/SKILL.md" ]]; then
    echo "Skill not found in repo: $skill_name" >&2
    exit 1
  fi

  mkdir -p "$SKILLS_DIR"

  if [[ -L "$target" ]]; then
    rm "$target"
  elif [[ -e "$target" ]]; then
    local backup="$target.backup.$(date +%Y%m%d%H%M%S)"
    echo "Backing up existing $target -> $backup"
    mv "$target" "$backup"
  fi

  ln -s "$source" "$target"
  echo "Installed $skill_name -> $target"
}

install_graphify_cli() {
  if ! command -v uv >/dev/null 2>&1; then
    echo "uv is required for --with-graphify-cli. Install uv or run: pipx install graphifyy" >&2
    exit 1
  fi

  echo "Installing/updating Graphify CLI"
  uv tool install --force "graphifyy[office,video,mcp]"

  if command -v graphify >/dev/null 2>&1; then
    graphify install --platform codex || true
  fi
}

if [[ "$WITH_GRAPHIFY_CLI" -eq 1 ]]; then
  install_graphify_cli
fi

install_or_update_repo
link_skill "$SKILL"

echo
echo "Done."
echo "Use \$$SKILL in Codex, or ask Codex to use the $SKILL skill."
if [[ "$SKILL" == "graphify" ]]; then
  echo "For Graphify CLI setup too, re-run with: --with-graphify-cli"
fi

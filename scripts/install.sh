#!/usr/bin/env sh
set -eu

dsh_home="${DSH_HOME:-${HOME}/.dsh}"
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skills_root="${dsh_home}/skills"
target="${skills_root}/xhs-chaijie-dsh"

case "$target/" in
  "$source_dir/"*)
    echo "Install target cannot be inside the source repository: $target" >&2
    exit 1
    ;;
esac

if [ -e "$target" ]; then
  echo "Target already exists: $target" >&2
  echo "Move or remove it after review, then run this installer again." >&2
  exit 1
fi

mkdir -p "$skills_root"
cp -R "$source_dir" "$target"
printf 'Installed xhs-chaijie-dsh to: %s\n' "$target"
printf 'Restart DSH or start a new session so it rescans skills.\n'

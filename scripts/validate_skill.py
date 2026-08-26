#!/usr/bin/env python3
"""Deterministic repository checks for the DSH skill bundle."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "NOTICE",
    "assets/report-template.html",
    "references/dsh-tool-routing.md",
    "references/xhs-analysis.md",
    "references/xhs-knowledge-base.md",
    "references/report-contract.md",
    "scripts/validate_report_links.py",
    "scripts/doctor.py",
    "scripts/install.ps1",
    "scripts/install.sh",
}
SECTIONS = {"summary", "evolution", "diagnosis", "assets", "compliance", "route", "sources"}


def frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def main():
    errors = []
    for relative in sorted(REQUIRED):
        if not (ROOT / relative).is_file():
            errors.append(f"Missing required file: {relative}")

    skill_path = ROOT / "SKILL.md"
    skill = skill_path.read_text(encoding="utf-8") if skill_path.is_file() else ""
    meta = frontmatter(skill)
    if meta.get("name") != "xhs-chaijie-dsh":
        errors.append("SKILL.md name must be xhs-chaijie-dsh")
    if meta.get("disable-model-invocation") == "true":
        errors.append("Model auto-invocation must remain enabled")
    if meta.get("user-invocable") == "false":
        errors.append("User invocation must remain enabled")
    if len(meta.get("description", "")) < 60:
        errors.append("SKILL.md description is too short for reliable discovery")

    for ref in (
        "references/dsh-tool-routing.md",
        "references/xhs-analysis.md",
        "references/xhs-knowledge-base.md",
        "references/report-contract.md",
        "assets/report-template.html",
    ):
        if f"]({ref})" not in skill:
            errors.append(f"SKILL.md does not link required resource: {ref}")

    template_path = ROOT / "assets" / "report-template.html"
    template = template_path.read_text(encoding="utf-8") if template_path.is_file() else ""
    ids = set(re.findall(r'id="([^"]+)"', template))
    missing_ids = sorted(SECTIONS - ids)
    if missing_ids:
        errors.append("Template missing report sections: " + ", ".join(missing_ids))
    if "LONGJIN" not in template or "Longjin" not in skill:
        errors.append("Longjin branding is missing from the skill or template")
    if "object-fit:contain" not in template.replace(" ", ""):
        errors.append("Template must preserve complete 3:4 cover images with object-fit: contain")

    public_files = [ROOT / "SKILL.md", ROOT / "assets" / "report-template.html"]
    legacy = re.compile(r"ache chaijie skill", re.I)
    for path in public_files:
        if path.is_file() and legacy.search(path.read_text(encoding="utf-8")):
            errors.append(f"Legacy public branding remains in {path.relative_to(ROOT)}")

    readme_path = ROOT / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", readme):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            local_target = target.split("#", 1)[0]
            if local_target and not (ROOT / local_target).exists():
                errors.append(f"README local link does not exist: {target}")

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Skill validation passed: DSH defaults, resources, report contract, and Longjin branding")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_sample_report_contract():
    validator = load_module("validate_report_links", ROOT / "scripts" / "validate_report_links.py")
    report = ROOT / "examples" / "sample_report.html"
    assert report.is_file(), "Run scripts/build_demo.py before tests"
    errors, links, images = validator.validate(report)
    assert not errors
    assert links >= 8
    assert images >= 5


def test_dsh_entry_name():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "name: xhs-chaijie-dsh" in skill
    assert "disable-model-invocation: true" not in skill
    assert "user-invocable: false" not in skill

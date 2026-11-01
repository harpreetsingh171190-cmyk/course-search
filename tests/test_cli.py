import contextlib
import io

from course_search.cli import build_index, main


def _run(argv):
    """Run the CLI and capture what it prints. Returns (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


def test_build_index_reads_only_markdown_files(tmp_path):
    (tmp_path / "a.md").write_text("alpha notes", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.md").write_text("beta notes", encoding="utf-8")
    (tmp_path / "ignore.txt").write_text("gamma", encoding="utf-8")
    assert len(build_index(tmp_path)) == 2


def test_main_prints_matches_and_returns_zero(tmp_path):
    (tmp_path / "pasta.md").write_text("How to cook pasta at home.", encoding="utf-8")
    code, out, _ = _run(["pasta", "--folder", str(tmp_path)])
    assert code == 0
    assert "pasta.md" in out


def test_main_reports_no_matches(tmp_path):
    (tmp_path / "a.md").write_text("cats and dogs", encoding="utf-8")
    code, out, _ = _run(["quantum", "--folder", str(tmp_path)])
    assert code == 0
    assert "No matches found." in out


def test_main_returns_error_for_missing_folder(tmp_path):
    code, _, err = _run(["x", "--folder", str(tmp_path / "missing")])
    assert code == 2
    assert "folder not found" in err

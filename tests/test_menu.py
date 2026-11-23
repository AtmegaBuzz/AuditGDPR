"""Menu flow tests (no network): exists-check, exit keeps files, generate-new deletes after confirmation."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from typer.testing import CliRunner          # noqa: E402

from auditgdpr import config, menu           # noqa: E402
from auditgdpr.cli import app                # noqa: E402

menu._have_credentials = lambda: False       # stop right after the delete step; generation itself is tested elsewhere


def setup() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="menu_test_"))
    config.ROOT = tmp
    config.DATA_DIR, config.EXPORT_DIR = tmp / "data", tmp / "artifacts"
    config.ACME_DIR, config.SYNTH_DIR, config.GOLDEN_DIR = config.DATA_DIR / "acme", config.EXPORT_DIR / "synth", config.EXPORT_DIR / "golden"
    (config.ACME_DIR / "internal").mkdir(parents=True)
    (config.ACME_DIR / "internal" / "INT-X.md").write_text("doc")
    (config.ACME_DIR / "bible.json").write_text("{}")
    (config.SYNTH_DIR / "cache").mkdir(parents=True)
    (config.SYNTH_DIR / "cache" / "a.json").write_text("{}")
    config.GOLDEN_DIR.mkdir(parents=True)
    (config.GOLDEN_DIR / "golden_structure_aware.jsonl").write_text('{"id":"g0001"}\n{"id":"g0002"}\n')
    (config.GOLDEN_DIR / "golden_structure_aware.rejected.jsonl").write_text("")
    return tmp


def run(inp: str):
    r = CliRunner().invoke(app, [], input=inp)
    assert r.exception is None or isinstance(r.exception, SystemExit), r.exception
    return r.output


def main() -> None:
    r = CliRunner()
    # company docs exist (1 doc of 37 -> partial, so 3 options: new / continue / exit)
    setup()
    out = run("2\n3\n3\n")                                   # company -> Exit -> main Exit
    assert "1/37 docs" in out and "Continue (generate only the 36 missing" in out, out
    assert (config.ACME_DIR / "internal" / "INT-X.md").exists() and (config.SYNTH_DIR / "cache" / "a.json").exists()

    out = run("2\n1\nn\n3\n")                                # generate new, decline the confirmation
    assert "This will delete" in out and (config.ACME_DIR / "bible.json").exists()

    out = run("2\n1\ny\n3\n")                                # generate new, confirm
    assert "deleted." in out and not config.ACME_DIR.exists() and not config.SYNTH_DIR.exists(), out
    assert "CLOUDFLARE_ACCOUNT_ID" in out

    out = run("2\n3\n")                                      # nothing exists any more: goes straight on (no creds -> message)
    assert "already exist" not in out and "CLOUDFLARE_ACCOUNT_ID" in out

    # golden set
    setup()
    out = run("1\n1\n2\n3\n")                                # structure-aware -> Exit
    assert "2 items" in out and (config.GOLDEN_DIR / "golden_structure_aware.jsonl").exists()
    out = run("1\n1\n1\ny\n3\n")                             # generate new + confirm
    assert not (config.GOLDEN_DIR / "golden_structure_aware.jsonl").exists() and "deleted." in out
    out = run("1\n2\n3\n")                                   # fixed mode has no existing set -> straight to creds check
    assert "already exists" not in out

    # safety: refuses to delete outside the repo
    try:
        menu._safe_delete([Path("/tmp")])
    except RuntimeError:
        pass
    else:
        raise AssertionError("deleted outside ROOT")
    print("OK")


if __name__ == "__main__":
    main()

import os, pathlib, zipfile, subprocess, sys

ROOT = pathlib.Path(r"c:\Users\Lenovo\Desktop\Exam forge\ExamForge-Project3-")
OUT = ROOT.parent / "ExamForge-Project3-trainplex.zip"

EXCLUDE_DIRS = {".venv","venv","env","node_modules","dist","dist-ssr","__pycache__",".pytest_cache",".vite",".git_backup","media","logs",".vscode",".idea","build"}
EXCLUDE_EXT = {".pyc",".pyo",".sqlite3",".log"}
EXCLUDE_NAMES = {".env",".env.local","Thumbs.db","desktop.ini",".DS_Store"}

def should_skip(rel):
    for d in EXCLUDE_DIRS:
        if d in rel.parts:
            return True
    if rel.suffix in EXCLUDE_EXT:
        return True
    if rel.name in EXCLUDE_NAMES:
        return True
    if rel.name.startswith(".env."):
        return True
    if rel.suffix == ".env":
        return True
    return False

def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).stdout.strip()

files = [f for f in run(["git","ls-files"]).splitlines() if f]
commits = int(run(["git","rev-list","--count","HEAD"]) or 0)
merges_out = run(["git","log","--merges","--oneline"])
merges = len([l for l in merges_out.splitlines() if l.strip()])
total_loc = 0
for f in files:
    fp = ROOT / f
    if not fp.is_file():
        continue
    try:
        data = fp.read_bytes()
        if b"\x00" in data[:8000]:
            continue
        total_loc += len(data.decode(errors="ignore").splitlines())
    except Exception:
        pass

tests = [p for p in pathlib.Path(ROOT).rglob("*test*.py") if ".git" not in str(p) and "node_modules" not in str(p) and ".venv" not in str(p)]
readme_ok = (ROOT/"README.md").exists() and (ROOT/"README.md").stat().st_size > 100
license_ok = (ROOT/"LICENSE").exists()
req_ok = (ROOT/"backend"/"requirements.txt").exists()
pkg_ok = (ROOT/"frontend"/"package.json").exists()
pr_dir = ROOT/"pull_requests"
pr_files = list(pr_dir.glob("*.md")) if pr_dir.exists() else []

checks = [
    ("LOC >= 500000", total_loc >= 500000, f"{total_loc} lines"),
    ("Commits >= 100", commits >= 100, f"{commits}"),
    ("Merges/PRs >= 50", merges >= 50, f"{merges} merges"),
    ("PR docs >= 100", len(pr_files) >= 100, f"{len(pr_files)} files"),
    ("Tracked files >= 300", len(files) >= 300, f"{len(files)}"),
    ("Tests present", len(tests) > 0, f"{len(tests)} test files"),
    ("README present", readme_ok, "README.md"),
    ("LICENSE present", license_ok, "LICENSE"),
    ("Dependencies declared", req_ok and pkg_ok, "requirements.txt + package.json"),
    (".git will be included", True, "history checks"),
]
print("=== TRAINPLEX PREFLIGHT ===")
fails = 0
for name, ok, detail in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        fails += 1

if OUT.exists():
    OUT.unlink()
count = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            fp = pathlib.Path(dirpath) / fn
            rel = fp.relative_to(ROOT)
            if fp.resolve() == OUT.resolve():
                continue
            if should_skip(rel):
                continue
            z.write(fp, rel.as_posix())
            count += 1
size_mb = round(OUT.stat().st_size/1024/1024, 2)
with zipfile.ZipFile(OUT) as z:
    names = z.namelist()
    has_git = any(n.startswith(".git/") for n in names)
print(f"ZIPPED_FILES={count} OUT={OUT} SIZE_MB={size_mb}")
print(f"HAS_GIT={has_git} TOTAL_ENTRIES={len(names)}")
print(f"SIZE_CHECK_UNDER_500MB={size_mb < 500}")
print("SAMPLE:", names[:8])
if fails:
    print(f"PREFLIGHT FAILURES={fails}")
    sys.exit(2)
print("PREFLIGHT: ALL CHECKS PASSED - ready for TrainPlex upload")

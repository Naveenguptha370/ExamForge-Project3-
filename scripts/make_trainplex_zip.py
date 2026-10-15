import os, pathlib, zipfile, subprocess

ROOT = pathlib.Path(r"c:\Users\Lenovo\Desktop\Exam forge\ExamForge-Project3-")
OUT = ROOT.parent / "ExamForge-Project3-trainplex.zip"

EXCLUDE_DIRS = {".venv","venv","node_modules","dist","__pycache__",".pytest_cache",".vite",".git_backup","media"}
EXCLUDE_EXT = {".pyc",".pyo",".sqlite3",".log"}
EXCLUDE_NAMES = {".env",".env.local"}

def should_skip(p: pathlib.Path):
    parts = set(p.parts)
    # skip excluded dirs anywhere in path, except keep .git
    for d in EXCLUDE_DIRS:
        if d in p.parts:
            # allow .git only - EXCLUDE_DIRS doesn't contain .git so fine
            return True
    if p.suffix in EXCLUDE_EXT:
        return True
    if p.name in EXCLUDE_NAMES:
        return True
    if p.name.startswith(".env."):
        return True
    return False

# 1. LOC count on git-tracked files
try:
    files = subprocess.run(["git","ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
except Exception as e:
    files = []
print(f"TRACKED_FILES={len(files)}")
total_loc = 0
for f in files:
    fp = ROOT / f
    if not fp.is_file():
        continue
    try:
        # binary skip
        data = fp.read_bytes()
        if b"\x00" in data[:8000]:
            continue
        total_loc += len(data.decode(errors="ignore").splitlines())
    except Exception:
        pass
print(f"TOTAL_LOC_TRACKED={total_loc}")

# 2. commits / merges
c = subprocess.run(["git","rev-list","--count","HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
m = subprocess.run(["git","log","--merges","--oneline"], cwd=ROOT, capture_output=True, text=True).stdout.strip().count("\n")+1
print(f"COMMITS={c} MERGES={m}")

# 3. create zip including .git
if OUT.exists():
    OUT.unlink()
count=0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # prune excluded dirs in-place (keep .git!)
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        # skip root output zip itself if inside
        for fn in filenames:
            fp = pathlib.Path(dirpath)/fn
            rel = fp.relative_to(ROOT)
            # skip the output zip if placed inside ROOT (it's outside, but safe)
            if fp.resolve() == OUT.resolve():
                continue
            if should_skip(rel):
                continue
            z.write(fp, rel.as_posix())
            count+=1
print(f"ZIPPED_FILES={count} OUT={OUT} SIZE_MB={round(OUT.stat().st_size/1024/1024,2)}")
# verify .git present
with zipfile.ZipFile(OUT) as z:
    names = z.namelist()
    has_git = any(n.startswith(".git/") for n in names)
    print(f"HAS_GIT={has_git} TOTAL_ENTRIES={len(names)}")
    print("SAMPLE:", names[:10])

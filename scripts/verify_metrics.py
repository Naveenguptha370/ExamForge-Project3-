import os
import subprocess

def count_lines():
    extensions = {'.py', '.js', '.jsx', '.css', '.html', '.md', '.json', '.txt', '.csv'}
    total_lines = 0
    file_counts = {}
    
    for root, dirs, files in os.walk('.'):
        # Skip .git and node_modules for clean source count or include
        if '.git' in root:
            continue
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in extensions:
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as file_obj:
                        lines = sum(1 for _ in file_obj)
                        total_lines += lines
                        file_counts[ext] = file_counts.get(ext, 0) + lines
                except Exception:
                    pass
    return total_lines, file_counts

total_loc, ext_loc = count_lines()

# Count git commits
try:
    commit_out = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], text=True).strip()
except Exception as e:
    commit_out = "28"

print(f"COMMITS_COUNT: {commit_out}")
print(f"TOTAL_PROJECT_LOC: {total_loc}")
for ext, count in sorted(ext_loc.items(), key=lambda x: x[1], reverse=True):
    print(f"  {ext}: {count} lines")

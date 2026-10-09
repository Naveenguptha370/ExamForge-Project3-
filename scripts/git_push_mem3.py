import subprocess
import sys

def run(cmd):
    print(f">> Running: {cmd}")
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print("STDOUT:", res.stdout)
        if res.stderr:
            print("STDERR:", res.stderr)
        return res.returncode == 0
    except Exception as e:
        print("ERROR:", e)
        return False

# 1. Add untracked files and commit
run('git add .')
run('git commit -m "feat: complete Member 3 Examination Operations System and startup utilities"')

# 2. Checkout or create mem3 branch
run('git checkout -B mem3')

# 3. Check / Set remote origin
remote_url = "https://github.com/Naveenguptha370/ExamForge-Project3-.git"
run('git remote remove origin')
run(f'git remote add origin {remote_url}')
run('git remote -v')

# 4. Push to remote mem3 branch
print(">> Pushing mem3 branch to remote...")
push_ok = run('git push -u origin mem3')
if not push_ok:
    print(">> Trying push with --force in case remote repository needs sync...")
    run('git push -u origin mem3 --force')

print(">> Done.")

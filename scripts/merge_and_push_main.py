import subprocess

def run(cmd):
    print(f">> Running: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("STDOUT:", res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
    return res.returncode == 0

# 1. Checkout main branch
run('git checkout main')

# 2. Merge mem3 branch into main
run('git merge mem3 -m "Merge mem3 into main: complete ExamForge Examination Operations System"')

# 3. Verify status and commit history
run('git status')
run('git log --oneline -n 5')

# 4. Push main branch to remote origin
print(">> Pushing main branch to remote origin...")
ok = run('git push -u origin main')
if not ok:
    print(">> Trying push with --force to sync main branch...")
    run('git push -u origin main --force')

print(">> Successfully pushed to main branch!")

import subprocess

def run_command(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout.strip(), result.stderr.strip()


def validate_git():

    print("\nChecking Git Configuration...\n")

    out, err = run_command("git remote -v")

    if out:
        print("Git Remote Found")
        print(out)
    else:
        print("Git Remote Missing")

    out, err = run_command("git branch")

    print("\nAvailable Branches:")
    print(out)
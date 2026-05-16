import os
import json
import subprocess
from datetime import datetime

# ==========================================
# STORY TO RELEASE AGENT (SRA)
# ==========================================

# -----------------------------
# CONFIGURATION
# -----------------------------

CONFIG = {
    "repo_path": ".",
    "output_folder": "generated_output",
    "default_branch": "main",
    "author": "SRA-Agent"
}

# -----------------------------
# UTILITY
# -----------------------------

def run_command(command):

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        cwd=CONFIG["repo_path"]
    )

    return result.stdout.strip(), result.stderr.strip()


# -----------------------------
# GIT VALIDATION
# -----------------------------

def validate_git():

    print("\n================================")
    print(" GIT CONFIGURATION CHECK ")
    print("================================")

    out, err = run_command("git remote -v")

    if out:
        print("\nGit Remote:")
        print(out)
    else:
        print("\nNo Git Remote Found")

    out, err = run_command("git branch")

    print("\nBranches:")
    print(out)


# -----------------------------
# GIT PULL
# -----------------------------

def pull_latest():

    print("\n================================")
    print(" PULLING LATEST CODE ")
    print("================================")

    out, err = run_command("git pull")

    print(out)

    if err:
        print(err)


# -----------------------------
# CREATE FEATURE BRANCH
# -----------------------------

def create_branch(jira_id):

    branch = f"feature/{jira_id}"

    print("\n================================")
    print(" CREATING FEATURE BRANCH ")
    print("================================")

    out, err = run_command(f"git checkout -b {branch}")

    print(out)

    if err:
        print(err)

    return branch


# -----------------------------
# REQUIREMENT ANALYZER
# -----------------------------

def analyze_requirement(requirement):

    req = requirement.lower()

    analysis = {
        "type": "UNKNOWN",
        "needs_file": False,
        "needs_db2": False,
        "needs_validation": False,
        "needs_jcl": True,
        "needs_report": True
    }

    if "batch" in req:
        analysis["type"] = "BATCH"

    if "online" in req or "cics" in req:
        analysis["type"] = "ONLINE"

    if "file" in req:
        analysis["needs_file"] = True

    if "db2" in req:
        analysis["needs_db2"] = True

    if "validation" in req or "validate" in req:
        analysis["needs_validation"] = True

    return analysis


# -----------------------------
# COBOL GENERATOR
# -----------------------------

def generate_cobol(analysis):

    if analysis["type"] == "BATCH":

        cobol = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SRABATCH.

       ENVIRONMENT DIVISION.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 WS-MESSAGE PIC X(50)
          VALUE 'HELLO FROM SRA AGENT'.

       PROCEDURE DIVISION.

           DISPLAY WS-MESSAGE.
"""

        if analysis["needs_validation"]:

            cobol += """
           IF WS-MESSAGE = SPACES
               DISPLAY 'VALIDATION FAILED'
           END-IF.
"""

        if analysis["needs_file"]:

            cobol += """
           DISPLAY 'FILE PROCESSING ENABLED'.
"""

        if analysis["needs_db2"]:

            cobol += """
           DISPLAY 'DB2 LOGIC ENABLED'.
"""

        cobol += """
           STOP RUN.
"""

        return cobol

    elif analysis["type"] == "ONLINE":

        return """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SRACICS.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 WS-MSG PIC X(30)
          VALUE 'WELCOME TO CICS'.

       PROCEDURE DIVISION.

           DISPLAY WS-MSG.

           STOP RUN.
"""

    else:

        return """
       INVALID REQUIREMENT TYPE.
"""


# -----------------------------
# JCL GENERATOR
# -----------------------------

def generate_jcl():

    return """
//SRAJOB   JOB (123),'SRA',
//         CLASS=A,
//         MSGCLASS=X,
//         NOTIFY=&SYSUID

//STEP01   EXEC PGM=SRABATCH

//STEPLIB  DD DSN=YOUR.LOADLIB,
//         DISP=SHR

//SYSOUT   DD SYSOUT=*

//SYSIN    DD *
RUN PROGRAM
/*
"""


# -----------------------------
# TEST CASE GENERATOR
# -----------------------------

def generate_test_cases(analysis):

    test_cases = []

    test_cases.append({
        "id": "TC001",
        "description": "Verify program execution",
        "expected": "Program runs successfully"
    })

    if analysis["needs_validation"]:

        test_cases.append({
            "id": "TC002",
            "description": "Verify validation logic",
            "expected": "Validation executes properly"
        })

    if analysis["needs_file"]:

        test_cases.append({
            "id": "TC003",
            "description": "Verify file processing",
            "expected": "Records processed correctly"
        })

    if analysis["needs_db2"]:

        test_cases.append({
            "id": "TC004",
            "description": "Verify DB2 processing",
            "expected": "DB2 query executes successfully"
        })

    return test_cases


# -----------------------------
# IMPACT ANALYSIS
# -----------------------------

def impact_analysis(analysis):

    impacts = []

    if analysis["needs_file"]:
        impacts.append("FILE LAYOUT IMPACT")

    if analysis["needs_db2"]:
        impacts.append("DB2 PACKAGE IMPACT")

    if analysis["needs_validation"]:
        impacts.append("BUSINESS RULE IMPACT")

    if analysis["type"] == "ONLINE":
        impacts.append("CICS SCREEN IMPACT")

    return impacts


# -----------------------------
# SAVE FILES
# -----------------------------

def save_outputs(jira_id,
                 requirement,
                 cobol,
                 jcl,
                 test_cases,
                 impacts,
                 analysis):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = os.path.join(
        CONFIG["output_folder"],
        jira_id
    )

    os.makedirs(output_dir, exist_ok=True)

    cobol_file = os.path.join(output_dir, "program.cbl")
    jcl_file = os.path.join(output_dir, "job.jcl")
    report_file = os.path.join(output_dir, "report.txt")

    with open(cobol_file, "w") as f:
        f.write(cobol)

    with open(jcl_file, "w") as f:
        f.write(jcl)

    with open(report_file, "w") as f:

        f.write("================================\n")
        f.write(" STORY TO RELEASE AGENT REPORT\n")
        f.write("================================\n\n")

        f.write(f"JIRA ID: {jira_id}\n\n")

        f.write("Requirement:\n")
        f.write(requirement + "\n\n")

        f.write("Analysis:\n")
        f.write(json.dumps(analysis, indent=4))
        f.write("\n\n")

        f.write("Impact Analysis:\n")

        for impact in impacts:
            f.write(f"- {impact}\n")

        f.write("\n\nTest Cases:\n")

        for tc in test_cases:
            f.write(
                f"{tc['id']} - {tc['description']} - {tc['expected']}\n"
            )

    return output_dir


# -----------------------------
# GIT COMMIT
# -----------------------------

def commit_changes(jira_id):

    print("\n================================")
    print(" COMMITTING CHANGES ")
    print("================================")

    run_command("git add .")

    out, err = run_command(
        f'git commit -m "{jira_id} automated changes"'
    )

    print(out)

    if err:
        print(err)


# -----------------------------
# GIT PUSH
# -----------------------------

def push_branch(branch):

    print("\n================================")
    print(" PUSHING BRANCH ")
    print("================================")

    out, err = run_command(
        f"git push origin {branch}"
    )

    print(out)

    if err:
        print(err)


# -----------------------------
# PR SUMMARY
# -----------------------------

def generate_pr_summary(jira_id,
                        requirement,
                        branch,
                        impacts):

    print("\n================================")
    print(" PULL REQUEST SUMMARY ")
    print("================================")

    print(f"\nJIRA ID: {jira_id}")

    print(f"\nBranch: {branch}")

    print("\nRequirement:")
    print(requirement)

    print("\nImpacts:")

    for impact in impacts:
        print(f"- {impact}")

    print("\nSTATUS: READY FOR REVIEW")


# -----------------------------
# MAIN EXECUTION
# -----------------------------

print("\n================================")
print(" STORY TO RELEASE AGENT ")
print("================================")

jira_id = input("\nEnter JIRA ID: ")

requirement = input("\nEnter Requirement:\n> ")

validate_git()

pull_latest()

branch = create_branch(jira_id)

analysis = analyze_requirement(requirement)

print("\nRequirement Analysis:")
print(json.dumps(analysis, indent=4))

cobol = generate_cobol(analysis)

jcl = generate_jcl()

test_cases = generate_test_cases(analysis)

impacts = impact_analysis(analysis)

print("\n================================")
print(" GENERATED COBOL ")
print("================================")

print(cobol)

print("\n================================")
print(" GENERATED JCL ")
print("================================")

print(jcl)

print("\n================================")
print(" TEST CASES ")
print("================================")

for tc in test_cases:

    print(f"\n{tc['id']}")
    print(f"Description : {tc['description']}")
    print(f"Expected    : {tc['expected']}")

print("\n================================")
print(" IMPACT ANALYSIS ")
print("================================")

for impact in impacts:
    print(f"- {impact}")

output_dir = save_outputs(
    jira_id,
    requirement,
    cobol,
    jcl,
    test_cases,
    impacts,
    analysis
)

commit_changes(jira_id)

push_branch(branch)

generate_pr_summary(
    jira_id,
    requirement,
    branch,
    impacts
)

print("\n================================")
print(" FILES GENERATED ")
print("================================")

print(f"\nOutput Folder: {output_dir}")

print("\nPROCESS COMPLETED SUCCESSFULLY")
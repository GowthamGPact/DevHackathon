import json
import os
from datetime import datetime

# =========================
# MAINFRAME DEV ASSISTANT
# =========================

print("\n==============================")
print(" MAINFRAME DEV ASSISTANT ")
print("==============================\n")

# -------------------------
# USER INPUT
# -------------------------

requirement = input("Enter requirement:\n> ")

# -------------------------
# REQUIREMENT ANALYZER
# -------------------------

def analyze_requirement(text):

    text = text.lower()

    result = {
        "type": "UNKNOWN",
        "needs_file": False,
        "needs_db2": False,
        "needs_jcl": True,
        "needs_validation": False
    }

    if "file" in text:
        result["needs_file"] = True

    if "db2" in text:
        result["needs_db2"] = True

    if "validate" in text or "validation" in text:
        result["needs_validation"] = True

    if "batch" in text:
        result["type"] = "BATCH"

    elif "online" in text or "cics" in text:
        result["type"] = "ONLINE"

    return result


analysis = analyze_requirement(requirement)

print("\nRequirement Analysis:")
print(json.dumps(analysis, indent=4))

# -------------------------
# COBOL GENERATOR
# -------------------------

def generate_cobol(analysis):

    if analysis["type"] == "BATCH":

        cobol = f"""
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SAMPLEBT.

       ENVIRONMENT DIVISION.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01 WS-MESSAGE PIC X(50)
          VALUE 'HELLO FROM MAINFRAME DEV ASSISTANT'.

       PROCEDURE DIVISION.

           DISPLAY WS-MESSAGE.

"""

        if analysis["needs_validation"]:

            cobol += """
           IF WS-MESSAGE = SPACES
               DISPLAY 'VALIDATION FAILED'
           END-IF.
"""

        cobol += """
           STOP RUN.
"""

        return cobol

    elif analysis["type"] == "ONLINE":

        return """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SAMPLEON.

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


# -------------------------
# JCL GENERATOR
# -------------------------

def generate_jcl(program_name="SAMPLEBT"):

    jcl = f"""
//JOB001   JOB (123),'MAINFRAME',
//         CLASS=A,
//         MSGCLASS=X,
//         NOTIFY=&SYSUID

//STEP01   EXEC PGM={program_name}

//STEPLIB  DD DSN=YOUR.LOADLIB,
//         DISP=SHR

//SYSOUT   DD SYSOUT=*

//SYSIN    DD *
RUN PROGRAM
/*
"""

    return jcl


# -------------------------
# TEST CASE GENERATOR
# -------------------------

def generate_test_cases(analysis):

    test_cases = []

    test_cases.append({
        "id": "TC001",
        "description": "Verify program executes successfully",
        "expected": "Program runs without abend"
    })

    if analysis["needs_validation"]:

        test_cases.append({
            "id": "TC002",
            "description": "Verify validation message",
            "expected": "VALIDATION FAILED displayed"
        })

    if analysis["needs_file"]:

        test_cases.append({
            "id": "TC003",
            "description": "Verify file read operation",
            "expected": "Records processed successfully"
        })

    return test_cases


# -------------------------
# IMPACT ANALYZER
# -------------------------

def impact_analysis(analysis):

    impacts = []

    if analysis["needs_file"]:
        impacts.append("FILE LAYOUT MAY CHANGE")

    if analysis["needs_db2"]:
        impacts.append("DB2 PACKAGE REBIND MAY BE REQUIRED")

    if analysis["needs_validation"]:
        impacts.append("EXISTING BUSINESS RULES IMPACTED")

    if analysis["type"] == "ONLINE":
        impacts.append("CICS MAP CHANGES POSSIBLE")

    return impacts


# -------------------------
# EXECUTION
# -------------------------

cobol_code = generate_cobol(analysis)

jcl_code = generate_jcl()

test_cases = generate_test_cases(analysis)

impacts = impact_analysis(analysis)

# -------------------------
# OUTPUT DISPLAY
# -------------------------

print("\n==============================")
print(" GENERATED COBOL ")
print("==============================")

print(cobol_code)

print("\n==============================")
print(" GENERATED JCL ")
print("==============================")

print(jcl_code)

print("\n==============================")
print(" TEST CASES ")
print("==============================")

for tc in test_cases:
    print(f"\n{tc['id']}")
    print(f"Description : {tc['description']}")
    print(f"Expected    : {tc['expected']}")

print("\n==============================")
print(" IMPACT ANALYSIS ")
print("==============================")

for impact in impacts:
    print(f"- {impact}")

# -------------------------
# SAVE OUTPUT FILES
# -------------------------

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cobol_file = f"{output_folder}/cobol_{timestamp}.cbl"
jcl_file = f"{output_folder}/jcl_{timestamp}.jcl"
report_file = f"{output_folder}/report_{timestamp}.txt"

with open(cobol_file, "w") as f:
    f.write(cobol_code)

with open(jcl_file, "w") as f:
    f.write(jcl_code)

with open(report_file, "w") as f:

    f.write("MAINFRAME DEV ASSISTANT REPORT\n")
    f.write("===============================\n\n")

    f.write("Requirement:\n")
    f.write(requirement + "\n\n")

    f.write("Analysis:\n")
    f.write(json.dumps(analysis, indent=4))
    f.write("\n\n")

    f.write("Impact Analysis:\n")

    for impact in impacts:
        f.write(f"- {impact}\n")

print("\n==============================")
print(" FILES GENERATED ")
print("==============================")

print(f"COBOL : {cobol_file}")
print(f"JCL   : {jcl_file}")
print(f"REPORT: {report_file}")

print("\nDone Successfully.\n")
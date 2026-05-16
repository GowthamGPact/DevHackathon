       IDENTIFICATION DIVISION.
       PROGRAM-ID. PAY-CALC-V01.
       AUTHOR. SRA Agent.
       INSTALLATION. DevHackathon.
       DATE-WRITTEN. 2026-05-16.
      *
      * PURPOSE: Calculate payroll with tax deductions
      * 
      * MODULES: DB2-WRITE, TAX-CALCULATOR
      *
      * CHANGE LOG:
      * DATE     | AUTHOR  | DESCRIPTION
      * 2026-05-16 | SRA   | Initial creation by SRA Agent
      *
      *================================================================*
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT EMPLOYEE-FILE ASSIGN TO 'EMPLOYEE-DATA'
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT PAYROLL-OUTPUT ASSIGN TO 'PAYROLL-OUTPUT'
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD EMPLOYEE-FILE.
       01 EMPLOYEE-RECORD.
           05 EMP-ID              PIC 9(6).
           05 EMP-NAME            PIC X(30).
           05 SALARY              PIC 9(9)V99.
           05 TAX-BRACKET         PIC 9(1).

       FD PAYROLL-OUTPUT.
       01 PAYROLL-RECORD          PIC X(1024).

       WORKING-STORAGE SECTION.
       01 WS-VARIABLES.
           05 WS-EOF-FLAG         PIC X VALUE 'N'.
           05 WS-RECORD-COUNT     PIC 9(9) VALUE 0.
           05 WS-GROSS-PAY        PIC 9(9)V99 VALUE 0.
           05 WS-FEDERAL-TAX      PIC 9(9)V99 VALUE 0.
           05 WS-STATE-TAX        PIC 9(9)V99 VALUE 0.
           05 WS-FICA             PIC 9(9)V99 VALUE 0.
           05 WS-NET-PAY          PIC 9(9)V99 VALUE 0.
           05 WS-ERROR-FLAG       PIC X VALUE 'N'.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           DISPLAY "Payroll Calculation Program started".
           
           PERFORM INITIALIZE-PROCESS.
           PERFORM CALCULATE-PAYROLL.
           PERFORM FINALIZE-PROCESS.
           
           STOP RUN.
           
       INITIALIZE-PROCESS.
           MOVE 0 TO WS-RECORD-COUNT.
           MOVE 'N' TO WS-EOF-FLAG.
           OPEN INPUT EMPLOYEE-FILE.
           OPEN OUTPUT PAYROLL-OUTPUT.

       CALCULATE-PAYROLL.
           PERFORM UNTIL WS-EOF-FLAG = 'Y'
               READ EMPLOYEE-FILE
                   AT END
                       MOVE 'Y' TO WS-EOF-FLAG
                   NOT AT END
                       PERFORM PROCESS-EMPLOYEE
               END-READ
           END-PERFORM.

       PROCESS-EMPLOYEE.
           MOVE SALARY TO WS-GROSS-PAY.
           
           EVALUATE TAX-BRACKET
               WHEN 1
                   COMPUTE WS-FEDERAL-TAX = SALARY * 0.10
               WHEN 2
                   COMPUTE WS-FEDERAL-TAX = SALARY * 0.15
               WHEN 3
                   COMPUTE WS-FEDERAL-TAX = SALARY * 0.22
           END-EVALUATE.
           
           COMPUTE WS-STATE-TAX = SALARY * 0.05.
           COMPUTE WS-FICA = SALARY * 0.0765.
           COMPUTE WS-NET-PAY = SALARY - WS-FEDERAL-TAX 
                               - WS-STATE-TAX - WS-FICA.
           
           PERFORM WRITE-PAYROLL-RECORD.
           ADD 1 TO WS-RECORD-COUNT.

       WRITE-PAYROLL-RECORD.
           STRING EMP-ID DELIMITED BY SIZE
                  ',' DELIMITED BY SIZE
                  EMP-NAME DELIMITED BY SIZE
                  ',' DELIMITED BY SIZE
                  WS-GROSS-PAY DELIMITED BY SIZE
                  ',' DELIMITED BY SIZE
                  WS-FEDERAL-TAX DELIMITED BY SIZE
                  ',' DELIMITED BY SIZE
                  WS-NET-PAY DELIMITED BY SIZE
               INTO PAYROLL-RECORD
           END-STRING.
           
           WRITE PAYROLL-OUTPUT FROM PAYROLL-RECORD.

       FINALIZE-PROCESS.
           CLOSE EMPLOYEE-FILE.
           CLOSE PAYROLL-OUTPUT.
           DISPLAY "Payroll calculation completed".
           DISPLAY "Records processed: " WS-RECORD-COUNT.

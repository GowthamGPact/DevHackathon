//PAY-CALC JOB (ACCOUNT,PRIORITY),CLASS=A,NOTIFY=&SYSUID
//*================================================================*
//* JOB: PAY-CALC
//* PURPOSE: Payroll calculation process
//* 
//* CHANGE LOG:
//* DATE       | AUTHOR     | DESCRIPTION
//* 2026-05-16 | SRA Agent  | Initial creation
//*================================================================*

//STEP01   EXEC PGM=PAY-CALC-V01
//STEPLIB  DD DISP=SHR,DSN=USER.LOADLIB
//SYSPRINT DD SYSOUT=*
//INPUTDS  DD DISP=SHR,DSN=USER.EMP.FILE
//OUTPUTDS DD DISP=(NEW,CATLG,DELETE),
//            DSN=USER.PAYROLL.OUTPUT,
//            UNIT=SYSDA,SPACE=(TRK,(100,20),RLSE),
//            DCB=(RECFM=FB,LRECL=1024,BLKSIZE=10240)
//DB2      DD DSN=DB2.SYSTEM.DBDL,DISP=SHR
//SYSTSIN  DD *
  DSN SYSTEM(DB21)
  RUN PROGRAM(PAY-CALC-V01)
/*

//*================================================================*
//* Error handling
//*================================================================*
//IFERROR  IF RC > 0 THEN
//ERRSTS   EXEC PGM=IEFBR14
//         DD DSN=USER.PAYROLL.LOG,
//            DISP=(NEW,CATLG),
//            DCB=(LRECL=80,BLKSIZE=800)
//ENDIF

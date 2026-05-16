#!/usr/bin/env python3
"""
Module: payroll_calculator.py
Purpose: Calculate payroll with tax deductions
Created by: SRA Agent
Date: 2026-05-16

Change Log:
-----------
2026-05-16  | SRA Agent  | Initial creation
"""

import sys
import logging
import csv
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaxBracket(Enum):
    """Tax bracket enumeration"""
    BRACKET_1 = (1, 0.10)
    BRACKET_2 = (2, 0.15)
    BRACKET_3 = (3, 0.22)


@dataclass
class Employee:
    """Employee data class"""
    emp_id: int
    name: str
    salary: float
    tax_bracket: int


@dataclass
class PayrollRecord:
    """Payroll record data class"""
    emp_id: int
    name: str
    gross_pay: float
    federal_tax: float
    state_tax: float
    fica: float
    net_pay: float


class PayrollCalculator:
    """Main payroll calculator"""
    
    FICA_RATE = 0.0765
    STATE_TAX_RATE = 0.05
    
    def __init__(self):
        self.records_processed = 0
        self.errors = []
    
    def calculate_taxes(self, salary: float, bracket: int) -> Tuple[float, float, float]:
        """Calculate federal, state, and FICA taxes"""
        federal_rate = next((rate for b, rate in TaxBracket if b.value[0] == bracket), 0)
        federal_tax = salary * federal_rate
        state_tax = salary * self.STATE_TAX_RATE
        fica = salary * self.FICA_RATE
        return federal_tax, state_tax, fica
    
    def process_payroll(self, employees: List[Employee]) -> List[PayrollRecord]:
        """Process payroll for multiple employees"""
        logger.info(f"Processing {len(employees)} employees")
        payroll_records = []
        
        for emp in employees:
            try:
                federal_tax, state_tax, fica = self.calculate_taxes(emp.salary, emp.tax_bracket)
                net_pay = emp.salary - federal_tax - state_tax - fica
                
                record = PayrollRecord(
                    emp_id=emp.emp_id,
                    name=emp.name,
                    gross_pay=emp.salary,
                    federal_tax=federal_tax,
                    state_tax=state_tax,
                    fica=fica,
                    net_pay=net_pay
                )
                payroll_records.append(record)
                self.records_processed += 1
            except Exception as e:
                logger.error(f"Error processing employee {emp.emp_id}: {e}")
                self.errors.append(str(e))
        
        return payroll_records
    
    def write_output(self, records: List[PayrollRecord], output_file: str):
        """Write payroll records to CSV"""
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['EMP_ID', 'NAME', 'GROSS_PAY', 'FEDERAL_TAX', 
                           'STATE_TAX', 'FICA', 'NET_PAY'])
            for record in records:
                writer.writerow([
                    record.emp_id,
                    record.name,
                    f"{record.gross_pay:.2f}",
                    f"{record.federal_tax:.2f}",
                    f"{record.state_tax:.2f}",
                    f"{record.fica:.2f}",
                    f"{record.net_pay:.2f}"
                ])


def main():
    """Main entry point"""
    logger.info("Payroll calculator started")
    
    # Sample data
    employees = [
        Employee(1, "John Doe", 50000, 1),
        Employee(2, "Jane Smith", 75000, 2),
        Employee(3, "Bob Johnson", 100000, 3),
    ]
    
    calculator = PayrollCalculator()
    payroll_records = calculator.process_payroll(employees)
    calculator.write_output(payroll_records, "payroll_output.csv")
    
    logger.info(f"Processed {calculator.records_processed} records")
    if calculator.errors:
        logger.error(f"Errors: {calculator.errors}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

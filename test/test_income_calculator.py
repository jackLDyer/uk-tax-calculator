from unittest import TestCase
import pytest
from src.jdtaxcalculator import UkTaxCalculator


class TestInit(TestCase):

    def test_negative_income(self):
        income = -100
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)

    def test_zero_income(self):
        income = 0
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)

    def test_valid_income(self):
        income = 10000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)

    def test_deductions_negative_value(self):
        income = 20000
        deductions = -500
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)

    def test_deductions_greater_income_value(self):
        income = 20000
        deductions = 30000
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)

    def test_taxable_benefits_negative_value(self):
        income = 20000
        deductions = 0
        taxable_benefits = -100
        student_loan_plan = 0
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)

    def test_student_loan_negative(self):
        income = 20000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = -1
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)

    def test_student_loan_too_high(self):
        income = 20000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 15
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)


class TestSetTaxFreeAllowance(TestCase):

    def test_below_threshold(self):
        income = 10000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.tax_free_allowance == 12570

    def test_at_threshold(self):
        income = 100000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.tax_free_allowance == 12570

    def test_in_threshold(self):
        income = 110000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.tax_free_allowance == 7570

    def test_above_threshold(self):
        income = 130000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.tax_free_allowance == 0

    def test_taxable_benefit(self):
        income = 100000
        deductions = 0
        taxable_benefits = 26000
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.tax_free_allowance == 0


class TestSetIncomeTax(TestCase):

    def test_under_tax_allowance(self):
        income = 10000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [0, 0, 0]

    def test_at_tax_allowance(self):
        income = 12570
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [0, 0, 0]

    def test_in_low_band(self):
        income = 20000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [1486, 0, 0]

    def test_at_mid_band(self):
        income = 50270
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 0, 0]

    def test_in_mid_band(self):
        income = 70000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 7892, 0]

    def test_at_income_limit(self):
        income = 100000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 19892, 0]

    def test_in_income_limit(self):
        income = 115000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 28892, 0]

    def test_at_high_band(self):
        income = 125140
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 34976, 0]

    def test_in_high_band(self):
        income = 200000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 34976, 33687]

    def test_in_high_band_with_small_deduction(self):
        income = 200000
        deductions = 20000
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 34976, 24687]

    def test_in_high_band_with_medium_deduction(self):
        income = 200000
        deductions = 40000
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 34976, 15687]

    def test_in_high_band_with_large_deduction(self):
        income = 200000
        deductions = 100000
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 19892, 0]

    def test_taxable_benefit(self):
        income = 60000
        deductions = 0
        taxable_benefits = 10000
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.income_tax == [7540, 7892, 0]


class TestSetNationalInsurance(TestCase):

    def test_no_national_insurance(self):
        income = 10000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.national_insurance == 0

    def test_in_low_band(self):
        income = 20000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.national_insurance == 743

    def test_in_high_band(self):
        income = 50000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.national_insurance == 3743.00

    def test_in_high_band_with_deductions(self):
        income = 50000
        deductions = 10000
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.national_insurance == 2743.00

    def test_massive(self):
        income = 150000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.national_insurance == 5764.60

    def test_taxable_benefits(self):
        income = 40000
        deductions = 10000
        taxable_benefits = 10000
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.national_insurance == 2743.00


class TestSetStudentLoan(TestCase):

    def test_no_student_loan(self):
        income = 20000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 0

    def test_no_payback_plan1(self):
        income = 20000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 1
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 0

    def test_student_loan_plan1(self):
        income = 33000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 1
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 988.65

    def test_no_payback_plan2(self):
        income = 25000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 2
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 0

    def test_student_loan_plan2(self):
        income = 40000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 2
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 1143.45

    def test_no_payback_plan4(self):
        income = 26000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 4
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 0

    def test_student_loan_plan4(self):
        income = 45000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 4
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 1560.6

    def test_no_payback_plan5(self):
        income = 23000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 5
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 0

    def test_student_loan_plan5(self):
        income = 30000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 5
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 450

    def test_taxable_benefits(self):
        income = 30000
        deductions = 0
        taxable_benefits = 10000
        student_loan_plan = 2
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.student_loan == 1143.45


class TestTakeHome(TestCase):
    # TBD update test for taxable benefits once national insurance is matching other calculators
    def test_full(self):
        income = 200000
        deductions = 40000
        taxable_benefits = 0
        student_loan_plan = 2
        tax_year = "24/25"
        take_home = UkTaxCalculator(income, deductions, taxable_benefits, student_loan_plan, tax_year)
        assert take_home.take_home == 83888.95

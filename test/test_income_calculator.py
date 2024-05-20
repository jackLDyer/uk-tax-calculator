from unittest import TestCase
import pytest
from src.jdtaxcalculator import UkTaxCalculator


class TestInit(TestCase):

    def test_negative_income(self):
        income = -100
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        with pytest.raises(ValueError):
            take_home = UkTaxCalculator(
                income, deductions, student_loan_plan, tax_year)

    def test_zero_income(self):
        income = 0
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, student_loan_plan, tax_year)

    def test_valid_income(self):
        income = 10000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        UkTaxCalculator(income, deductions, student_loan_plan, tax_year)

    def test_deductions_negative_value(self):
        income = 20000
        deductions = -500
        student_loan_plan = 0
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, student_loan_plan, tax_year)

    def test_deductions_greater_income_value(self):
        income = 20000
        deductions = 30000
        student_loan_plan = 0
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, student_loan_plan, tax_year)

    def test_student_loan_negative(self):
        income = 20000
        deductions = 0
        student_loan_plan = -1
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, student_loan_plan, tax_year)

    def test_student_loan_too_high(self):
        income = 20000
        deductions = 0
        student_loan_plan = 15
        tax_year = "24/25"
        with pytest.raises(ValueError):
            UkTaxCalculator(income, deductions, student_loan_plan, tax_year)


class TestSetTaxFreeAllowance(TestCase):

    def test_below_threshold(self):
        income = 10000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        assert take_home.tax_free_allowance == 12570

    def test_at_threshold(self):
        income = 100000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        assert take_home.tax_free_allowance == 12570

    def test_in_threshold(self):
        income = 110000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        assert take_home.tax_free_allowance == 7570

    def test_above_threshold(self):
        income = 130000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        assert take_home.tax_free_allowance == 0


class TestSetIncomeTax(TestCase):

    def test_under_tax_allowance(self):
        income = 10000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [0, 0, 0]

    def test_at_tax_allowance(self):
        income = 12570
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [0, 0, 0]

    def test_in_low_band(self):
        income = 20000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [1486, 0, 0]

    def test_at_mid_band(self):
        income = 50270
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [7540, 0, 0]

    def test_in_mid_band(self):
        income = 70000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [7540, 7892, 0]

    def test_at_income_limit(self):
        income = 100000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [7540, 19892, 0]

    def test_in_income_limit(self):
        income = 115000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [7540, 28892, 0]

    def test_at_high_band(self):
        income = 125140
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [7540, 34976, 0]

    def test_in_high_band(self):
        income = 200000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [7540, 34976, 33687]

    def test_in_high_band_with_small_deduction(self):
        income = 200000
        deductions = 20000
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [7540, 34976, 24687]

    def test_in_high_band_with_medium_deduction(self):
        income = 200000
        deductions = 40000
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [7540, 34976, 15687]

    def test_in_high_band_with_large_deduction(self):
        income = 200000
        deductions = 100000
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()

        assert take_home.income_tax == [7540, 19892, 0]


class TestSetNationalInsurance(TestCase):

    def test_no_national_insurance(self):
        income = 10000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_national_insurance()

        assert take_home.national_insurance == 0

    def test_in_high_band(self):
        income = 50000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_national_insurance()

        assert take_home.national_insurance == 3743.00

    def test_in_high_band_with_deductions(self):
        income = 50000
        deductions = 10000
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_national_insurance()

        assert take_home.national_insurance == 2743.00

    def test_massive(self):
        income = 150000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_national_insurance()

        assert take_home.national_insurance == 5764.60


class TestSetStudentLoan(TestCase):

    def test_no_student_loan(self):
        income = 20000
        deductions = 0
        student_loan_plan = 0
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_student_loan()

        assert take_home.student_loan == 0

    def test_no_payback_plan1(self):
        income = 20000
        deductions = 0
        student_loan_plan = 1
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_student_loan()

        assert take_home.student_loan == 0

    def test_student_loan_plan1(self):
        income = 33000
        deductions = 0
        student_loan_plan = 1
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_student_loan()

        assert take_home.student_loan == 988.65

    # TO DO: add unit tests for all plans paying an amount and not paying


class TestSetUkTaxCalculator(TestCase):

    def test_full(self):
        income = 200000
        deductions = 40000
        student_loan_plan = 2
        tax_year = "24/25"
        take_home = UkTaxCalculator(
            income, deductions, student_loan_plan, tax_year)
        take_home.set_tax_free_allowance()
        take_home.set_income_tax()
        take_home.set_national_insurance()
        take_home.set_student_loan()
        take_home.set_take_home()

        assert take_home.take_home == 83888.95

from unittest import TestCase
from src.jdtaxcalculator import UkTaxCalculator


# Private methods accessed with obj = MyClass() -> obj._MyClass__private_method()
class TestPersonalAllowance(TestCase):

    def test_below_threshold(self):
        deducted_total_award = 10000
        personal_allowance_income_limit = 100000
        max_personal_allowance = 12570
        expected = 12570

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__personal_allowance(deducted_total_award, personal_allowance_income_limit,
                                                           max_personal_allowance)

        self.assertEqual(expected, actual)

    def test_at_threshold(self):
        deducted_total_award = 100000
        personal_allowance_income_limit = 100000
        max_personal_allowance = 12570
        expected = 12570

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__personal_allowance(deducted_total_award, personal_allowance_income_limit,
                                                           max_personal_allowance)

        self.assertEqual(expected, actual)

    def test_in_threshold(self):
        deducted_total_award = 110000
        personal_allowance_income_limit = 100000
        max_personal_allowance = 12570
        expected = 7570

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__personal_allowance(deducted_total_award, personal_allowance_income_limit,
                                                           max_personal_allowance)

        self.assertEqual(expected, actual)

    def test_above_threshold(self):
        deducted_total_award = 130000
        personal_allowance_income_limit = 100000
        max_personal_allowance = 12570
        expected = 0

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__personal_allowance(deducted_total_award, personal_allowance_income_limit,
                                                           max_personal_allowance)

        self.assertEqual(expected, actual)


class TestGetBandedTaxDeductions(TestCase):

    def test_under_min_band(self):
        bands = [12570, 50270, 125140]
        amounts = [0.2, 0.4, 0.45]
        deducted_total_award = 10000
        expected = [0, 0, 0]

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__get_banded_deductions(bands, amounts, deducted_total_award)

        self.assertEqual(expected, actual)

    def test_at_low_band(self):
        bands = [12570, 50270, 125140]
        amounts = [0.2, 0.4, 0.45]
        deducted_total_award = 12570
        expected = [0, 0, 0]

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__get_banded_deductions(bands, amounts, deducted_total_award)

        self.assertEqual(expected, actual)

    def test_in_low_band(self):
        bands = [12570, 50270, 125140]
        amounts = [0.2, 0.4, 0.45]
        deducted_total_award = 20000
        expected = [1486, 0, 0]

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__get_banded_deductions(bands, amounts, deducted_total_award)

        self.assertEqual(expected, actual)

    def test_at_mid_band(self):
        bands = [12570, 50270, 125140]
        amounts = [0.2, 0.4, 0.45]
        deducted_total_award = 50270
        expected = [7540, 0, 0]

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__get_banded_deductions(bands, amounts, deducted_total_award)

        self.assertEqual(expected, actual)

    def test_in_mid_band(self):
        bands = [12570, 50270, 125140]
        amounts = [0.2, 0.4, 0.45]
        deducted_total_award = 70000
        expected = [7540, 7892, 0]

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__get_banded_deductions(bands, amounts, deducted_total_award)

        self.assertEqual(expected, actual)

    def test_at_high_band(self):
        bands = [0, 37700, 125140]
        amounts = [0.2, 0.4, 0.45]
        deducted_total_award = 125140
        expected = [7540, 34976, 0]

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__get_banded_deductions(bands, amounts, deducted_total_award)

        self.assertEqual(expected, actual)

    def test_in_high_band(self):
        bands = [0, 37700, 125140]
        amounts = [0.2, 0.4, 0.45]
        deducted_total_award = 200000
        expected = [7540, 34976, 33687]

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__get_banded_deductions(bands, amounts, deducted_total_award)

        self.assertEqual(expected, actual)


class TestSetStudentLoan(TestCase):

    def test_no_student_loan(self):
        deducted_total_award = 20000
        student_loan_threshold = 25000
        student_loan_rate = 0.09
        expected = 0

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__student_loan(deducted_total_award, student_loan_threshold, student_loan_rate)

        self.assertEqual(expected, actual)

    def test_some_student_loan(self):
        deducted_total_award = 45000
        student_loan_threshold = 24990
        student_loan_rate = 0.09
        expected = 1800

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__student_loan(deducted_total_award, student_loan_threshold, student_loan_rate)

        self.assertEqual(expected, actual)


class TestTakeHome(TestCase):
    def test_take_home(self):
        deducted_income = 40000
        national_insurance = 5000
        income_tax = 10000
        student_loan = 2000
        expected = 23000

        uktc = UkTaxCalculator()
        actual = uktc._UkTaxCalculator__take_home(deducted_income, national_insurance, income_tax, student_loan)

        self.assertEqual(expected, actual)


class TestCalculate(TestCase):

    def test_under_low_band_no_deduction_no_benefits_no_student_loan(self):
        income = 10000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = '24/25'
        expected = {
            'personal_allowance': 12570,
            'banded_income_tax': [0, 0, 0],
            'banded_national_insurance': [0, 0],
            'student_loan': 0,
            'take_home': 10000
        }

        uktc = UkTaxCalculator()
        actual = uktc.calculate(income, deductions, taxable_benefits, student_loan_plan, tax_year)

        self.assertEqual(expected, actual)

    def test_in_low_band_no_deduction_no_benefits_no_student_loan(self):
        income = 20000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = '24/25'
        expected = {
            'personal_allowance': 12570,
            'banded_income_tax': [1486, 0, 0],
            'banded_national_insurance': [594.4, 0],
            'student_loan': 0,
            'take_home': 17919.6
        }

        uktc = UkTaxCalculator()
        actual = uktc.calculate(income, deductions, taxable_benefits, student_loan_plan, tax_year)

        self.assertEqual(expected, actual)

    def test_in_mid_band_no_deduction_no_benefits_no_student_loan(self):
        income = 60000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = '24/25'
        expected = {
            'personal_allowance': 12570,
            'banded_income_tax': [7540, 3892, 0],
            'banded_national_insurance': [3016.0, 194.6],
            'student_loan': 0,
            'take_home': 45357.4
        }

        uktc = UkTaxCalculator()
        actual = uktc.calculate(income, deductions, taxable_benefits, student_loan_plan, tax_year)

        self.assertEqual(expected, actual)

    def test_personal_allowance_reduction_no_deduction_no_benefits_no_student_loan(self):
        income = 110000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = '24/25'
        expected = {
            'personal_allowance': 7570,
            'banded_income_tax': [7540, 25892, 0],
            'banded_national_insurance': [3016.0, 1194.6],
            'student_loan': 0,
            'take_home': 72357.4
        }

        uktc = UkTaxCalculator()
        actual = uktc.calculate(income, deductions, taxable_benefits, student_loan_plan, tax_year)

        self.assertEqual(expected, actual)

    def test_max_tax_no_deduction_no_benefits_no_student_loan(self):
        income = 200000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = '24/25'
        expected = {
            'personal_allowance': 0,
            'banded_income_tax': [7540, 34976, 33687],
            'banded_national_insurance': [3016.0, 2994.6],
            'student_loan': 0,
            'take_home': 117786.4
        }

        uktc = UkTaxCalculator()
        actual = uktc.calculate(income, deductions, taxable_benefits, student_loan_plan, tax_year)

        self.assertEqual(expected, actual)

    def test_mid_band_deduction_to_low_no_benefits_no_student_loan(self):
        income = 60000
        deductions = 40000
        taxable_benefits = 0
        student_loan_plan = 0
        tax_year = '24/25'
        expected = {
            'personal_allowance': 12570,
            'banded_income_tax': [1486, 0, 0],
            'banded_national_insurance': [594.4, 0],
            'student_loan': 0,
            'take_home': 17919.6
        }

        uktc = UkTaxCalculator()
        actual = uktc.calculate(income, deductions, taxable_benefits, student_loan_plan, tax_year)

        self.assertEqual(expected, actual)

    def test_low_band_no_deduction_benefits_to_mid_no_student_loan(self):
        income = 40000
        deductions = 0
        taxable_benefits = 20000
        student_loan_plan = 0
        tax_year = '24/25'
        expected = {
            'personal_allowance': 12570,
            'banded_income_tax': [7540, 3892, 0],
            'banded_national_insurance': [2194.4, 0],
            'student_loan': 0,
            'take_home': 26373.6
        }

        uktc = UkTaxCalculator()
        actual = uktc.calculate(income, deductions, taxable_benefits, student_loan_plan, tax_year)

        self.assertEqual(expected, actual)

    def test_low_band_no_deduction_no_benefits_student_loan_plan_2(self):
        income = 40000
        deductions = 0
        taxable_benefits = 0
        student_loan_plan = 2
        tax_year = '24/25'
        expected = {
            'personal_allowance': 12570,
            'banded_income_tax': [5486, 0, 0],
            'banded_national_insurance': [2194.4, 0],
            'student_loan': 1140,
            'take_home': 31179.6
        }

        uktc = UkTaxCalculator()
        actual = uktc.calculate(income, deductions, taxable_benefits, student_loan_plan, tax_year)

        self.assertEqual(expected, actual)

    def test_mid_band_deduction_to_low_benefit_to_mid_loan_plan_1(self):
        income = 70000
        deductions = 25000
        taxable_benefits = 10000
        student_loan_plan = 1
        tax_year = '24/25'
        expected = {
            'personal_allowance': 12570,
            'banded_income_tax': [7540, 1892, 0],
            'banded_national_insurance': [2594.4, 0],
            'student_loan': 1800,
            'take_home': 31173.60
        }

        uktc = UkTaxCalculator()
        actual = uktc.calculate(income, deductions, taxable_benefits, student_loan_plan, tax_year)

        self.assertEqual(expected, actual)

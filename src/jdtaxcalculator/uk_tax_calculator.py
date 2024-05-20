import yaml
from os import path


class UkTaxCalculator(object):
    # Calculate the deductions and take home pay of a person working in the UK based on their income and conditions

    def get_config(self, student_loan_plan: int, tax_year: str):
        # Retrieves config for and validates tax year, subsequently validates student loan plan under tax year config
        conf_path = path.join(path.dirname(__file__),
                              'conf', 'uk_tax_rules.yml')
        with open(conf_path, 'r') as config_file:
            full_config = yaml.load(config_file, Loader=yaml.FullLoader)
        if tax_year not in full_config['tax_year']:
            raise ValueError('Invalid tax year')
        conf = full_config['tax_year'][tax_year]

        self.standard_tax_free_allowance = conf['income_tax']['tax_free_allowance']
        self.tax_free_allowance_backoff_start = conf['income_tax']['allowance_backoff_start']
        self.tax_bands = conf['income_tax']['bands']
        self.tax_amounts = conf['income_tax']['amounts']
        self.ni_bands = conf['national_insurance']['bands']
        self.ni_amounts = conf['national_insurance']['amounts']
        student_loan_plans = conf['student_loan_plans']
        if student_loan_plan == 0:
            return
        elif student_loan_plan in student_loan_plans:
            self.student_loan_threshold = student_loan_plans[student_loan_plan]['threshold']
            self.student_loan_rate = student_loan_plans[student_loan_plan]['rate']
        else:
            raise ValueError('Invalid student loan plan')

    def __init__(self, income: float, deductions: float, student_loan_plan: int, tax_year: str):
        """Use student_loan_plan=0 if not on a student loan plan and tax_year as year_start/year_end e.g. 24/25"""
        self.tax_free_allowance = None
        self.student_loan_rate = None
        self.student_loan_threshold = None
        self.ni_amounts = None
        self.ni_bands = None
        self.tax_amounts = None
        self.tax_bands = None
        self.tax_free_allowance_backoff_start = None
        self.standard_tax_free_allowance = None
        self.deductions = 0
        self.deducted_income = 0
        self.income_tax = [0, 0, 0]
        self.national_insurance = 0
        self.student_loan = 0
        self.take_home = 0
        if not income > 0:
            raise ValueError('Income must be greater than zero')
        self.income = income
        if not deductions >= 0:
            raise ValueError('Deductions must not be negative')
        if not income > deductions:
            raise ValueError('Deductions must be lesser than income')
        self.deductions = deductions
        self.get_config(student_loan_plan, tax_year)
        self.student_loan_plan = student_loan_plan
        self.deducted_income = income - deductions
        self.set_tax_free_allowance()
        self.set_income_tax()
        self.set_national_insurance()
        self.set_student_loan()
        self.set_take_home()

    def set_tax_free_allowance(self):
        if self.deducted_income <= self.tax_free_allowance_backoff_start:
            self.tax_free_allowance = self.standard_tax_free_allowance
            return
        tax_free_reduction = (self.deducted_income -
                              self.tax_free_allowance_backoff_start) / 2
        if tax_free_reduction < self.standard_tax_free_allowance:
            self.tax_free_allowance = self.standard_tax_free_allowance - tax_free_reduction
        else:
            self.tax_free_allowance = 0

    def set_income_tax(self):
        # Add the tax-free allowance to the tax bands
        tax_bands = [band + self.tax_free_allowance for band in self.tax_bands]

        tax_band_found = False
        for i in reversed(range(len(tax_bands))):
            if tax_band_found:
                # Just take the maximum
                self.income_tax[i] = (
                                             tax_bands[i + 1] - tax_bands[i]) * self.tax_amounts[i]
                continue
            if tax_bands[i] >= self.deducted_income:
                self.income_tax[i] = 0
                continue
            tax_band_found = True
            self.income_tax[i] = (self.deducted_income -
                                  tax_bands[i]) * self.tax_amounts[i]

    def set_national_insurance(self):
        national_insurance = 0
        for i in reversed(range(len(self.ni_bands))):
            if i + 1 >= len(self.ni_bands):
                # Final ni bracket to be handled differently to prevent index out of range
                if self.ni_bands[i] < self.deducted_income:
                    national_insurance += self.ni_amounts[i] * (
                            self.deducted_income - self.ni_bands[i])
            else:
                if self.ni_bands[i] < self.deducted_income:
                    if self.ni_bands[i + 1] > self.deducted_income:
                        national_insurance += self.ni_amounts[i] * (
                                self.deducted_income - self.ni_bands[i])
                    elif self.ni_bands[i + 1] <= self.deducted_income:
                        national_insurance += self.ni_amounts[i] * (
                                self.ni_bands[i + 1] - self.ni_bands[i])
        self.national_insurance = round(national_insurance, 2)

    def set_student_loan(self):
        if self.student_loan_plan == 0:
            return

        over_threshold = self.deducted_income - self.student_loan_threshold
        if over_threshold > 0:
            self.student_loan = round(
                over_threshold * self.student_loan_rate, 2)

    def set_take_home(self):
        self.take_home = self.deducted_income - self.national_insurance - sum(self.income_tax) - self.student_loan

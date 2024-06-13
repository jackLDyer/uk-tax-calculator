import yaml
from os import path


class UkTaxCalculator(object):
    # Calculate the deductions and take home pay of a person working in the UK based on their income and conditions

    def __get_config(self, student_loan_plan: int, tax_year: str):
        # Retrieves config for and validates tax year, subsequently validates student loan plan under tax year config
        conf_path = path.join(path.dirname(__file__), 'conf', 'uk_tax_rules.yml')
        with open(conf_path, 'r') as config_file:
            full_config = yaml.load(config_file, Loader=yaml.FullLoader)
        if tax_year not in full_config['tax_year']:
            raise ValueError('Invalid tax year')
        conf = full_config['tax_year'][tax_year]

        self.__max_personal_allowance = conf['income_tax']['tax_free_allowance']
        self.__personal_allowance_income_limit = conf['income_tax']['allowance_backoff_start']
        self.__tax_bands = conf['income_tax']['bands']
        self.__tax_amounts = conf['income_tax']['amounts']
        self.__ni_bands = conf['national_insurance']['bands']
        self.__ni_amounts = conf['national_insurance']['amounts']
        student_loan_plans = conf['student_loan_plans']
        if student_loan_plan == 0:
            self.__student_loan_threshold = None
            self.__student_loan_rate = None
        elif student_loan_plan in student_loan_plans:
            self.__student_loan_threshold = student_loan_plans[student_loan_plan]['threshold']
            self.__student_loan_rate = student_loan_plans[student_loan_plan]['rate']
        else:
            raise ValueError('Invalid student loan plan')

    def __init__(self, income: float, deductions: float, taxable_benefits: float, student_loan_plan: int,
                 tax_year: str):
        """Use student_loan_plan=0 if not on a student loan plan and tax_year as year_start/year_end e.g. 24/25"""

        # Validate income
        if not income > 0:
            raise ValueError('Income must be greater than zero')

        # Validate deductions
        if not deductions >= 0:
            raise ValueError('Deductions must not be negative')
        if not income > deductions:
            raise ValueError('Deductions must be lesser than income')
        self.__deducted_income = income - deductions

        # Validate taxable benefits
        if not taxable_benefits >= 0:
            raise ValueError('Taxable benefits must not be negative')
        self.__deducted_total_award = self.__deducted_income + taxable_benefits

        # Validate student loan plan from config
        self.__get_config(student_loan_plan, tax_year)
        self.student_loan_plan = student_loan_plan

        # Run methods
        self.__set_personal_allowance()
        self.__set_income_tax()
        self.__set_national_insurance()
        self.__set_student_loan()
        self.__set_take_home()

    def __set_personal_allowance(self):
        if self.__deducted_total_award <= self.__personal_allowance_income_limit:
            self.personal_allowance = self.__max_personal_allowance
            return
        tax_free_reduction = (self.__deducted_total_award - self.__personal_allowance_income_limit) / 2
        if tax_free_reduction < self.__max_personal_allowance:
            self.personal_allowance = self.__max_personal_allowance - tax_free_reduction
        else:
            self.personal_allowance = 0

    def __set_income_tax(self):
        self.income_tax = [0, 0, 0]
        # Add the tax-free allowance to the tax bands
        tax_bands = [band + self.personal_allowance for band in self.__tax_bands]

        tax_band_found = False
        for i in reversed(range(len(tax_bands))):
            if tax_band_found:
                # Just take the maximum
                self.income_tax[i] = (tax_bands[i + 1] - tax_bands[i]) * self.__tax_amounts[i]
                continue
            if tax_bands[i] >= self.__deducted_total_award:
                self.income_tax[i] = 0
                continue
            tax_band_found = True
            self.income_tax[i] = (self.__deducted_total_award - tax_bands[i]) * self.__tax_amounts[i]

    def __set_national_insurance(self):
        national_insurance = 0
        for i in reversed(range(len(self.__ni_bands))):
            if i + 1 >= len(self.__ni_bands):
                # Final ni bracket to be handled differently to prevent index out of range
                if self.__ni_bands[i] < self.__deducted_total_award:
                    national_insurance += self.__ni_amounts[i] * (self.__deducted_total_award - self.__ni_bands[i])
            else:
                if self.__ni_bands[i] < self.__deducted_total_award:
                    if self.__ni_bands[i + 1] > self.__deducted_total_award:
                        national_insurance += self.__ni_amounts[i] * (self.__deducted_total_award - self.__ni_bands[i])
                    elif self.__ni_bands[i + 1] <= self.__deducted_total_award:
                        national_insurance += self.__ni_amounts[i] * (self.__ni_bands[i + 1] - self.__ni_bands[i])
        self.national_insurance = round(national_insurance, 2)

    def __set_student_loan(self):
        if self.student_loan_plan == 0:
            self.student_loan = 0
            return

        over_threshold = self.__deducted_total_award - self.__student_loan_threshold
        if over_threshold > 0:
            self.student_loan = round(over_threshold * self.__student_loan_rate, 2)
        else:
            self.student_loan = 0

    def __set_take_home(self):
        self.take_home = self.__deducted_income - self.national_insurance - sum(self.income_tax) - self.student_loan

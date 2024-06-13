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
        self.__student_loan_plan = student_loan_plan

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

    @staticmethod
    def __get_banded_tax_deductions(bands: list, amounts: list, deducted_total_award) -> list:
        tax_deductions = [0] * len(bands)

        # Iterate backwards over the tax bands, once band is found take the maximum value for the band
        in_previous_band = False
        for i in reversed(range(len(bands))):
            if in_previous_band:
                tax_deductions[i] = (bands[i + 1] - bands[i]) * amounts[i]
            elif bands[i] >= deducted_total_award:
                tax_deductions[i] = 0
            else:
                in_previous_band = True
                tax_deductions[i] = (deducted_total_award - bands[i]) * amounts[i]

        return tax_deductions

    def __set_income_tax(self):
        personal_allowance_tax_bands = [band + self.personal_allowance for band in self.__tax_bands]
        self.income_tax = self.__get_banded_tax_deductions(personal_allowance_tax_bands, self.__tax_amounts,
                                                           self.__deducted_total_award)

    def __set_national_insurance(self):
        national_insurance_banded = self.__get_banded_tax_deductions(self.__ni_bands, self.__ni_amounts,
                                                                     self.__deducted_total_award)
        self.national_insurance = round(sum(national_insurance_banded), 2)

    def __set_student_loan(self):
        if self.__student_loan_plan == 0:
            self.student_loan = 0
            return

        over_threshold = self.__deducted_total_award - self.__student_loan_threshold
        if over_threshold > 0:
            self.student_loan = round(over_threshold * self.__student_loan_rate, 2)
        else:
            self.student_loan = 0

    def __set_take_home(self):
        self.take_home = self.__deducted_income - self.national_insurance - sum(self.income_tax) - self.student_loan

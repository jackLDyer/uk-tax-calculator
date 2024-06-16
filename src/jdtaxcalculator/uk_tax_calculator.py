import yaml
from os import path


class UkTaxCalculator(object):
    # Calculate the deductions and take home pay of a person working in the UK based on their income and conditions

    def calculate(self, income: float, deductions: float, taxable_benefits: float, student_loan_plan: int,
                  tax_year: str):
        """Use student_loan_plan=0 if not on a student loan plan and tax_year as year_start/year_end e.g. 24/25"""

        if not income > 0:
            raise ValueError('Income must be greater than zero')

        if not deductions >= 0:
            raise ValueError('Deductions must not be negative')
        if not income > deductions:
            raise ValueError('Deductions must be lesser than income')
        deducted_income = income - deductions

        if not taxable_benefits >= 0:
            raise ValueError('Taxable benefits must not be negative')
        deducted_total_award = deducted_income + taxable_benefits

        if student_loan_plan == 0:
            student_loan_threshold = 0
            student_loan_rate = 0
        elif student_loan_plan not in self.config['student_loan_plan']:
            raise ValueError('Invalid student loan plan')
        else:
            student_loan_threshold = self.config['student_loan_plan'][student_loan_plan]['threshold']
            student_loan_rate = self.config['student_loan_plan'][student_loan_plan]['rate']

        if tax_year not in self.config['tax_year']:
            raise ValueError('Invalid or unsupported tax year - "dd/dd" format expected')
        else:
            tax_rules = self.config['tax_year'][tax_year]
            personal_allowance_income_limit = tax_rules['personal_allowance']['income_limit']
            max_personal_allowance = tax_rules['personal_allowance']['max']
            tax_bands = tax_rules['income_tax']['bands']
            tax_amounts = tax_rules['income_tax']['amounts']
            ni_bands = tax_rules['national_insurance']['bands']
            ni_amounts = tax_rules['national_insurance']['amounts']

        personal_allowance = self.__personal_allowance(deducted_total_award, personal_allowance_income_limit,
                                                       max_personal_allowance)
        tax_bands = [band + personal_allowance for band in tax_bands]
        banded_income_tax = self.__get_banded_deductions(tax_bands, tax_amounts, deducted_total_award)
        banded_national_insurance = self.__get_banded_deductions(ni_bands, ni_amounts, deducted_total_award)
        student_loan = self.__student_loan(deducted_total_award, student_loan_threshold, student_loan_rate)
        take_home = self.__take_home(deducted_income, sum(banded_national_insurance), sum(banded_income_tax),
                                     student_loan)

        return {
            'personal_allowance': personal_allowance,
            'banded_income_tax': banded_income_tax,
            'banded_national_insurance': banded_national_insurance,
            'student_loan': student_loan,
            'take_home': take_home
        }

    def __init__(self):
        conf_path = path.join(path.dirname(__file__), 'conf', 'uk_tax_rules.yml')
        with open(conf_path, 'r') as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)

    @staticmethod
    def __personal_allowance(deducted_total_award: float, personal_allowance_income_limit: float,
                             max_personal_allowance: float) -> float:
        if deducted_total_award <= personal_allowance_income_limit:
            return max_personal_allowance
        tax_free_reduction = (deducted_total_award - personal_allowance_income_limit) / 2
        if tax_free_reduction < max_personal_allowance:
            return max_personal_allowance - tax_free_reduction
        else:
            return 0

    @staticmethod
    def __get_banded_deductions(bands: list, amounts: list, deducted_total_award) -> list:
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

    @staticmethod
    def __student_loan(deducted_total_award: float, student_loan_threshold: float, student_loan_rate: float) -> float:
        if deducted_total_award - student_loan_threshold > 0:
            return round((deducted_total_award - student_loan_threshold) * student_loan_rate, 2)
        else:
            return 0

    @staticmethod
    def __take_home(deducted_income: float, national_insurance: float, income_tax: float, student_loan: float) -> float:
        return deducted_income - national_insurance - income_tax - student_loan

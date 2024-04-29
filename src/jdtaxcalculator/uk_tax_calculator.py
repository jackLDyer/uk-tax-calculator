class UkTaxCalculator():
    # This class is intended to calculate the deductions and take home pay of a person working in the UK based on their income and conditions

    tax_free_allowance_income_limit = 100000
    tax_bands = [0, 37700, 125140]
    tax_amounts = [0.2, 0.4, 0.45]
    ni_bands = [12570, 50270]
    ni_amounts = [0.10, 0.02]
    valid_student_loan_plans = [0, 1, 2, 4, 5]
    plan1_threshold = 22015
    plan2_threshold = 27295
    plan4_threshold = 27660
    plan5_threshold = 25000
    student_loan_rate = 0.09

    tax_free_allowance = 12570
    income = 0
    deductions = 0
    deducted_income = 0
    income_tax = [0, 0, 0]
    national_insurance = 0
    student_loan_plan = 0
    student_loan = 0
    take_home = 0

    def reset(self):
        self.tax_free_allowance = 12570
        self.income = 0
        self.deductions = 0
        self.income_tax = [0, 0, 0]
        self.national_insurance = 0

    def __init__(self, income: float, deductions: float, student_loan_plan: int):
        self.reset()
        assert income > 0
        self.income = income
        assert deductions >= 0
        assert income > deductions
        self.deductions = deductions
        assert student_loan_plan in self.valid_student_loan_plans
        self.student_loan_plan = student_loan_plan

        self.deducted_income = income - deductions
        self.set_tax_free_allowance
        self.set_income_tax
        self.set_national_insurance
        self.set_student_loan
        self.set_take_home

    def set_tax_free_allowance(self):
        # Calculate tax free allowance and hence tax bands
        if self.deducted_income <= self.tax_free_allowance_income_limit:
            return
        tax_free_reduction = (self.deducted_income -
                              self.tax_free_allowance_income_limit) / 2
        if tax_free_reduction < self.tax_free_allowance:
            self.tax_free_allowance -= tax_free_reduction
        else:
            self.tax_free_allowance = 0

    def set_income_tax(self):
        # Add the tax free allowance to the tax bands
        tax_bands = [band + self.tax_free_allowance for band in self.tax_bands]
        
        tax_band_found = False
        for i in reversed(range(len(tax_bands))):
            if tax_band_found:
                # Just take the maximum
                self.income_tax[i] = (tax_bands[i + 1] - tax_bands[i]) * self.tax_amounts[i]
                continue
            if tax_bands[i] >= self.deducted_income:
                self.income_tax[i] = 0
                continue
            tax_band_found = True
            self.income_tax[i] = (self.deducted_income - tax_bands[i])* self.tax_amounts[i]

    def set_national_insurance(self):
        for i in reversed(range(len(self.ni_bands))):
            if i + 1 >= len(self.ni_bands):
                # Final ni bracket to be handled differently to prevent index out of range
                if self.ni_bands[i] < self.deducted_income:
                    self.national_insurance += self.ni_amounts[i] * (
                        self.deducted_income - self.ni_bands[i])
            else:
                if self.ni_bands[i] < self.deducted_income:
                    if self.ni_bands[i + 1] > self.deducted_income:
                        self.national_insurance += self.ni_amounts[i] * (
                            self.deducted_income - self.ni_bands[i])
                    elif self.ni_bands[i + 1] <= self.deducted_income:
                        self.national_insurance += self.ni_amounts[i] * (
                            self.ni_bands[i + 1] - self.ni_bands[i])
        self.national_insurance = round(self.national_insurance, 2)

    def set_student_loan(self):
        match self.student_loan_plan:
            case 0:
                return
            case 1:
                threshold = self.plan1_threshold
            case 2:
                threshold = self.plan2_threshold
            case 4:
                threshold = self.plan4_threshold
            case 5:
                threshold = self.plan5_threshold
            case _:
                raise Exception('Invalid student loan plan')
        over_threshold = self.deducted_income - threshold
        if over_threshold > 0:
            self.student_loan = round(
                over_threshold * self.student_loan_rate, 2)

    def set_take_home(self):
        self.take_home = self.deducted_income - self.national_insurance - \
            sum(self.income_tax) - self.student_loan

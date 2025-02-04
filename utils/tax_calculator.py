from data.months import months
from data.tax_rates import tax_brackets

def calculate_net_salary(gross_salary):

    annual_income = 0
    net_salaries = []

    for _ in range(12):
        remaining_income = gross_salary
        tax = 0

        for limit, rate in tax_brackets:
            if annual_income < limit:
                taxable_amount = min(remaining_income, limit - annual_income)
                tax += taxable_amount * rate
                remaining_income -= taxable_amount

            if remaining_income <= 0:
                break

        net_salary = gross_salary - tax
        net_salaries.append(net_salary)
        annual_income += gross_salary

    return net_salaries, months



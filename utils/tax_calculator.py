import os
import openpyxl
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

    root_dir = os.getcwd()

    output_folder = os.path.join(root_dir, "files")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_path = os.path.join(output_folder, "net_salaries.xlsx")

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Зарплата"

    sheet['A1'] = 'Месяц'
    sheet['B1'] = 'Зарплата на руки'

    for i, net_salary in enumerate(net_salaries):
        sheet[f'A{i + 2}'] = months[i]  # Название месяца
        sheet[f'B{i + 2}'] = f'{net_salary:.2f} руб.'  # Зарплата с точностью до двух знаков

    wb.save(file_path)

    print(f"\nФайл net_salaries.xlsx сохранён в папке {os.path.abspath(output_folder)}\n")

    return net_salaries, months

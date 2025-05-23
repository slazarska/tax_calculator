import os
import openpyxl
from data.months import months
from data.tax_rates import tax_brackets

def calculate_net_salary(gross_salary, start_month_index):
    annual_income = 0  # Доход с начала расчёта — с выбранного месяца
    net_salaries = []

    print("\nРасчёт 'на руки' по месяцам:\n")

    for i in range(start_month_index, 12):
        remaining_income = gross_salary
        tax = 0

        for limit, rate in tax_brackets:
            if annual_income < limit:
                taxable_amount = min(remaining_income, limit - annual_income)
                tax += taxable_amount * rate
                remaining_income -= taxable_amount
                annual_income += taxable_amount

            if remaining_income <= 0:
                break

        net_salary = gross_salary - tax
        net_salaries.append(net_salary)

        month_name = months[i]
        print(f"{month_name}: {net_salary:.2f} руб.")

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
        sheet[f'A{i + 2}'] = months[start_month_index + i]
        sheet[f'B{i + 2}'] = f'{net_salary:.2f} руб.'

    wb.save(file_path)

    print(f"\nФайл net_salaries.xlsx сохранён в папке {os.path.abspath(output_folder)}\n")

    return net_salaries, months[start_month_index:]

def calculate_taxed_salary(gross_salary, start_month_index):
    annual_income = 0
    net_salaries = []

    for i in range(start_month_index, 12):
        remaining_income = gross_salary
        tax = 0

        for limit, rate in tax_brackets:
            if annual_income < limit:
                taxable_amount = min(remaining_income, limit - annual_income)
                tax += taxable_amount * rate
                remaining_income -= taxable_amount
                annual_income += taxable_amount

            if remaining_income <= 0:
                break

        net_salary = gross_salary - tax
        net_salaries.append((months[i], net_salary))

    return net_salaries


def print_and_save_results(net_salaries, filename_suffix=""):
    print("\nРасчёт 'на руки' по месяцам:\n")

    for month, salary in net_salaries:
        print(f"{month}: {salary:.2f} руб.")

    root_dir = os.getcwd()
    output_folder = os.path.join(root_dir, "files")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_path = os.path.join(output_folder, f"net_salaries{filename_suffix}.xlsx")

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Зарплата"

    sheet['A1'] = 'Месяц'
    sheet['B1'] = 'Зарплата на руки'

    for i, (month, salary) in enumerate(net_salaries):
        sheet[f'A{i + 2}'] = month
        sheet[f'B{i + 2}'] = f'{salary:.2f} руб.'

    wb.save(file_path)
    print(f"\nФайл net_salaries{filename_suffix}.xlsx сохранён в папке {os.path.abspath(output_folder)}\n")


def find_gross_salary_for_target_net(target_net, start_month_index):
    low = target_net
    high = target_net * 2

    for _ in range(100):
        mid = (low + high) / 2
        net_salaries = calculate_taxed_salary(mid, start_month_index)
        avg_net = sum(s for _, s in net_salaries) / len(net_salaries)

        if abs(avg_net - target_net) < 0.5:
            return mid, net_salaries
        elif avg_net < target_net:
            low = mid
        else:
            high = mid

    return mid, net_salaries

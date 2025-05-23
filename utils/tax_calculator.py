import os
import openpyxl
from typing import List, Tuple
from data.months import months
from data.tax_rates import tax_brackets

YEAR_MONTHS = 12
DEFAULT_OUTPUT_FOLDER = "files"
DEFAULT_FILENAME = "net_salaries.xlsx"

def calculate_tax(gross_salary: float, annual_income: float) -> Tuple[float, float]:
    """Вычисляет налог на зарплату с учётом накопленного дохода."""
    remaining_income = gross_salary
    tax = 0
    effective_annual_income = annual_income

    for limit, rate in tax_brackets:
        if effective_annual_income < limit:
            taxable_amount = min(remaining_income, limit - effective_annual_income)
            tax += taxable_amount * rate
            remaining_income -= taxable_amount
            effective_annual_income += taxable_amount

            if remaining_income <= 0:
                break

    new_annual_income = annual_income + gross_salary - remaining_income
    return tax, new_annual_income


def calculate_net_salaries(gross_salary: float, start_month_index: int, initial_income: float = 0.0) -> List[Tuple[str, float]]:
    """Рассчитывает чистую зарплату с учётом пропущенных месяцев и уже полученного дохода."""
    annual_income = initial_income
    results = []

    for month_idx in range(start_month_index, 12):
        tax, annual_income = calculate_tax(gross_salary, annual_income)
        net_salary = gross_salary - tax
        results.append((months[month_idx], net_salary))

    return results


def save_to_excel(data: List[Tuple[str, float]], filename: str = None) -> str:
    """
    Сохраняет данные в Excel файл."""
    if filename is None:
        filename = DEFAULT_FILENAME

    output_folder = os.path.join(os.getcwd(), DEFAULT_OUTPUT_FOLDER)
    os.makedirs(output_folder, exist_ok=True)

    file_path = os.path.join(output_folder, filename)

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Зарплата"

    sheet['A1'] = 'Месяц'
    sheet['B1'] = 'Зарплата на руки'

    for i, (month, salary) in enumerate(data, start=2):
        sheet[f'A{i}'] = month
        sheet[f'B{i}'] = f'{salary:.2f} руб.'

    wb.save(file_path)
    return file_path


def print_results(net_salaries: List[Tuple[str, float]]) -> None:
    """Выводит на экран результаты расчёта зарплат по месяцам."""
    print("\nРасчёт 'на руки' по месяцам:\n")

    for month, salary in net_salaries:
        print(f"{month}: {salary:.2f} руб.")

def calculate_and_save(gross_salary: float, start_month_index: int, output_path: str = None, initial_income: float = 0.0) -> None:
    """Основная функция: рассчитывает, выводит и сохраняет результаты."""
    results = calculate_net_salaries(gross_salary, start_month_index, initial_income)
    print_results(results)
    file_path = save_to_excel(results, filename=output_path)
    print(f"\nФайл сохранён: {os.path.abspath(file_path)}\n")

def find_gross_salary_for_target_net(
    target_net: float,
    start_month_index: int,
    initial_income: float = 0.0,
    precision: float = 0.5,
    max_iter: int = 100
) -> Tuple[float, List[Tuple[str, float]]]:

    low = target_net
    high = target_net * 2

    for _ in range(max_iter):
        mid = (low + high) / 2
        net_salaries = calculate_net_salaries(mid, start_month_index, initial_income)
        last_month_salary = net_salaries[-1][1]

        if abs(last_month_salary - target_net) < precision:
            return mid, net_salaries
        elif last_month_salary < target_net:
            low = mid
        else:
            high = mid

    return mid, net_salaries


def run_calculator_with_input():
    gross = float(input("Введите зарплату до вычета налога: "))
    start_month = int(input("С какого месяца начинаем расчёт? (0 - январь, 11 - декабрь): "))

    initial_income = 0.0
    if start_month > 0:
        initial_income = float(input("Введите сумму дохода, полученного с января до начала расчёта (в рублях): "))

    calculate_and_save(gross, start_month, initial_income=initial_income)

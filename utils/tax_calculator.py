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

        # Получаем корневую директорию проекта
    root_dir = os.path.abspath(os.path.dirname(__file__))  # __file__ указывает на путь текущего файла
    root_dir = os.path.dirname(root_dir)  # Поднимаемся на один уровень выше (к корню проекта)

    # Папка для сохранения файла будет в корне проекта
    output_folder = os.path.join(root_dir, "files")  # Путь к папке 'files' в корне проекта

    # Создаем папку, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_path = os.path.join(output_folder, "net_salaries.xlsx")

    # Создание Excel файла
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Зарплата"

    # Заполнение заголовков
    sheet['A1'] = 'Месяц'
    sheet['B1'] = 'Зарплата на руки'

    # Заполнение данными
    for i, net_salary in enumerate(net_salaries):
        sheet[f'A{i + 2}'] = months[i]  # Название месяца
        sheet[f'B{i + 2}'] = f'{net_salary:.2f} руб.'  # Зарплата с точностью до двух знаков

    # Сохранение файла
    wb.save(file_path)

    # Вывод пути к файлу
    print(f"\nФайл net_salaries.xlsx сохранён в папке {os.path.abspath(output_folder)}\n")
    return net_salaries, months

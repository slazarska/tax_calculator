import os
import pytest
from openpyxl import load_workbook
from utils.tax_calculator import calculate_net_salary

@pytest.fixture
def setup_and_teardown():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.dirname(root_dir)

    output_folder = os.path.join(root_dir, "files")
    file_path = os.path.join(output_folder, "net_salaries.xlsx")

    # Удаляем файл перед тестом
    if os.path.exists(file_path):
        os.remove(file_path)

    yield file_path

    # Удаляем файл после теста
    if os.path.exists(file_path):
        os.remove(file_path)

def test_excel_file_creation(setup_and_teardown):
    file_path = setup_and_teardown

    #TODO random test date
    calculate_net_salary(100000)
    #TODO soft-assert
    assert os.path.exists(file_path), "Excel файл не был создан!"

    wb = load_workbook(file_path)
    sheet = wb.active

    assert sheet['A1'].value == 'Месяц', "Заголовок 'Месяц' неверен!"
    assert sheet['B1'].value == 'Зарплата на руки', "Заголовок 'Зарплата на руки' неверен!"
    assert sheet['A2'].value == 'Январь', "Месяц в первой строке неверен!"
    assert sheet['B2'].value.endswith(" руб."), "Зарплата в первой строке неверна!"

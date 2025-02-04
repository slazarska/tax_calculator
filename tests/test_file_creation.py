import os
import pytest
from openpyxl import load_workbook
from utils.tax_calculator import calculate_net_salary

@pytest.fixture
def setup_and_teardown():
    # Получаем корень проекта
    root_dir = os.path.abspath(os.path.dirname(__file__))  # __file__ указывает на текущий файл
    root_dir = os.path.dirname(root_dir)  # Поднимаемся на один уровень выше (к корню проекта)

    output_folder = os.path.join(root_dir, "files")  # Папка 'files' будет в корне проекта
    file_path = os.path.join(output_folder, "net_salaries.xlsx")

    # Удаляем файл перед тестом
    if os.path.exists(file_path):
        os.remove(file_path)

    # Перед каждым тестом возвращаем путь к файлу
    yield file_path

    # Удаляем файл после теста
    if os.path.exists(file_path):
        os.remove(file_path)

def test_excel_file_creation(setup_and_teardown):
    """Тестируем, что Excel файл создается в папке files и содержит правильные данные"""
    file_path = setup_and_teardown

    # Запускаем функцию для расчета зарплаты
    calculate_net_salary(100000)  # Передаем произвольную зарплату (например, 100000)

    # Проверяем, что файл был создан
    assert os.path.exists(file_path), "Excel файл не был создан!"

    # Открываем созданный Excel файл
    wb = load_workbook(file_path)
    sheet = wb.active

    # Проверяем, что заголовки корректны
    assert sheet['A1'].value == 'Месяц', "Заголовок 'Месяц' неверен!"
    assert sheet['B1'].value == 'Зарплата на руки', "Заголовок 'Зарплата на руки' неверен!"

    # Проверяем, что данные для первого месяца записаны корректно
    assert sheet['A2'].value == 'Январь', "Месяц в первой строке неверен!"
    assert sheet['B2'].value.endswith(" руб."), "Зарплата в первой строке неверна!"

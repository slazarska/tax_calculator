from data.months import months
from utils.tax_calculator import calculate_net_salaries, print_results, save_to_excel, find_gross_salary_for_target_net

def main():
    # Выбор режима работы
    while True:
        user_mode = input(
            "Выберите режим:\n"
            "1 — расчёт по зарплате до вычета\n"
            "2 — расчёт по желаемой зарплате 'на руки'\n"
            "Ваш выбор (1/2): "
        )
        if user_mode in ('1', '2'):
            break
        print("Ошибка: введите 1 или 2\n")

    # Ввод начального месяца
    while True:
        user_month = input("Введите начальный месяц (например, 'Май'): ").capitalize()
        if user_month in months:
            start_month_index = months.index(user_month)
            break
        print(f"Ошибка: месяц должен быть одним из: {', '.join(months)}\n")

    # Ввод уже полученного дохода, если старт не с января
    initial_income = 0.0
    if start_month_index > 0:
        while True:
            try:
                initial_income = float(input("Введите сумму дохода, полученного с января по указанный месяц: "))
                if initial_income >= 0:
                    break
                print("Доход не может быть отрицательным")
            except ValueError:
                print("Ошибка: введите числовое значение")

    if user_mode == '1':
        # Режим 1 - расчёт от gross salary
        while True:
            try:
                gross_salary = float(input("Введите ежемесячную зарплату до вычета налогов: "))
                if gross_salary > 0:
                    break
                print("Зарплата должна быть положительным числом")
            except ValueError:
                print("Ошибка: введите числовое значение")

        # Расчёт, вывод и сохранение результатов
        results = calculate_net_salaries(gross_salary, start_month_index, initial_income)
        print_results(results)
        save_to_excel(results)

    else:
        # Режим 2 - расчёт от net salary
        while True:
            try:
                target_net = float(input("Введите желаемую сумму 'на руки' в месяц: "))
                if target_net > 0:
                    break
                print("Сумма должна быть положительным числом")
            except ValueError:
                print("Ошибка: введите числовое значение")

        # Поиск gross salary и вывод результатов
        gross_salary, results = find_gross_salary_for_target_net(
            target_net, start_month_index, initial_income=initial_income
        )
        print(f"Чтобы получать ~{target_net:.2f} руб. на руки, нужно зарабатывать {gross_salary:.2f} руб. до вычета налогов.")

        print_results(results)
        save_to_excel(results, filename="target_salary.xlsx")

if __name__ == "__main__":
    main()
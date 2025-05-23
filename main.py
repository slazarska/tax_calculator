from data.months import months
from utils.tax_calculator import calculate_taxed_salary, print_and_save_results, \
    find_gross_salary_for_target_net


def main():
    user_mode = input("Выберите режим: \n1 — ввести зарплату до вычета\n2 — ввести желаемую зарплату на руки\nВаш выбор (1/2): ")

    user_month = input("Введите начальный месяц (например, 'Май'): ").capitalize()
    if user_month not in months:
        print("Неверное название месяца.")
        return
    start_month_index = months.index(user_month)

    if user_mode == "1":
        gross_salary = float(input("Введите ежемесячную зарплату (до вычета налогов): "))
        net_salaries = calculate_taxed_salary(gross_salary, start_month_index)
        print_and_save_results(net_salaries)
    elif user_mode == "2":
        target_net = float(input("Введите желаемую сумму 'на руки' в месяц: "))
        gross_salary, net_salaries = find_gross_salary_for_target_net(target_net, start_month_index)
        print(f"\nЧтобы получать ~{target_net:.2f} руб. на руки, нужно зарабатывать {gross_salary:.2f} руб. до вычета налогов.")
        print_and_save_results(net_salaries, filename_suffix="_from_target")
    else:
        print("Некорректный выбор режима.")


if __name__ == "__main__":
    main()
from utils.tax_calculator import calculate_net_salary

if __name__ == "__main__":
    gross_salary = float(input("Введите ежемесячную зарплату до налогов: "))
    net_salaries, months = calculate_net_salary(gross_salary)

    for month, salary in zip(months, net_salaries):
        print(f"{month}: {salary:.2f} руб. на руки")

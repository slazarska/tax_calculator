import unittest
from utils.tax_calculator import calculate_net_salaries


class TestSalaryCalculator(unittest.TestCase):

    def test_low_salary(self):
        """Тест для зарплаты, которая полностью облагается 13%"""
        gross_salary = 100_000  # 1.2 млн в год, ниже 2.4 млн
        net_salaries = calculate_net_salaries(gross_salary, 0)
        expected_net = gross_salary * 0.87  # 13% налог

        self.assertAlmostEqual(net_salaries[0][1], expected_net, places=2)

    def test_middle_salary(self):
        """Тест для зарплаты, попадающей во вторую налоговую категорию"""
        gross_salary = 300_000  # 3.6 млн в год
        start_month_index = 0
        net_salaries = calculate_net_salaries(gross_salary, start_month_index)

        first_month_net = net_salaries[0][1]
        self.assertGreater(first_month_net, 300_000 * 0.85)
        self.assertLessEqual(first_month_net, 300_000 * 0.87)

    def test_high_salary(self):
        """Тест для высокой зарплаты, затрагивающей несколько налоговых уровней"""
        gross_salary = 2_000_000  # 24 млн в год
        start_month_index = 0
        net_salaries = calculate_net_salaries(gross_salary, start_month_index)

        first_month_net = net_salaries[0][1]
        self.assertGreater(first_month_net, 2_000_000 * 0.80)
        self.assertLessEqual(first_month_net, 2_000_000 * 0.87)

    def test_extreme_salary(self):
        """Тест для зарплаты, попадающей под все налоговые уровни"""
        gross_salary = 10_000_000  # 120 млн в год
        start_month_index = 0
        net_salaries = calculate_net_salaries(gross_salary, start_month_index)

        first_month_net = net_salaries[0][1]
        self.assertGreaterEqual(first_month_net, 8_000_000)
        self.assertLessEqual(first_month_net, 8_500_000)

if __name__ == "__main__":
    unittest.main()

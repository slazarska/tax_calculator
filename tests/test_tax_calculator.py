import unittest
from utils.tax_calculator import calculate_net_salary

class TestSalaryCalculator(unittest.TestCase):

    def test_low_salary(self):
        """Тест для зарплаты, которая полностью облагается 13%"""
        gross_salary = 100_000  # 1.2 млн в год, ниже 2.4 млн
        net_salaries, _ = calculate_net_salary(gross_salary)
        expected_net = gross_salary * 0.87  # 13% налог

        self.assertAlmostEqual(net_salaries[0], expected_net, places=2)

    def test_middle_salary(self):
        """Тест для зарплаты, попадающей во вторую налоговую категорию"""
        gross_salary = 300_000  # 3.6 млн в год, частично 13%, частично 15%
        net_salaries, _ = calculate_net_salary(gross_salary)

        self.assertGreater(net_salaries[0], 300_000 * 0.85)  # Должно быть выше 85% от ЗП
        self.assertLessEqual(net_salaries[0], 300_000 * 0.87)  # И ниже 87% от ЗП

    def test_high_salary(self):
        """Тест для высокой зарплаты, затрагивающей несколько налоговых уровней"""
        gross_salary = 2_000_000  # 24 млн в год, попадает в 4 категории
        net_salaries, _ = calculate_net_salary(gross_salary)

        self.assertGreater(net_salaries[0], 2_000_000 * 0.80)  # Часть дохода попадает под 20%
        self.assertLessEqual(net_salaries[0], 2_000_000 * 0.87)

    def test_extreme_salary(self):
        """Тест для зарплаты, попадающей под все налоговые уровни"""
        gross_salary = 10_000_000  # 120 млн в год, попадает в 22% налог
        net_salaries, _ = calculate_net_salary(gross_salary)

        self.assertGreaterEqual(net_salaries[0], 8_000_000)  # Должно быть хотя бы 8 млн
        self.assertLessEqual(net_salaries[0], 8_500_000)  # Но не больше 8.5 млн

if __name__ == "__main__":
    unittest.main()

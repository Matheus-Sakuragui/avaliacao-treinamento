from flaskr.helpers.math_strategy import (ArithmeticProgressionStrategy,
                                          GeometricProgressionStrategy)
from tests.functional.core.base_test import BaseTestCase


class TestMathStrategy(BaseTestCase):

    def test_pa_calculate(self):
        math_strategy = ArithmeticProgressionStrategy()
        result = math_strategy.calculate([1, 3, 4])
        assert result == 10

    def test_pg_calculate(self):
        math_strategy = GeometricProgressionStrategy()
        result = math_strategy.calculate([2, 2, 4])
        assert result == 16

import abc


class AbstractMathStrategy():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate(self, parameters):
        raise NotImplementedError("Abstract method to be implemented by subclass")


class ArithmeticProgressionStrategy(AbstractMathStrategy):

    def calculate(self, parameters):
        first_element = parameters[0]
        ratio = parameters[1]
        qty_elements = parameters[2]

        return first_element + (qty_elements - 1) * ratio


class GeometricProgressionStrategy(AbstractMathStrategy):

    def calculate(self, parameters):
        first_element = parameters[0]
        ratio = parameters[1]
        qty_elements = parameters[2]

        return first_element * (ratio ** (qty_elements - 1))

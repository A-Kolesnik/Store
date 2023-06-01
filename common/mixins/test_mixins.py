class ModelFieldParamsMixin(object):

    """Миксин для исследования значений параметра всех полей модели

    Методы:
        1. research_equal_parameter_value()

    """

    def research_equal_parameter_value(self, record, pairs_field_parameter_value, parameter_name):
        """Выполняет контроль равенства значения параметра поля модели с ожидаемым значением"""
        for field_name, expected_parameter_value in pairs_field_parameter_value.items():
            field_value = record._meta.get_field(field_name)
            real_parameter_value = getattr(field_value, parameter_name)
            self.assertEqual(
                expected_parameter_value,
                real_parameter_value,
                f'Неожиданное значение параметра {parameter_name} поля {field_name}\n'
                f'Ожидаемое значение: {expected_parameter_value}\n'
                f'Полученное значение: {real_parameter_value}\n')


class TestVerboseNameMixin(ModelFieldParamsMixin):

    """Миксин для выполнения тестирования параметра поля модели verbose_name

    Методы:
        1. run_test_verbose_name()

    """

    def run_test_verbose_name(self, record, pairs_field_parameter_value):
        """Выполняет тестирование значения параметра verbose_name всех полей модели

        Тестирование выполняется с использованием одной записи модели

        """
        super(TestVerboseNameMixin, self).research_equal_parameter_value(
            record,
            pairs_field_parameter_value,
            'verbose_name'
        )

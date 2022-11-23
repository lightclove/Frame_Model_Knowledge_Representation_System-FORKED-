from frame import Slot
from el_scheme import Diod, Transistor, Resistor, Capacitor, Inductance, Component, CheckPoint


__all__ = ('KnowledgeAccumulator',)


class KnowledgeAccumulator:
    """
    Модуль накопления знаний
    """
    def __init__(self, scheme):
        """
        :param scheme: Электрическая схема
        :type scheme: el_scheme.Scheme
        """
        self._scheme = scheme

    def learning(self):
        """
        Функция извлечения знаний
        """
        menu_text = (
            '\nМодуль накопления знаний:\n'
            '1. Вывести компоненты и контрольные точки схемы\n'
            '2. Добавить компонент\n'
            '3. Удалить компонент\n'
            '4. Добавить контрольную точку\n'
            '5. Удалить контрольную точку\n'
            '\nПункт меню: '
        )

        menu_methods = [
            self._scheme.print,
            self.add_component,
            self.remove_component,
            self.add_check_point,
            self.remove_check_point,
        ]

        try:
            while True:
                print(menu_text)
                menu_method_index = int(input()) - 1

                result = menu_methods[menu_method_index]()

                if menu_method_index != 0 and result:
                    self._scheme.save_to_db()

        except (ValueError, IndexError):
            print('\nВыход...')

    def add_component(self, component=None):
        """
        Функция добавления компонента
        :type component: el_scheme.Component
        """
        if component is None:
            menu_text = (
                '1. Добавить диод\n'
                '2. Добавить транзистор\n'
                '3. Добавить резистор\n'
                '4. Добавить конденсатор\n'
                '5. Добавить катушку индуктивности\n'
            )
            component_types = [Diod, Transistor, Resistor, Capacitor, Inductance]
            print(menu_text)

            try:
                component_type_index = int(input()) - 1
                ComponentType = component_types[component_type_index]

            except (ValueError, IndexError):
                return False

            component = ComponentType()
            self._request_frame_data(component)

        if self.is_existing_component(component):
            print('Данный компонент уже присутствует в схеме.')
            return False

        self._scheme.add_components(component)

        return True

    def remove_component(self, symbol=None):
        """
        Функция удаления компонента
        :param symbol: Символьное обозначение компонента
        """
        if symbol is None:
            print('Введите символьное обозначение компонента')
            symbol = input()

        if not self.is_existing_component(symbol):
            print('Данный компонент не присутствует в схеме')
            return False

        return self._remove_element_by_symbol(self._scheme.elements, symbol)

    def is_existing_component(self, component):
        """
        Функция проверки компонента на существование
        :type component: el_scheme.Component
        """
        if isinstance(component, str):
            component = Component(symbol=component)

        return not all(
            element.symbol.value != component.symbol.value
            for element in self._scheme.elements
        )

    def add_check_point(self, check_point=None):
        """
        Функция добавления контрольной точки
        :type check_point: el_scheme.CheckPoint
        """
        if not check_point:
            check_point = CheckPoint()
            self._request_frame_data(check_point)

        if self.is_existing_check_point(check_point):
            print('Данная контрольная точка уже присутствует в схеме.')
            return False

        self._scheme.add_check_points(check_point)

        return True

    def remove_check_point(self, check_point=None):
        """
        Функция удаления контрольной точки
        :type check_point: Наименование контрольной точки
        """
        if check_point is None:
            print('Введите наименование контрольной точки')
            check_point = input()

        if not self.is_existing_check_point(check_point):
            print('Данная контрольная точка не присутствует в схеме')
            return False

        return self._remove_element_by_symbol(self._scheme.check_points, check_point)

    def is_existing_check_point(self, check_point):
        """
        Функция проверки контрольной точки на существование
        :type check_point: el_scheme.CheckPoint
        """
        if isinstance(check_point, str):
            check_point = CheckPoint(symbol=check_point)

        return not all(
            point.symbol.value != check_point.symbol.value
            for point in self._scheme.check_points
        )

    @staticmethod
    def _request_frame_data(frame):
        print('Добавление "{}"'.format(frame.name))
        for attr_name in dir(frame):
            slot = getattr(frame, attr_name)
            if isinstance(slot, Slot) and not slot.is_system and slot.value is None:
                print('Введите "{}":'.format(slot.name))
                slot.value = input()

    @staticmethod
    def _remove_element_by_symbol(elements, symbol):
        if isinstance(symbol, Component):
            symbol = symbol.symbol.value

        for element in elements:
            if element.symbol.value == symbol:
                elements.remove(element)
                print(element, 'удален')
                return True

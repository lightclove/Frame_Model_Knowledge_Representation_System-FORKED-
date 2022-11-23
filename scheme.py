import json

import settings
from frame import Frame, Slot
from frame.slot_types import FramePtrList


class Scheme(Frame):
    """
    Электрическая схема
    """
    _name_ = 'Электрическая схема'
    _slots_ = {
        'IS_A':    (FramePtrList(), Slot.IT_OVERRIDE),
        'PART_OF': (FramePtrList(), Slot.IT_OVERRIDE),

        'elements':     ('Элементы',          FramePtrList(), Slot.IT_UNIQUE),
        'check_points': ('Контрольные точки', FramePtrList(), Slot.IT_UNIQUE),
    }

    def add_components(self, *components):
        """
        Добавить электронные компоненты
        :type components: tuple[el_scheme.Component]
        """
        for component in components:
            self.elements.append(component)

    def add_check_points(self, *check_points):
        """
        Добавить контрольные точки
        :type check_points: tuple[el_scheme.CheckPoint]
        """
        for check_point in check_points:
            self.check_points.append(check_point)

    def print(self):
        """
        Вывести на экран содержимое
        """
        print(self)
        print('\t*** Электронные компоненты ***')
        for element in self.elements:
            print('\t{}'.format(element))
        print()

        if self.check_points.value:
            print('\t*** Контрольные точки ***')
            for point in self.check_points:
                print('\t{}'.format(point))

    def serialize(self):
        return {
            'name': self._frame_name,
            'type': self.__class__.__name__,
            'elements': [
                component.serialize()
                for component in self.elements
            ],
            'check_points': [
                check_point.serialize()
                for check_point in self.check_points
            ]
        }

    def save_to_db(self):
        """
        Сохранение в базу данных (файл формата JSON)
        """
        data = self.serialize()
        file_path = settings.DB_FILE_PATH

        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=2)

        print('Схема "{}" сохранена в {}\n'.format(self, file_path))

    @classmethod
    def load_from_db(cls):
        """
        Загрузка схемы из базы данных (файл формата JSON)
        :return Объект типа Scheme
        """
        from .check_point import CheckPoint

        scheme = cls()

        file_path = settings.DB_FILE_PATH

        with open(file_path, 'r') as infile:
            data = json.load(infile)

        scheme._frame_name = data['name']

        for element in data['elements']:
            component_class = element.pop('type')
            component = getattr(__import__('el_scheme'), component_class)(**element)
            scheme.add_components(component)

        scheme.add_check_points(*[
            CheckPoint(**check_point)
            for check_point in data['check_points']
        ])
        print('Схема "{}" загружена из {}\n'.format(scheme, file_path))

        return scheme

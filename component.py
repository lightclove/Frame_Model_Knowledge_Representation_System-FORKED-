from frame import Frame, Slot, FramePtrList, Integer, Real, Text, Bool, Table
from .scheme import Scheme

__all__ = (
    'Component', 'ActiveComponent', 'PassiveComponent', 'Diod', 'Transistor', 'Resistor', 'Capacitor', 'Inductance'
)


class Component(Frame):
    """
    Электронный компонент
    """
    _name_ = 'Электронный компонент'
    _slots_ = {
        'IS_A':     (FramePtrList(),       Slot.IT_OVERRIDE),
        'PART_OF':  (FramePtrList(Scheme), Slot.IT_OVERRIDE),

        'title':        ('Наименование',            Text(), Slot.IT_UNIQUE),
        'is_active':    ('Активный?',               Bool(), Slot.IT_UNIQUE),
        'symbol':       ('Символьное обозначение',  Text(), Slot.IT_UNIQUE),
        'graphic':      ('Графическое обозначение', Text(), Slot.IT_UNIQUE),
    }

    def __repr__(self):
        return '<{} "{}" ({})>'.format(
            self._frame_name,
            self.symbol.value,
            'активный' if self.is_active.value else 'не активный'
        )

    def __eq__(self, other):
        return self.symbol.value == other.symbol.value


class ActiveComponent(Component):
    """
    Активный электронный компонент
    """
    _name_ = 'Активный компонент'
    _slots_ = {
        'IS_A':      (FramePtrList(Component), Slot.IT_UNIQUE),
        'is_active': ('Активный?', Bool(True), Slot.IT_SAME),
    }


class PassiveComponent(Component):
    """
    Пассивный электронный компонент
    """
    _name_ = 'Пассивный компонент'
    _slots_ = {
        'IS_A':      (FramePtrList(Component),  Slot.IT_UNIQUE),
        'is_active': ('Активный?', Bool(False), Slot.IT_SAME),
    }


class Diod(ActiveComponent):
    """
    Диод
    """
    _name_ = 'Диод'
    _slots_ = {
        'IS_A': (FramePtrList(ActiveComponent), Slot.IT_SAME),

        'vac':                      ('ВАХ',                              Table(), Slot.IT_UNIQUE),
        'operating_switching_freq': ('Рабочая частота переключения, Гц', Real(),  Slot.IT_UNIQUE),
    }


class Transistor(ActiveComponent):
    """
    Транзистор
    """
    _name_ = 'Транзистор'
    _slots_ = {
        'IS_A': (FramePtrList(ActiveComponent), Slot.IT_SAME),

        'transition_type':                         ('Тип перехода',                 Text(), Slot.IT_OVERRIDE),
        'current_transfer_ratio':                  ('Коэффициент передачи по току', Real(), Slot.IT_UNIQUE),
        'reverse_collector_current':               ('Обратный ток коллектора, А',   Real(), Slot.IT_UNIQUE),
        'input_resistance':                        ('Входное сопротивление, Ом',    Real(), Slot.IT_UNIQUE),
        'limit_freq_base_current_transfer_factor': ('Предельная частота коэффициента '
                                                    'передачи тока базы, Гц',       Real(), Slot.IT_UNIQUE),
    }

    def __repr__(self):
        return '<{} "{}">'.format(self._frame_name, self.symbol.value)


class Resistor(PassiveComponent):
    """
    Резистор
    """
    _name_ = 'Резистор'
    _slots_ = {
        'IS_A': (FramePtrList(ActiveComponent), Slot.IT_SAME),

        'rated_resistance':             ('Номинальное сопротивление, Ом',           Integer(), Slot.IT_UNIQUE),
        'limiting_operating_voltage':   ('Предельное рабочее напряжение, В',        Real(),    Slot.IT_UNIQUE),
        'resistance_temperature_coeff': ('Температурный коэффициент сопротивления', Real(),    Slot.IT_UNIQUE),
    }

    def __repr__(self):
        return '<{} "{}" ({} Ом)>'.format(self._frame_name, self.symbol.value, self.rated_resistance.value)


class Capacitor(PassiveComponent):
    """
    Конденсатор
    """
    _name_ = 'Конденсатор'
    _slots_ = {
        'IS_A': (FramePtrList(ActiveComponent), Slot.IT_SAME),

        'capacity':          ('Ёмкость',                Integer(), Slot.IT_UNIQUE),
        'specific_capacity': ('Удельная ёмкость',       Real(),    Slot.IT_UNIQUE),
        'rated_voltage':     ('Номинальное напряжение', Real(),    Slot.IT_UNIQUE),
    }

    def __repr__(self):
        return '<{} "{}" ({} мкФ)>'.format(self._frame_name, self.symbol.value, self.capacity.value)


class Inductance(PassiveComponent):
    """
    Катушка индуктивности
    """
    _name_ = 'Катушка индуктивности'
    _slots_ = {
        'IS_A': (FramePtrList(ActiveComponent), Slot.IT_SAME),

        'inductance':      ('Индуктивность, Гн',        Integer(), Slot.IT_UNIQUE),
        'loss_resistance': ('Сопротивление потерь, Ом', Real(),    Slot.IT_UNIQUE),
        'q_factor':        ('Добротность',              Real(),    Slot.IT_UNIQUE),
    }

    def __repr__(self):
        return '<{} "{}" ({} Гн)>'.format(self._frame_name, self.symbol.value, self.inductance.value)

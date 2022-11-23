from frame import Frame, Slot, FramePtrList, Text, Real
from .scheme import Scheme


__all__ = ('CheckPoint',)


class CheckPoint(Frame):
    """
    Контрольная точка
    """
    _name_ = 'Контрольная точка'
    _slots_ = {
        'IS_A':     (FramePtrList(),       Slot.IT_OVERRIDE),
        'PART_OF':  (FramePtrList(Scheme), Slot.IT_OVERRIDE),

        'symbol':               ('Наименование',             Text(), Slot.IT_UNIQUE),
        'permissible_voltage':  ('Допустимое напряжение, В', Real(), Slot.IT_UNIQUE),
        'error':                ('Погрешность',              Real(), Slot.IT_UNIQUE),
    }

    def __repr__(self):
        return '<{} "{}" ({} ± {} В)>'.format(
            self._frame_name, self.symbol.value, self.permissible_voltage.value, self.error.value or 0
        )

    def __eq__(self, other):
        return self.symbol.value == other.symbol.value

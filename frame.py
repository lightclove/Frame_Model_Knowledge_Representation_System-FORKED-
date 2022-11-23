from copy import deepcopy

from .slot import Slot


__all__ = ('Frame',)


class Frame:
    """
    Фрейм
    """
    _name_ = 'Фрейм'
    _slots_ = {}

    def __repr__(self):
        return '<{}>'.format(self._frame_name)

    def __init__(self, name=None, **slot_values):
        self._frame_name = name or self._name_

        self._collect_slots()
        self._set_slots_for_instance(**slot_values)

    def _collect_slots(self):
        """
        Агрегация слотов от своих предков
        """
        self.__slots = deepcopy(self._slots_)

        parents = self.__class__.__mro__
        for parent in reversed(parents):
            if parent not in (self.__class__, object, type):
                self.__slots.update(parent._slots_)
                for slot_attr, params in parent._slots_.items():
                    if not params:
                        continue
                    name, value, inheritance_type = self._get_slot_args(slot_attr, params)

                    if inheritance_type == Slot.IT_UNIQUE:
                        self.__slots[slot_attr] = (
                            (value.__class__(), inheritance_type)
                            if name in Slot.SYSTEMS_NAMES else
                            (name, value.__class__(), inheritance_type)
                        )

    def _set_slots_for_instance(self, **slot_values):
        """
        Инициализация слотов у конечного объекта
        """
        for attr_name, params in self.__slots.items():
            if params is None:
                continue
            slot = Slot(*self._get_slot_args(attr_name, params))

            if slot.inheritance_type != Slot.IT_SAME and attr_name in slot_values:
                slot.value = slot_values[attr_name]

            setattr(self, attr_name, slot)

    @staticmethod
    def _get_slot_args(name, params):
        if name in Slot.SYSTEMS_NAMES:
            return name, params[0], params[1]
        return params[0], params[1], params[2]

    @property
    def name(self):
        return self._frame_name

    def serialize(self):
        data = {
            attr: getattr(self, attr).value
            for attr in dir(self)
            if isinstance(getattr(self, attr), Slot) and (attr not in Slot.SYSTEMS_NAMES)
        }
        data['name'] = self._frame_name
        data['type'] = self.__class__.__name__
        return data

    @classmethod
    def deserialize(cls, data):
        """
        :type data: dict
        """
        frame = cls()

        for key, value in data.items():
            getattr(frame, key).value = value

        return frame

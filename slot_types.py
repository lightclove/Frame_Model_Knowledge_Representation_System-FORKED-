__all__ = ('SlotType', 'Integer', 'Real', 'Bool', 'Text', 'Table', 'Lisp', 'FramePtr', 'FramePtrList')


class SlotType:
    """
    Тип данных слота
    """
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return '<{} "{}">'.format(self.__class__.__name__, self.value)


class Integer(SlotType):
    """
    Целочисленный тип
    """
    def __init__(self, value=None):
        value = value and int(value)
        super().__init__(value)


class Real(SlotType):
    """
    Действительный тип
    """
    def __init__(self, value=None):
        value = value and float(value)
        super().__init__(value)


class Bool(SlotType):
    """
    Булевский тип
    """
    def __init__(self, value=None):
        value = value and bool(value)
        super().__init__(value)


class Text(SlotType):
    """
    Текст
    """
    def __init__(self, value=None):
        value = value and str(value)
        super().__init__(value)


class Table(SlotType):
    """
    Таблица
    """
    @property
    def columns(self):
        return (self.value and len(self.value)) or 0

    @property
    def rows(self):
        return (self.value and len(self.value[0])) or 0


class Lisp(SlotType):
    """
    Присоединённая процедура
    """
    pass


class FramePtr(SlotType):
    """
    Указатель на другой фрейм
    """
    pass


class FramePtrList(SlotType):
    """
    Список указателей на другие фреймы
    """
    def __init__(self, *frame_pointers):
        super().__init__(value=frame_pointers)

    def __iter__(self):
        return iter(self.value)

    def append(self, frame_pointer):
        if not self.value:
            self.value = []
        self.value.append(frame_pointer)

    def remove(self, frame_pointer):
        if not self.value:
            return
        self.value.remove(frame_pointer)

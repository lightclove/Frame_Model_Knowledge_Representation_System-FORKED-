from el_scheme import Scheme, Resistor, Transistor, Capacitor, CheckPoint
from knowledge_accumulator import KnowledgeAccumulator


def create_scheme(from_db=False):
    """
    Создать электрическую схему однокаскадного усилителя в статике
    :param from_db: Загрузить схему из базы данных
    """
    if from_db:
        return Scheme.load_from_db()

    scheme = Scheme(name='Однокаскадный усилитель')
    scheme.add_components(
        Resistor(symbol='R1', rated_resistance=8200),
        Resistor(symbol='R2', rated_resistance=4700),
        Resistor(symbol='Rк', rated_resistance=1200),
        Resistor(symbol='Rэ', rated_resistance=1000),

        Capacitor(symbol='C1', capacity=220),
        Capacitor(symbol='C2', capacity=470),
        Capacitor(symbol='Cэ', capacity=6800),

        Transistor(symbol='V1'),
    )
    scheme.add_check_points(
        CheckPoint(symbol='КТ1', permissible_voltage=11),
        CheckPoint(symbol='КТ2', permissible_voltage=7.5),
        CheckPoint(symbol='КТ3', permissible_voltage=18),
        CheckPoint(symbol='КТ4', permissible_voltage=15),
        CheckPoint(symbol='КТ5', permissible_voltage=7),
        CheckPoint(symbol='КТ6', permissible_voltage=0),
        CheckPoint(symbol='КТ7', permissible_voltage=11),
    )

    return scheme


def main():
    #create_scheme().save_to_db()
    scheme = create_scheme(from_db=True)
    KnowledgeAccumulator(scheme).learning()


if __name__ == '__main__':
    main()

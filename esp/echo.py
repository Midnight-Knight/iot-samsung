import machine
import time

class Echo:

    __sound_speed = 340
    __trig_pulse_duration_us = 10

    def __init__(self):
        print("echo start init")
        self.__trig_pin = machine.Pin(4, machine.Pin.OUT)
        self.__echo_pin = machine.Pin(15, machine.Pin.IN)
        print("echo end init")

    def cm(self, timer = False):
        self.__trig_pin.value(0)
        time.sleep_us(5)
        self.__trig_pin.value(1)
        time.sleep_us(self.__trig_pulse_duration_us)
        self.__trig_pin.value(0)
        ultrason_duration = machine.time_pulse_us(self.__echo_pin, 1, 30000)
        return self.__sound_speed * ultrason_duration / 20000

    def get(self):
        measurements = []

        # Сбор 5 измерений
        for _ in range(5):
            measurements.append(self.cm())
            time.sleep(0.1)  # Небольшая задержка между измерениями

        # Проверка на повторяющиеся значения
        counts = {}
        for value in measurements:
            if value in counts:
                counts[value] += 1
            else:
                counts[value] = 1

        # Поиск значения с наибольшим количеством повторов
        max_count = 0
        most_common_value = None
        for value, count in counts.items():
            if count > max_count:
                max_count = count
                most_common_value = value

        # Если хотя бы двух повторяющихся значений нет, выбирается среднее значение
        if max_count < 2:
            most_common_value = sum(measurements) / len(measurements)

        # Проверка на отрицательные значения
        if most_common_value < 0:
            most_common_value = 0

        return most_common_value
from machine import Pin, ADC

class Water:

    def __init__(self):
        print("water start init")
        self.__water_level_pin = Pin(16, Pin.IN)
        self.__water_turbidity_pin = ADC(Pin(32))
        self.__water_turbidity_pin.width(ADC.WIDTH_12BIT)
        self.__water_turbidity_pin.atten(ADC.ATTN_11DB)
        self.__water_level = self.__water_level_pin.value()
        self.__water_turbidity = self.__water_turbidity_pin.read()
        #self.__water_level_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.func_water_level)
        print("water end init")

    def func_water_level(self, pin = False):
        self.__water_level = self.__water_level_pin.value()
        return self.__water_level

    def func_water_turbidity(self, pin = False):
        self.__water_turbidity = self.__water_turbidity_pin.read()
        return self.__water_turbidity
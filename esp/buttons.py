import machine

class Buttons:
    
    def __init__(self):
        print("buttons start init")
        self.__b1 = machine.Pin(5, machine.Pin.IN)
        self.__b2 = machine.Pin(18, machine.Pin.IN)
        self.__b3 = machine.Pin(19, machine.Pin.IN)
        self.__b4 = machine.Pin(21, machine.Pin.IN)
        self.__dt1 = machine.Timer(2)
        self.__dt2 = machine.Timer(3)
        self.__dt3 = machine.Timer(4)
        self.__dt4 = machine.Timer(5)
        self.__bp1 = False
        self.__bp2 = False
        self.__bp3 = False
        self.__bp4 = False
        self.__be1 = True
        self.__be2 = True
        self.__be3 = True
        self.__be4 = True
        self.__b1.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.func_button_1)
        self.__b2.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.func_button_2)
        self.__b3.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.func_button_3)
        self.__b4.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.func_button_4)
        print("buttons end init")

    def button1_enabled_cb(self, timer):
        self.__be1 = True

    def func_button_1(self, pin):
        if self.__be1:
            self.__be1 = False
            self.__bp1 = True
            self.__dt1.init(mode=machine.Timer.ONE_SHOT, period=300, callback=self.button1_enabled_cb)

    def button2_enabled_cb(self, timer):
        self.__be2 = True

    def func_button_2(self, pin):
        if self.__be2:
            self.__be2 = False
            self.__bp2 = True
            self.__dt2.init(mode=machine.Timer.ONE_SHOT, period=300, callback=self.button2_enabled_cb)

    def button3_enabled_cb(self, timer):
        self.__be3 = True

    def func_button_3(self, pin):
        if self.__be3:
            self.__be3 = False
            self.__bp3 = True
            self.__dt3.init(mode=machine.Timer.ONE_SHOT, period=300, callback=self.button3_enabled_cb)

    def button4_enabled_cb(self, timer):
        self.__be4 = True

    def func_button_4(self, pin):
        if self.__be4:
            self.__be4 = False
            self.__bp4 = True
            self.__dt4.init(mode=machine.Timer.ONE_SHOT, period=300, callback=self.button4_enabled_cb)

    def get_button_1(self):
        return self.__bp1
    
    def get_button_2(self):
        return self.__bp2
    
    def get_button_3(self):
        return self.__bp3
    
    def get_button_4(self):
        return self.__bp4
    
    def set_button_1(self):
        self.__bp1 = False

    def set_button_2(self):
        self.__bp2 = False

    def set_button_3(self):
        self.__bp3 = False

    def set_button_4(self):
        self.__bp4 = False
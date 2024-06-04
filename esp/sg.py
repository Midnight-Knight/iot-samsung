import machine

class Sg90:

    def __init__(self, open_hatch = True):
        print("sg90 start init")
        self.__sg90 = machine.PWM(machine.Pin(22, mode=machine.Pin.OUT))
        self.__sg90.freq(50)
        self.__open_hatch = open_hatch
        self.switch()
        print("sg90 end init")
        
    def get(self):
        return self.__open_hatch
    
    def switch(self, timer = False):
        try:
            if self.__open_hatch:
                self.__sg90.duty(170)
            else:
                self.__sg90.duty(10)
            self.__open_hatch = not self.__open_hatch
        except Exception as e:
            print(f'Error! {e}')

    def change(self, status):
        try:
            if status:
                self.__sg90.duty(170)
            else:
                self.__sg90.duty(10)
            self.__open_hatch = status
        except Exception as e:
            print(f'Error! {e}')
class Car:

    def __init__(self):
        self.starter = Starter()
        self.alarm = Alarm()
        self.start_button = False
        self.braking = False

    def start(self):
        self.start_button = True
        self._step()
        self.start_button = False
        self._step()

    def _step(self):
        self.starter._step(self.start_button, self.braking)
        self.alarm._step()

class Alarm:
    def _step(self): pass

class Starter:

    Started = 3
    Starting = 1
    Shutting_down = 2
    Off = 0

    def __init__(self):
        self._state = Starter.Off

    def _step(self, start_button, braking):
        self._state = Starter.transition(self._state, start_button, braking)

    @staticmethod
    def transition(inp_state, start_button, braking):
        return inp_state

def drive_car():
    car = Car()
    print('Starting Car')
    car.start()
    print('Car started!')

if __name__ == "__main__":
    drive_car()

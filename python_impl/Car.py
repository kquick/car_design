class Car:

    def __init__(self):
        self.starter = Starter()
        self.alarm = Alarm()
        self.start_button = False
        self.braking = False
        self.alarm_button = False

    def start(self):
        self.start_button = True
        self._step()
        self.start_button = False
        self._step()

    def _step(self):
        self.starter._step(self.start_button, self.braking)
        self.alarm._step(self.starter._state, self.alarm_button)

class Alarm:
    "Finite State Machine for the alarm system"

    Disabled = 0
    Enabled = 1

    def __init__(self):
        self._state = Alarm.Disabled

    def _step(self, starter_state, alarm_button):
        self._state = Alarm.transition(self._state, starter_state, alarm_button)

    @staticmethod
    def transition(alarm,  # this is the input state; the name must match the
                           # kind2 variable name.
                   starter_state, alarm_button):
        return alarm

class Starter:
    "Finite State Machine for the starter system"

    Started = 0
    Starting = 1
    Off = 2

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

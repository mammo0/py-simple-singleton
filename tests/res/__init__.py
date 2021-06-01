class TSingletonBase():
    def __init__(self, arg1: str='', arg2: str='') -> None:
        self._param1 = arg1
        self._param2 = arg2

    @property
    def param1(self):
        return self._param1

    @param1.setter
    def param1(self, value: str):
        self._param1 = value

    @property
    def param2(self):
        return self._param2

    @param2.setter
    def param2(self, value: str):
        self._param2 = value

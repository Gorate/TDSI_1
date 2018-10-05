from copy import deepcopy


class CPR:

    def __init__(self, name, thrust :list, start_time:list, stop_time:list):
        self.name = name
        self.thrust = thrust
        self.start_time = start_time
        self.stop_time = stop_time

    def get_time_rigth(self):
        tmp = self.start_time[0]
        print(tmp)
        for i in range(len(self.start_time)):
            self.start_time[i] -= tmp
            self.stop_time[i]  -= tmp



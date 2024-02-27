class Process: 
    def __init__(self, a: int, b: int, c: int):
        self.processId = a
        self.arrivalTime = b
        self.burstTime = c
        self.startTime = 0
        self.endTime = 0
        self.waitingTime = 0
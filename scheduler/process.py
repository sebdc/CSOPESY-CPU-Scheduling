class Process: 
    def __init__(self, a = 0, b = 0, c = 0):
        self.processId = a
        self.arrivalTime = b
        self.burstTime = c
        self.startTime = 0
        self.endTime = 0
        self.waitingTime = 0

    def copyProcess(self, process: 'Process') -> None:
        if isinstance(process, Process):
            self.processId = process.processId
            self.arrivalTime = process.arrivalTime
            self.burstTime = process.burstTime
            self.startTime = process.startTime
            self.endTime = process.endTime
            self.waitingTime = process.waitingTime
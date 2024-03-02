from typing import List
from .process import Process

class CPUScheduler:
    def __init__(self):
        # Program Input
        self.algorithmId = None
        self.numProcesses = None
        self.timeQuantum = None 

        # Processes Details
        self.processes = []
        self.executedProcesses = []
        self.queue = []

        self.completionTime = None
        self.totalWaitingTime = 0
        self.currentTime = 0


    def readInputFile(self, fileName: str):
        from .input_handler import InputHandler

        try: 
            x, y, z, completionTime, processes = InputHandler.readProcessesFromFile(fileName)

            if processes is not None:
                self.algorithmId = x
                self.numProcesses = y
                self.timeQuantum = z
                self.completionTime = completionTime
                self.processes = processes
            else:
                print( 'Error: Invalid inputs or file not found.' )

        except FileNotFoundError:
            print(f'Error: File \'{fileName}\' not found.')
        except ValueError as ve:
            print(f'Error: Invalid input values: {ve}')
        except Exception as e: 
            print(f'Error: An unexpected error occurred: {e}')

    def sortProcessesByArrivalTimeAndId(self):
        self.processes.sort(key=lambda x: (x.arrivalTime, x.processId))

    def displayResults(self, processes):
        for p in processes: 
            print( f'P[{p.processId}] Start time: {p.startTime} | End time: {p.endTime} | Waiting time: {p.waitingTime}')
        print( 'Average waiting time: ', self.totalWaitingTime / self.numProcesses )

    def startSimulation(self):
        if self.algorithmId == 0:
            self.fcfs()
        elif self.algorithmId == 1:
            self.sjf()
        elif self.algorithmId == 2:
            self.srtf()
        elif self.algorithmId == 3:
            self.rr()

    def fcfs(self):
        self.sortProcessesByArrivalTimeAndId()
        
        for p in self.processes:
            # Process details
            self.currentTime = max(self.currentTime, p.arrivalTime)   # ensure it's at least as late as the arrival time
            p.startTime = self.currentTime                  # process started at current time
            p.endTime = p.startTime + p.burstTime           # how long it took the process to run 
            p.burstTime = 0                                 # completes its entire burst time without interruption
            p.waitingTime = p.startTime - p.arrivalTime     # the time elapsed between the process's arrival and start.

            # Time calculation
            self.currentTime = p.endTime                    # update the current time
            self.totalWaitingTime += p.waitingTime          # accumulate the waiting times of all the processes.
            
            self.executedProcesses.append(p)

        self.displayResults(self.executedProcesses)

    def sjf(self):
        self.sortProcessesByArrivalTimeAndId()

        while self.processes:
            # Creates a queue of processes that fills up when a process has arrived
            queue = []
            for process in self.processes:
                if process.arrivalTime <= self.currentTime:
                    queue.append(process)

            # When there is a process in the queue
            if queue:
                # Selects the process with the shortest burst time from the processes queue
                nextProcess = min(queue, key=lambda x: x.burstTime)
                self.processes.remove(nextProcess)

                nextProcess.startTime = self.currentTime
                nextProcess.endTime = self.currentTime + nextProcess.burstTime
                nextProcess.waitingTime = self.currentTime - nextProcess.arrivalTime
                self.totalWaitingTime += nextProcess.waitingTime
                self.currentTime = nextProcess.endTime

                self.executedProcesses.append(nextProcess)

        self.displayResults(self.executedProcesses)
    
    def srtf(self):
        self.sortProcessesByArrivalTimeAndId()
        waitingTimeIndex = []
        p = None

        while self.processes or self.queue:

            # No process in the queue, update current time
            if not self.queue:
                self.currentTime = self.processes[0].arrivalTime if self.processes else self.currentTime

            # Execute the process with the shortest remaining itme 
            else: 
                p = min(self.queue, key=lambda x: (x.burstTime, x.processId))
                self.queue.remove(p)

                # Calculate initial waiting time
                if p.processId not in waitingTimeIndex:
                    p.waitingTime = self.currentTime - p.arrivalTime                
                    waitingTimeIndex.append(p.processId)

                # Ensure that the currentTime is at least as late as the arrival time of the current process
                self.currentTime = max(self.currentTime, p.arrivalTime)

                # Execute the process with its remaining burst time or until the next process arrives
                if self.processes:
                    isPreEmptive = False

                    # Get all the processes that will arrive during the run time of current process
                    arrivingProcesses = [a for a in self.processes if a.arrivalTime <= self.currentTime + p.burstTime]

                    for a in arrivingProcesses: 
                        pNewBurstTime = p.burstTime - (a.arrivalTime - self.currentTime)
                        if a.burstTime < pNewBurstTime:
                            isPreEmptive = True
                            runTime = a.arrivalTime - self.currentTime

                    if isPreEmptive == False:
                        runTime = p.burstTime
                else:
                    runTime = p.burstTime

                p.startTime = self.currentTime 
                p.endTime = p.startTime + runTime 
                p.burstTime -= runTime 
                self.currentTime = p.endTime 

                # Add to executed processes
                executedProcess = Process() 
                executedProcess.copyProcess(p)
                self.executedProcesses.append(executedProcess)

            # Add arrived processes to the queue
            while self.processes and self.processes[0].arrivalTime <= self.currentTime:
                temp = self.processes.pop(0)
                self.queue.append(temp)

            # Calculate waiting time of processes in queue
            if p is not None and p.processId in waitingTimeIndex:
                for q in self.queue:
                    q.waitingTime += runTime

            # Add process back to queue if it did not finish
            if p is not None and p.burstTime > 0: 
                self.queue.append(p)

        # Calculate total waiting time
        tempProcesses = [e for e in self.executedProcesses]
        tempProcesses.sort(key=lambda x: (x.processId, x.waitingTime), reverse=True)
        uniqueProcesses = []
        seenIds = set()

        # Find the final snapshot of each process to calculate average waiting time
        for t in tempProcesses: 
            if t.processId not in seenIds:
                uniqueProcesses.append(t)
                seenIds.add(t.processId)

        self.totalWaitingTime = 0
        for u in uniqueProcesses:
            self.totalWaitingTime += u.waitingTime 

        self.displayResults(self.executedProcesses)

    def rr(self):
        # Sort processes by arrival time and process id
        self.processes.sort(key=lambda x: (x.arrivalTime, x.processId))

        # Keep track of time
        currentTime = 0

        # Stores final result here (sorted by which process ends first)
        executedProcesses = []
        waitingTimeIndex = []

        # Create the queue and initialize it
        queue = []
        while self.processes and self.processes[0].arrivalTime <= currentTime:
            temp = self.processes.pop(0)
            queue.append(temp) 

        # Loop until self.process and queue is empty
        while self.processes or queue:

            # Run the process at the head of the queue 
            p = queue.pop(0)

            # Calculate initial waiting time 
            if p.processId not in waitingTimeIndex:
                p.waitingTime = currentTime - p.arrivalTime                
                waitingTimeIndex.append(p.processId)

            # Ensure that the currentTime is at least as late as the arrival time of the current process
            currentTime = max(currentTime, p.arrivalTime)

            # Execute the process for the time quantum or its remaining burst time, whichever is smaller
            runTime = min(self.timeQuantum, p.burstTime)

            p.startTime = currentTime 
            p.endTime = p.startTime + runTime 
            p.burstTime -= runTime 
            currentTime = p.endTime 

            # Add processes that just arrived to the queue 
            while self.processes and self.processes[0].arrivalTime <= currentTime:
                arrivedProcess = self.processes.pop(0)
                queue.append(arrivedProcess) 

            # Calculate waiting time of processes in queue
            if p.processId in waitingTimeIndex:
                for q in queue:
                    q.waitingTime += runTime
                
            # If process has remaining burst time, add to the end of queue 
            if p.burstTime > 0:
                queue.append(p) 

            # Add to executed processes
            executedProcess = Process() 
            executedProcess.copyProcess(p)
            executedProcesses.append(executedProcess)

        for p in executedProcesses:
            print(f'P[{p.processId}] Start time: {p.startTime} | End time: {p.endTime} | Waiting time: {p.waitingTime}')

        # Sort executed processes by processId and waitingTime
        executedProcesses.sort(key=lambda x: (x.processId, x.waitingTime), reverse=True)
        uniqueProcesses = []
        seenIds = set()

        # Find the final snapshot of each process to calculate average waiting time
        for e in executedProcesses: 
            if e.processId not in seenIds:
                uniqueProcesses.append(e)
                seenIds.add(e.processId)

        totalWaitingTime = 0
        for u in uniqueProcesses:
            totalWaitingTime += u.waitingTime 

        averageWaitingTime = totalWaitingTime / self.numProcesses
        print('Average waiting time: ', averageWaitingTime)
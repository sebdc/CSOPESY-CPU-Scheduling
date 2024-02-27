from typing import List
from .process import Process

class CPUScheduler:
    def __init__(self):
        self.algorithmId = None
        self.numProcesses = None
        self.timeQuantum = None 
        self.completionTime = None
        self.processes = []

    """
        ` Reads input from a file specified by 'fileName' using the InputHandler class. It then
        sets 'algorithmId', 'numProcesses', 'timeQuantum', and 'processes' based on the file data.
        If the file is not found or inputs are invalid, it prints an error message.
    """
    def readInputFile(self, fileName: str):
        from .input_handler import InputHandler

        try: 
            x, y, z, completionTime, processes = InputHandler.readProcessesFromFile(fileName)
            print("Algorithm ID:", x)
            print("Num Processes:", y)
            print("Time Quantum:", z)
            print("Completion Time:", completionTime)
            print("Processes:", processes)

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

    def startSimulation(self):
        if self.algorithmId == 0:
            self.fcfs()
            pass 
        elif self.algorithmId == 1:
            # SJF
            pass
        elif self.algorithmId == 2:
            # SRTF
            pass
        elif self.algorithmId == 3:
            # RR
            pass

    '''
        - Since this is FCFS, sort process by arrivalTime
        - If the arrival time is the same, then use the one with the smaller processId
            a. Loop from currentTime (0) to completionTime (sum of all burst times)
            b. Since processes are sorted, just loop through it instead
        - Keep track of current time
        - Wait time = current time - arrival time
    '''
    def fcfs(self):
        # Sort process by arrival time and process id
        self.processes.sort(key=lambda x: (x.arrivalTime, x.processId))

        currentTime = 0
        totalWaitingTime = 0
        for index, process in enumerate(self.processes):
            currentTime = max(currentTime, process.arrivalTime)
            process.startTime = currentTime
            process.endTime = process.startTime + process.burstTime
            process.waitingTime = process.startTime - process.arrivalTime
            currentTime = process.endTime

            totalWaitingTime += process.waitingTime

            print( f'P[{index}] Start time: {process.startTime} | End time: {process.endTime} | Waiting time: {process.waitingTime}')

        averageWaitingTime = totalWaitingTime / len(self.processes)
        print( 'Average waiting time: ', averageWaitingTime )
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
        elif self.algorithmId == 1:
            self.sjf()
        elif self.algorithmId == 2:
            self.srtf()
        elif self.algorithmId == 3:
            self.rr()

    '''
        - Since this is FCFS, sort process by arrivalTime
        - If the arrival time is the same, then use the one with the smaller processId
            a. Loop from currentTime (0) to completionTime (sum of all burst times)
            b. Since processes are sorted, just loop through it instead
    '''
    def fcfs(self):
        # Sort process by arrival time and process id
        self.processes.sort(key=lambda x: (x.arrivalTime, x.processId))

        # Keep track of time
        currentTime = 0
        totalWaitingTime = 0

        for index, p in enumerate(self.processes):

            # Ensure that the currentTime is at least as late as the arrival time of the current process
            currentTime = max(currentTime, p.arrivalTime)

            # Set the start time of the current process to the current time.
            # If the current time is later than the arrival time, this means the process has to wait.
            # Otherwise, it starts immediately upon arrival.
            p.startTime = currentTime

            # Determine the end time of the current process by adding its burst time to its start time.
            # This represents when the process completes its execution.
            p.endTime = p.startTime + p.burstTime

            # Calculate the waiting time of the current process.
            # This is the duration the process spends waiting in the queue before it starts executing.
            # It is computed as the difference between the start time and the arrival time.
            p.waitingTime = p.startTime - p.arrivalTime

            # Update the current time to the end time of the current process.
            # This ensures that the next process starts after the current process finishes.
            currentTime = p.endTime

            # Accumulate the waiting times of all processes.
            totalWaitingTime += p.waitingTime

            print( f'P[{index}] Start time: {p.startTime} | End time: {p.endTime} | Waiting time: {p.waitingTime}')

        averageWaitingTime = totalWaitingTime / len(self.processes)
        print( 'Average waiting time: ', averageWaitingTime )

    def sjf(self):
        print( 'Not yet implemented' )
    
    def srtf(self):
        print( 'Not yet implemented' )

    def rr(self):
        print( 'Not yet implemented' )
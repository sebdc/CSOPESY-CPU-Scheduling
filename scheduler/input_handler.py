from typing import List, Tuple
from .process import Process


"""
    ` Reads and process data from '{fileName}'.txt located in the input folder. It extracts 
    the configuration data 'x', 'y', and 'z' from the text file's first line and validates it. 
    Then, it iterates through subsequent lines to create Process objects and appends them to a 
    list. 
    
    If successful, it returns the configuration data and the list of Process objects. 
    Otherwise, it handles various exceptions and returns 'None'. 
"""
class InputHandler:

    @staticmethod
    def readProcessesFromFile(fileName: str) -> Tuple[int, int, int, int, List[Process]]:
        fileDirectory = './input'
        filePath = f'{fileDirectory}/{fileName}'
        processes = []
        completionTime = 0

        try: 
            with open(filePath, 'r') as file:
                # Read the first line to get x, y, z
                x, y, z = map(int, file.readline().split())
  
                # Check if inputs are valid
                isAlgorithmIdValid = x >= 0 and x <= 3 
                isNumProcessesValid = y >= 3 and y <= 100
                isTimeQuantumValid = z >= 1 and z <= 100

                # @TO-DO: Error codes to produce dynamic error messages
                if not isAlgorithmIdValid and isNumProcessesValid and isTimeQuantumValid:
                    return None

                # Normalize time quantum values
                if x != 3:
                    z = 1  

                # Read subsequent lines to create the processes and to compute for completion time
                for line in file:
                    processId, arrivalTime, burstTime = map(int, line.split())
                    process = Process(processId, arrivalTime, burstTime)
                    processes.append(process)
                    completionTime += burstTime     

                # @TO-DO: While creating processes, ensure that the processId is unique
                # Otherwise, return an error

        except FileNotFoundError:
            raise FileNotFoundError

        except ValueError:
            raise ValueError

        except Exception: 
            raise Exception

        return x, y, z, completionTime, processes
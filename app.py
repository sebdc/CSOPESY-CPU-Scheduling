from scheduler.scheduler import CPUScheduler
from scheduler.process import Process

def main():

    fileInputName = 'srtf3.txt'
    scheduler = CPUScheduler()
    scheduler.readInputFile(fileInputName)
    scheduler.startSimulation()

if __name__ == "__main__":
    main()  
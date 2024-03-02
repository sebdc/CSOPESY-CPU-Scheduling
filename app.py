from scheduler.scheduler import CPUScheduler
from scheduler.scheduler_new import CPUScheduler2

def main():

    fileInputName = 'srtf4.txt'
    scheduler = CPUScheduler()
    # scheduler = CPUScheduler2()
    scheduler.readInputFile(fileInputName)
    scheduler.startSimulation()

if __name__ == "__main__":
    main()  
from scheduler.scheduler import CPUScheduler

def main():

    fileInputName = 'srtf5.txt'
    scheduler = CPUScheduler()
    scheduler.readInputFile(fileInputName)
    scheduler.startSimulation()

if __name__ == "__main__":
    main()  
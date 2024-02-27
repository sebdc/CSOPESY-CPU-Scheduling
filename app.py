# How would the application function?
''' The program reads the following from standard input:

 - The first line contains three integers separated by space, 𝑋 𝑌 𝑍.
    - 𝑋 denotes the CPU scheduling algorithm.
    - 𝑌 denotes the number of processes where 3 ≤𝑌 ≤100 
    - 𝑍 denotes a time quantum value (applicable for Round-Robin algorithm only), where 1 ≤ 𝑍 ≤ 100. 
    
 - If the CPU scheduling algorithm indicated by the value of 𝑋 is not the Round-Robin algorithm, 
 this value must be set to 1 but ignored.

 - There will be 𝑌 lines of space-separated integers 𝐴 𝐵 𝐶 where 𝐴 is the process ID, 𝐵 is the arrival 
 time, and 𝐶 is the burst time.
'''

from filehandler import FileHandler

file_name = 'input.txt'
file_handler = FileHandler(file_name)
parsed_integers = FileHandler.read_first_line()
if parsed_integers:
    print( 'Parsed integers: ', parsed_integers )
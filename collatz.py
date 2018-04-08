import os

#Performs the collatz sequence recursively
#Returns the cycle length of the collatz sequence
def collatz_len(n, count):
    count+=1
    if n <= 1:
        return count
    if n%2 == 0: #Even
        return collatz_len(n/2, count)
    elif n%2 == 1: #Odd
        return collatz_len(n*3+1, count)

#Returns the max cycle length thru i and j
def max_cycle_len(i, j):
    max_len = 0
    for z in range(i,j):
        cur_len = collatz_len(z,0)
        if cur_len > max_len:
            max_len = cur_len
    return max_len

#Reads in input files and writes output accordingly
def read_write(inpath, outpath):
    #Make sure we're in the correct working directory
    script_dir = os.path.dirname(__file__)
    read = open(os.path.join(script_dir,inpath))
    write = open(os.path.join(script_dir,outpath), 'w')

    line = read.readline()

    while line:
        arr = line.split()
        max_len = max_cycle_len(int(arr[0]), int(arr[1]))
        write.write(arr[0]+" "+arr[1]+" "+str(max_len)+"\n")

        line = read.readline()

    read.close()
    write.close()

read_write("input.txt","output.txt")

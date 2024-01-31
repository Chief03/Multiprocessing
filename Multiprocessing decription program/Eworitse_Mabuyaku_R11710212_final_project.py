import argparse
import copy
import time
import os
from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import Lock
from multiprocessing import Value
from multiprocessing import Array
from multiprocessing import Manager
from multiprocessing import Queue
from multiprocessing.shared_memory import ShareableList


#directly from the teachers hand 
def decryptLetter(letter, rotationValue):
  rotationString  = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ "
  currentPosition = rotationString.find(letter)

  return rotationString[(currentPosition + rotationValue) % 95]

def validate_seed(str):
    valid_list = ['a','b','c']
    for c in str:
        if c not in valid_list:
            return False
    return True


def get_command_line_arguments():
   
    # code for accepting command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', "--input",type=str, help ="please enter input file path", required=True)
    parser.add_argument("-s","--seed", type=str, help ="please enter seed", required=True)
    parser.add_argument("-p","--process", type=int,help="please enter the number of processes", required=True)
    parser.add_argument("-o","--output",type=str,help = "please enter output file path", required=True)

    args = parser.parse_args()

    # get command lline arguments from the parses
    file_path = args.input
    seed = args.seed
    output = args.output
    process_limit = args.process

    #check for argument errors
    if os.path.exists(file_path) and os.path.isfile(file_path) == False:
        print("Please enter a vaild file path for the input file.")
        quit()
    if os.path.exists(output) and os.path.isfile(output) == False:
        print("Please enter a vaild file path for the output file.")
        quit()
    if validate_seed(seed) == False:
        print("The seed string may only consist of 1 to many lowercase letters a, b, and c")
        quit()
    if process_limit <= 0:
        print("The processes limit must be greater than 1")
        quit()
    return [file_path,seed,output,process_limit]



def get_string_from_file(file_path):
    string = ""
    # open input file
    input_file = open(file_path,"r")
    # read the string from the file
    for data in input_file:
        string += data
    # close input file
    input_file.close()
    return string



def trim_input_string(string):
    # remove leading and trailing whitespaces
    string = string.strip()
    # create 2D array
    return string
    
   

def populate_matrix(matrix,seed):
    seed_size = len(seed)
    seed_index = 0
    col = 0
    row = 0
    while row < size:
        col = 0
        while col < size:
            char = seed[seed_index]
            matrix[row][col] = get_cell_value(char)
            seed_index += 1
            col += 1
            if seed_index >= seed_size:
                seed_index = 0
        row += 1

def init_worker(data):
    global matrix
    matrix = data

    
def cell_calculation(row,col,matrix_cpy,matrix):
    neigboring_cells_total = get_sum_of_neighbouring_cells(row,col,matrix_cpy)
    return  transform_cell_stage_1_3(matrix[row][col],neigboring_cells_total)


# def cell_calculation(data):
#     row = data[0]
#     col = data[1]
#     matrix_cpy = data[2]
#     matrix = data[3]
#     size = data[4]
#     sub_list = matrix[row]
#     neigboring_cells_total = get_sum_of_neighbouring_cells(row,col,matrix_cpy,size)
#     sub_list[col] =  transform_cell_stage_1_3(sub_list[col],neigboring_cells_total)
#     matrix[row] = sub_list


    
    
def sum_column(col, matrix,size):
    row = 0
    total = 0
    while row < size:
        total += matrix[row][col]
        row += 1
    return total

def get_cell_value(char):
    if char == 'a':
        return 0
    elif char == 'b':
        return 1
    else:
        return 2
    
# get the sum of the neighbouring cells
def get_sum_of_neighbouring_cells(row,col,matrix):
    total = 0
    size = len(matrix)
    #if there is a row above the current cell
    if col-1 >= 0:
        total += matrix[row][col-1]
    if col+1 < size:
        total += matrix[row][col+1]
    if row-1 >= 0:
        total += matrix[row-1][col]
        #if there is column after the current cell
        if col+1 < size:
            total += matrix[row-1][col+1]
        if col-1 >= 0:
            total += matrix[row-1][col-1]     
    if row+1 < size:
        total += matrix[row+1][col]
        if col+1 < size:
            total += matrix[row+1][col+1]
        if col-1 >= 0:
            total += matrix[row+1][col-1]
    
    return total

# check if a number is even
def check_if_even(value):
    return value in {0,2,4,6,8,10,12,14,16}

# check if a number is odd
#def check_if_odd(value):
 #   if value % 2 == 0:
  #      return False
   # else: return True

# check if a number is a prime
def check_if_prime(value):
    return value in {2, 3, 5, 7, 11, 13, 17}

def transform_cell_stage_1_3(char, value):
    if char == 0:
        if check_if_prime(value):
            return 0
        elif check_if_even(value):
            return 1
        else:
            return 2
    elif char ==  1:
        if check_if_prime(value):
            return 1
        elif check_if_even(value):
            return 2
        else:
            return 0
    else:
        if check_if_prime(value):
            return 2
        elif check_if_even(value):
            return 0
        else:
            return 1

def transform_row(matrix,matrix_cpy, row):
    return[
        cell_calculation(
            row,col,matrix_cpy,matrix
        )
        for col, cell
        in enumerate(matrix[row])
    ]


if __name__ == "__main__":
    print("Project :: R11710212")
    start_timer = time.perf_counter()
    cmd_args = get_command_line_arguments()
    file_path = cmd_args[0]
    seed = cmd_args[1]
    output = cmd_args[2]
    process_limit = cmd_args[3]
    string = get_string_from_file(file_path)
    string = trim_input_string(string)
    size = len(string)
    matrix = [[0 for x in range(size)] for y in range(size)]
    populate_matrix(matrix,seed)

    matrix_cpy = copy.deepcopy(matrix)
    iteration = 0
    

    pool = Pool(process_limit)
    with pool:
        while iteration < 100:    
            matrix = list(pool.starmap(transform_row,[(matrix,matrix_cpy,row) for row in range(size)]))
            matrix_cpy = None
            matrix_cpy = copy.deepcopy(matrix)
            iteration += 1
            row = 0
    
    col = 0
    final_string = ""
    while col < size:
        column_sum = sum_column(col,matrix,size)
        final_string +=  decryptLetter(string[col],column_sum)
        col += 1
        
    output_file = open(output,"w")
    output_file.write(final_string)
    output_file.close()
    print (final_string)
    finish_time = time.perf_counter()
    print(f'Finsished in {round(finish_time - start_timer,2)} second(s)')







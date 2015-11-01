__author__ = 'liscju <piotr.listkiewicz@gmail.com>'

# Table size is comm.Get_size() x comm.Get_size(),
# Conductor size is first argument to program, conductor
#   is placed at the middle of table
# 
# For example when com.Get_size() =5, conductor_size=1 table 
# would look like this(o - border, * - custom cell, x - conductor)
# o - o - o
# o - x - o
# o - o - o
# For example when com.Get_size() =5, conductor_size=1 table
# would look like this
# o - o - o - o - o
# o - * - * - * - o
# o - * - x - * - o
# o - * - * - * - o
# o - o - o - o - o

import sys
from mpi4py import MPI

from helpers import GridInfo

def usage():
    print "You should invoke this with arguments: " \
        "conductor_x_pos, conductor_y_pos, conductor_size, conductor_value"
    exit(-1)
    
def get_conductor_x_pos():
    if len(sys.argv) < 2:
        print "You have to pass conductor x pos as first argument"
        usage()
    else:
        return int(sys.argv[1])
    
def get_conductor_y_pos():
    if len(sys.argv) < 3:
        print "You have to pass conductor x pos as second argument"
        usage()
    else:
        return int(sys.argv[2])

def get_conductor_size():
    if len(sys.argv) < 4:
        print "You have to pass conductor size as third argument"
        usage()
    else:
        return int(sys.argv[3])

def get_conductor_value():
    if len(sys.argv) < 5:
        print "You have to pass conductor value as fitth argument"
        usage()
    else:
        return int(sys.argv[4])
    
class RowParrallelCalculator:
    def __init__(self, rownum, grid_info):
        self.rownum = rownum
        self.grid_info = grid_info

    def run(self):
        #print "Executed parralel executor for rownum=", self.rownum
        pass

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    conductor_x_pos = get_conductor_x_pos()
    conductor_y_pos = get_conductor_y_pos()
    conductor_size = get_conductor_size()
    conductor_value = get_conductor_value()
    
    gridInfo = GridInfo(size, conductor_x_pos, conductor_y_pos, conductor_size, conductor_value)
    rowParallelCalculator = RowParrallelCalculator(rank, gridInfo)
    rowParallelCalculator.run()

if __name__ == "__main__":
    main()
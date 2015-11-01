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

def get_conductor_size():
    if len(sys.argv) == 1:
        print "You have to pass conductor size as first argument"
        exit(-1)
    else:
        return sys.argv[1]

def get_conductor_value():
    if len(sys.argv) < 3:
        print "You have to pass conductor value as second argument"
        exit(-1)
    else:
        return sys.argv[2]

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    conductor_size = get_conductor_size()
    conductor_value = get_conductor_value()
    print "Hello world from rank=", rank, " while size=", size, \
        "and conductor_size=", conductor_size, " and conductor_value=", \
        conductor_value

if __name__ == "__main__":
    main()
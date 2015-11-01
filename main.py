__author__ = 'liscju <piotr.listkiewicz@gmail.com>'

import sys
from mpi4py import MPI


def get_conductor_size():
    if len(sys.argv) == 1:
        print "You have to pass conductor size as first argument"
        exit(-1)
    else:
        return sys.argv[1]

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    conductor_size = get_conductor_size()
    print "Hello world from rank=", rank, " while size=", size, \
        "and conductor_size=", conductor_size

if __name__ == "__main__":
    main()
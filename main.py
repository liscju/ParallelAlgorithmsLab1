__author__ = 'liscju <piotr.listkiewicz@gmail.com>'

from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print "Hello world from rank=", rank, " while size=", size

if __name__ == "__main__":
    main()
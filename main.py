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
        return float(sys.argv[4])
    
class RowParrallelCalculator:
    def __init__(self, comm, rownum, grid_info):
        self.comm = comm
        self.rownum = rownum
        self.grid_info = grid_info
        self.initialize_row_values()

    def initialize_row_values(self):
        self.row_values = [None] * self.grid_info.get_size()
        y = self.rownum
        for x in range(0, self.grid_info.get_size()):
            if self.grid_info.is_screen_point(x, y):
                self.row_values[x] = self.grid_info.get_screen_value()
            elif self.grid_info.is_conductor_point(x, y):
                self.row_values[x] = self.grid_info.get_conductor_value()
            else:
                self.row_values[x] = self.grid_info.get_default_value()

    def run(self):
        while True:
            self.__send_row_values_to_neighbours()
            row_values_from_above, row_values_from_below = self.__recv_row_values_from_neighbours()
            print "Row(", self.rownum, ") received row from above", row_values_from_above, "and from below", row_values_from_below
            stop_condition = self.__calculate_new_row_values(row_values_from_above, row_values_from_below)
            print "Row:", self.rownum, "=", self.row_values
            if stop_condition:
                break

    def __send_row_values_to_neighbours(self):
        if self.rownum > 0:
            self.comm.send(self.row_values, dest=self.rownum - 1)

        if self.rownum < self.grid_info.get_size() - 1:
            self.comm.send(self.row_values, dest=self.rownum + 1)

    def __recv_row_values_from_neighbours(self):
        if self.rownum > 0:
            row_values_from_above = self.comm.recv(source=self.rownum - 1)
        else:
            row_values_from_above = None

        if self.rownum < self.grid_info.get_size() - 1:
            row_values_from_below = self.comm.recv(source=self.rownum + 1)
        else:
            row_values_from_below = None

        return row_values_from_above, row_values_from_below

    def __calculate_new_row_values(self, row_values_from_above, row_values_from_below):
        y = self.rownum
        for x in range(0, self.grid_info.get_size()):
            if self.grid_info.is_screen_point(x, y) or \
                    self.grid_info.is_conductor_point(x, y):
                pass
            else:
                self.row_values[x] = (self.row_values[x - 1] + self.row_values[x + 1] +
                                      row_values_from_above[x] + row_values_from_below[x]) / 4
        return True


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    conductor_x_pos = get_conductor_x_pos()
    conductor_y_pos = get_conductor_y_pos()
    conductor_size = get_conductor_size()
    conductor_value = get_conductor_value()

    gridInfo = GridInfo(size, conductor_x_pos, conductor_y_pos, conductor_size, conductor_value)
    rowParallelCalculator = RowParrallelCalculator(comm, rank, gridInfo)
    rowParallelCalculator.run()

if __name__ == "__main__":
    main()
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

def usage():
    print "You should invoke this with arguments: " \
        "conductor_x_pos, conductor_y_pos, conductor_size, conductor_value, number_of_iterations, [sequential|parallel]"
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

def get_number_of_iteration():
    if len(sys.argv) < 6:
        print "You have to pass number of iteration as sixth argument"
        usage()
    else:
        return int(sys.argv[5])
    
def get_program_type():
    if len(sys.argv) < 7:
        print "You have to pass program type as last argument"
        usage()
    else:
        return sys.argv[-1]

class GridInfo:
    def __init__(self, size, conductor_x_pos, conductor_y_pos, conductor_size, conductor_value,
                 number_of_iteration):
        self.size = size
        self.conductor_x_pos = conductor_x_pos
        self.conductor_y_pos = conductor_y_pos
        self.conductor_size = conductor_size
        self.conductor_value = conductor_value
        self.number_of_iteration = number_of_iteration

    def get_size(self):
        return self.size

    def get_conductor_value(self):
        return self.conductor_value

    def get_number_of_iteration(self):
        return self.number_of_iteration

    def get_screen_value(self):
        return 0.

    def get_default_value(self):
        # It could be any value, i chose 5 just to be different than 0 :P
        return 5.

    def is_screen_point(self, x, y):
        return y == 0 or y == self.size - 1 or \
               x == 0 or x == self.size - 1

    def is_conductor_point(self, x, y):
        return self.conductor_x_pos <= x < self.conductor_x_pos + self.conductor_size and \
            self.conductor_y_pos <= y < self.conductor_y_pos + self.conductor_size

class RowParrallelCalculator:
    def __init__(self, comm, rownum, grid_info):
        self.comm = comm
        self.rownum = rownum
        self.grid_info = grid_info
        self.__initialize_row_values()

    def run(self):
        for i in range(0, self.grid_info.get_number_of_iteration()):
            self.__send_row_values_to_neighbours()
            row_values_from_above, row_values_from_below = self.__recv_row_values_from_neighbours()
            self.__calculate_new_row_values(row_values_from_above, row_values_from_below)

        self.__finalize_calculation()

    def __initialize_row_values(self):
        self.row_values = [None] * self.grid_info.get_size()
        y = self.rownum
        for x in range(0, self.grid_info.get_size()):
            if self.grid_info.is_screen_point(x, y):
                self.row_values[x] = self.grid_info.get_screen_value()
            elif self.grid_info.is_conductor_point(x, y):
                self.row_values[x] = self.grid_info.get_conductor_value()
            else:
                self.row_values[x] = self.grid_info.get_default_value()

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

    def __finalize_calculation(self):
        if self.rownum == 0:
            all_values = [self.row_values]
            for neighbour in range(1, self.grid_info.get_size()):
                all_values.append(self.comm.recv(source=neighbour))
            print all_values
        else:
            self.comm.send(self.row_values, dest=0)


def main():
    if get_program_type() == "parallel":
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        conductor_x_pos = get_conductor_x_pos()
        conductor_y_pos = get_conductor_y_pos()
        conductor_size = get_conductor_size()
        conductor_value = get_conductor_value()
        number_of_iteration = get_number_of_iteration()

        gridInfo = GridInfo(size, conductor_x_pos, conductor_y_pos, conductor_size, conductor_value,
                            number_of_iteration)
        rowParallelCalculator = RowParrallelCalculator(comm, rank, gridInfo)
        rowParallelCalculator.run()

    elif get_program_type() == "sequential":
        size = sys.argv.pop(1)
        conductor_x_pos = get_conductor_x_pos()
        conductor_y_pos = get_conductor_y_pos()
        conductor_size = get_conductor_size()
        conductor_value = get_conductor_value()
        number_of_iteration = get_number_of_iteration()

        print "Size=", size, "conductor_x=", conductor_x_pos, "conductor_y=", conductor_y_pos, \
            "conductor_size=", conductor_size, "conductor_value=", conductor_value, "number_of_iter=", \
            number_of_iteration

        gridInfo = GridInfo(size, conductor_x_pos, conductor_y_pos, conductor_size, conductor_value,
                            number_of_iteration)

    else:
        print "Unrecognized program type in seventh argument:", get_program_type()
        usage()

if __name__ == "__main__":
    main()
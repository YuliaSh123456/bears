import random
import sys
from random import randint
import cell
import bear
import constants

list_of_bears = []

out_file = open('bear_out.txt', 'w')


def create_bear(name, cell_row, cell_col):
    activity_level = random.random()
    smell = random.random()
    aggression = random.random()
    cowardice = random.random()
    life_count = constants.INITIAL_LIFE_LEVEL

    return bear.Bear(
        name,
        activity_level,
        smell,
        aggression,
        cowardice,
        life_count,
        cell_row,
        cell_col)


def draw_bears_data():
    for each_bear in range(len(list_of_bears)):
        list_of_bears[each_bear].print_bear_data()


class Field(object):

    def __init__(self):
        self.matrix = [[cell.Cell(i, j) for i in range(constants.MAX_ROW)] for j in range(constants.MAX_COL)]
        self.populate_field()

    def populate_field(self):
        honey_counter = constants.HONEY_AMOUNT

        if honey_counter > constants.MAX_ROW * constants.MAX_COL:
            print >> out_file, "Irrational amount of honey"
            raise RuntimeError("Irrational amount of honey")
            sys.exit()

        while honey_counter > 0:
            row = random.randint(0, constants.MAX_ROW - 1)
            col = random.randint(0, constants.MAX_COL - 1)

            if not self.get_cell_at_location(row, col).has_honey:
                self.set_honey(row, col)
                honey_counter = honey_counter - 1

        bear_counter = constants.BEARS_AMOUNT

        while bear_counter > 0:
            random_empty_cell = self.get_random_empty_cell()

            if random_empty_cell is None:
                print >> out_file, "Irrational correlation between field size and amount of bears"
                raise RuntimeError("Irrational correlation between field size and amount of bears")
                sys.exit()

            new_bear = create_bear(str(bear_counter), random_empty_cell.row, random_empty_cell.col)
            list_of_bears.append(new_bear)
            random_empty_cell.set_bear(new_bear)
            bear_counter -= 1

    def get_random_empty_cell(self):

        list_of_empty_cells = []

        for i in range(constants.MAX_ROW - 1):
            for j in range(constants.MAX_COL - 1):
                if self.matrix[i][j].is_empty():
                    list_of_empty_cells.append(self.matrix[i][j])

        return random.choice(list_of_empty_cells)

    def get_random_cell_with_no_bear(self):
        col = randint(0, constants.MAX_COL - 1)
        row = randint(0, constants.MAX_ROW - 1)

        while self.matrix[row][col].has_bear() is not None:
            col = randint(0, constants.MAX_COL - 1)
            row = randint(0, constants.MAX_ROW - 1)

        return self.matrix[row][col]

    def remove_bear(self, row, col):
        self.matrix[row][col].bear = None

    def set_bear(self, the_bear, row, col):
        self.matrix[row][col].set_bear(the_bear)

    def set_honey(self, row, col):
        self.matrix[row][col].set_honey()

    def remove_honey(self, row, col):
        self.matrix[row][col].remove_honey()

    def get_cell_at_location(self, row, col):
        return self.matrix[row][col]

    def get_bear_present_in_cell(self, row, col):
        return self.matrix[row][col].get_bear()

    def draw_field(self):
        str_col = ""
        for rows in range(constants.MAX_ROW):
            for cols in range(constants.MAX_COL):
                if self.matrix[rows][cols].has_honey:
                    honey = "H"
                else:
                    honey = " "

                some_bear = self.matrix[rows][cols].has_bear()

                if some_bear is not None:
                    bear_name = "B" + some_bear.name
                else:
                    bear_name = " "

                str_col = str_col + '{} {} {} {} ||'.format(bear_name, rows, cols, honey)
            print >> out_file, str_col
            str_col = ""

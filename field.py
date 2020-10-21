import random
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


def populate_field(field_instance):

    honey_counter = constants.HONEY_AMOUNT

    while honey_counter > 0:
        row = random.randint(0, constants.MAX_ROW - 1)
        col = random.randint(0, constants.MAX_COL - 1)

        if not field_instance.get_cell_at_location(row, col).has_honey:
            field_instance.set_honey(row, col)
            honey_counter = honey_counter - 1

    bear_counter = constants.BEARS_AMOUNT

    while bear_counter > 0:
        random_empty_cell = field_instance.get_random_empty_cell()
        new_bear = create_bear(str(bear_counter), random_empty_cell.row, random_empty_cell.col)
        list_of_bears.append(new_bear)
        random_empty_cell.set_bear(new_bear)
        bear_counter -= 1


def draw_bears_data():
    for each_bear in range(len(list_of_bears)):
        list_of_bears[each_bear].print_bear_data()


class Field(object):

    def __init__(self):

        self.matrix = []

        self.matrix = [[cell.Cell(i, j) for i in range(constants.MAX_ROW)] for j in range(constants.MAX_COL)]
        populate_field(self)

    def get_random_empty_cell(self):
        col = randint(0, constants.MAX_COL-1)
        row = randint(0, constants.MAX_ROW-1)

        while not self.matrix[row][col].is_empty():
            col = randint(0, constants.MAX_COL-1)
            row = randint(0, constants.MAX_ROW-1)

        return self.matrix[row][col]

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



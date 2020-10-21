import random
from random import randint
import cell
import bear
import constants
import field
from field import out_file

def is_one_bear_left():
    live_bears = 0
    for i in range(constants.BEARS_AMOUNT):
        if field.list_of_bears[i].life_count > 0:
            live_bears = live_bears + 1

    return live_bears == 1

def main_algorythm():
    my_world_field = field.Field()
    field.populate_field(my_world_field)

    whose_turn = 0
    my_world_field.draw_field()

    my_world_field.draw_bears_data()

    while not is_one_bear_left():
        if field.list_of_bears[whose_turn].life_count > 0:
            field.list_of_bears[whose_turn].move(my_world_field)

        if whose_turn >= constants.BEARS_AMOUNT - 1:
            whose_turn = 0
        else:
            whose_turn = whose_turn + 1

    print >> out_file, "FINISHED"

    my_world_field.draw_field()
    my_world_field.draw_bears_data()
    out_file.close()


def main():
    main_algorythm()


if __name__ == "__main__":
    main()

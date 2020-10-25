import random
import cell
import bear
import constants
import field
from field import out_file


def is_one_bear_left():
    live_bears = 0
    for single_bear in field.list_of_bears:
        if single_bear.life_count > 0:
            live_bears += 1

    return live_bears == 1


def main():
    my_world_field = field.Field()

    whose_turn = 0
    my_world_field.draw_field()

    field.draw_bears_data()

    while not is_one_bear_left():

        for the_bear in field.list_of_bears:
            if the_bear.life_count > 0:
                the_bear.move(my_world_field)


    print >> out_file, "FINISHED"

    my_world_field.draw_field()
    field.draw_bears_data()
    out_file.close()


if __name__ == "__main__":
    main()

import random
import cell
import bear
import constants
import field
from field import out_file


def is_amount_bear_left(amount):
    live_bears = 0
    for single_bear in field.list_of_bears:
        if single_bear.life_count > 0:
            live_bears += 1

    return live_bears == amount


def main():
    my_world_field = field.Field()

    whose_turn = 0
    my_world_field.draw_field()

    field.draw_bears_data()

    while not is_amount_bear_left(2):
        for the_bear in field.list_of_bears:
            if the_bear.life_count > 0:
                the_bear.move(my_world_field)

    # Two left - do reproduct
    list_of_live_beras = []
    for the_bear in field.list_of_bears:
        if the_bear.life_count > 0:
            list_of_live_beras.append(the_bear)

    list_of_live_beras[0].reproduct(list_of_live_beras[1], my_world_field)

    print >> out_file, "REPRODUCT"

    my_world_field.draw_field()
    field.draw_bears_data()

    while not is_amount_bear_left(1):
        for the_bear in field.list_of_bears:
            if the_bear.life_count > 0:
                the_bear.move(my_world_field)

    out_file.close()


if __name__ == "__main__":
    main()

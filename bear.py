import os
import sys
import argparse
import constants
import random
import field

from field import out_file


def generate_fighting_coef():
    return random.random()


def end_of_fight(field, winner, loser, winners_fighting_coef, losers_fighting_coef):
    winner.life_count += losers_fighting_coef
    loser.life_count -= winners_fighting_coef

    if loser.life_count <= 0:
        loser.die(field)
    else:
        loser.go_to_random_cell(field)


class Bear(object):

    def __init__(self, name, activity_level, smell, aggression, cowardice, life_count, cell_row, cell_col):

        self.life_count = life_count
        self.last_action = constants.REST
        self.last_direction = constants.MOVEMENT_RANDOM
        self.activity_level = activity_level
        self.smell = smell
        self.aggression = aggression
        self.cowardice = cowardice
        self.cell_row = cell_row
        self.cell_col = cell_col
        self.name = name
        self.reduced_activity_level = False

    def print_bear_data(self):
        print >> out_file, 'B{} life count {} last action {} location r {} c {}'.format(self.name, self.life_count, self.last_action, self.cell_row, self.cell_col)

    def create_value_for_feature(self, value_bear_one, value_bear_two):
        from_whom_to_inherit = random.randint(0,1)

        if  from_whom_to_inherit == 0:
            new_value = value_bear_one
        else:
            new_value = value_bear_two

        # Add mutation
        new_value += random.gauss(0, 1.0/10)
        return new_value


    def reproduct(self, another_bear, the_field):
        life_count = constants.INITIAL_LIFE_LEVEL

        activity_level = self.create_value_for_feature(self.activity_level, another_bear.activity_level)
        smell = self.create_value_for_feature(self.smell, another_bear.smell)
        aggression = self.create_value_for_feature(self.aggression, another_bear.aggression)
        cowardice = self.create_value_for_feature(self.cowardice, another_bear.cowardice)

        activity_level = random.random()
        smell = random.random()
        aggression = random.random()
        cowardice = random.random()
        life_count = constants.INITIAL_LIFE_LEVEL
        random_empty_cell = the_field.get_random_empty_cell()

        baby_bear = Bear(
            self.name.split("B")[0] + another_bear.name.split("B")[0],
            activity_level,
            smell,
            aggression,
            cowardice,
            life_count,
            random_empty_cell.row,
            random_empty_cell.col)

        field.list_of_bears.append(baby_bear)
        random_empty_cell.set_bear(baby_bear)

    def eat_honey(self, the_field):
        cell = the_field.get_cell_at_location(self.cell_row, self.cell_col)

        if not cell.has_honey:
            return

        do_eat = random.random()

        if do_eat <= self.smell:
            print >> out_file, 'Bear {} ate honey'.format(self.name)
            self.life_count += 1
            self.activity_level /= 3
            self.reduced_activity_level = True
            cell.remove_honey()

    def do_you_defeat(self):
        do_defeat = random.random()
        return do_defeat <= self.cowardice

    def set_cell(self, cell_row, cell_col):
        self.cell_row = cell_row
        self.cell_col = cell_col

    def go_to_random_cell(self, field):
        field.remove_bear(self.cell_row, self.cell_col)
        random_empty_cell = field.get_random_cell_with_no_bear()
        self.set_cell(random_empty_cell.row, random_empty_cell.col)
        field.set_bear(self, self.cell_row, self.cell_col)

    def die(self, field):
        print >> out_file, 'Bear B{} dies'.format(self.name)
        cell = field.get_cell_at_location(self.cell_row, self.cell_col)
        cell.remove_bear()

    def fight(self, another_bear, the_field):
        print >> out_file, "F I G H T"
        do_fight = random.random()
        if do_fight <= self.aggression:
            print >> out_file, "Fight according to aggression level"
            if self.do_you_defeat() and not another_bear.do_you_defeat():
                # I defeat
                self.life_count = self.life_count * 0.9
                another_bear.life_count += self.life_count * 0.1
                # I go to random cell
                self.go_to_random_cell(the_field)
                print >> out_file, 'B{} defeats, goes to r{} c{} '.format(self.name, self.cell_row, self.cell_col)
            else:
                # No one defeats - fight
                my_fighting_coef = generate_fighting_coef()
                his_fighting_coef = generate_fighting_coef()

                while my_fighting_coef == his_fighting_coef:
                    my_fighting_coef = generate_fighting_coef()
                    his_fighting_coef = generate_fighting_coef()

                # I win
                if my_fighting_coef > his_fighting_coef:
                    end_of_fight(the_field, self, another_bear, my_fighting_coef, his_fighting_coef)
                    print >> out_file, 'B{} wins '.format(self.name)
                # I loose
                if his_fighting_coef > my_fighting_coef:
                    end_of_fight(the_field, another_bear, self, his_fighting_coef, my_fighting_coef)
                    print >> out_file, 'B{} looses '.format(self.name)
        else:
            # Aggression level doesn't let fighting
            print >> out_file, "Agression not enough for fighting, go to random cell"
            self.go_to_random_cell(the_field)

        the_field.draw_field()
        field.draw_bears_data()

    def move(self, the_field):

        new_row = 0
        new_col = 0
        mov_log = ""
        do_move = random.random()

        if do_move > self.activity_level:
            print >> out_file, 'B{} rests'.format(self.name)
            self.last_action = constants.REST
            return

        if self.last_action == constants.REST:
            self.last_direction = random.randint(0, 3)

        self.last_action = constants.MOVE

        if self.last_direction == constants.MOVEMENT_UP:
            mov_log = mov_log + " UP "
            if self.cell_row == 0:
                new_row = constants.MAX_ROW - 1
            else:
                new_row = self.cell_row - 1
            new_col = self.cell_col

        if self.last_direction == constants.MOVEMENT_DOWN:
            mov_log = mov_log + " DOWN "
            if self.cell_row == constants.MAX_ROW - 1:
                new_row = 0
            else:
                new_row = self.cell_row + 1
            new_col = self.cell_col

        if self.last_direction == constants.MOVEMENT_LEFT:
            mov_log = mov_log + " LEFT "
            if self.cell_col == 0:
                new_col = constants.MAX_COL - 1
            else:
                new_col = self.cell_col - 1
            new_row = self.cell_row

        if self.last_direction == constants.MOVEMENT_RIGHT:
            mov_log = mov_log + " RIGHT "
            if self.cell_col == constants.MAX_COL - 1:
                new_col = 0
            else:
                new_col = self.cell_col + 1
            new_row = self.cell_row

        print >> out_file, 'B{} moves {} from r{} c{} to r{} c{}'.format(self.name, mov_log, self.cell_row, self.cell_col, new_row, new_col)

        another_bear = the_field.get_bear_present_in_cell(new_row, new_col)

        if another_bear is not None:
            print >> out_file, ' FIGHTS with B{} r{} c{} to '.format(another_bear.name, another_bear.cell_row, another_bear.cell_col)
            self.fight(another_bear, the_field)
        else:
            the_field.remove_bear(self.cell_row, self.cell_col)
            the_field.set_bear(self, new_row, new_col)
            self.set_cell(new_row, new_col)
            self.eat_honey(the_field)

        if self.reduced_activity_level:
            self.reduced_activity_level = False
            self.activity_level *= 3

        the_field.draw_field()
        field.draw_bears_data()

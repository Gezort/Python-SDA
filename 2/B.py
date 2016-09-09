#!/bin/env python
from random import choice as rand
from copy import deepcopy


class Ocean:
    '''Ocean(width=1, height=1, predators=(), victims=(), barriers=(),
    starvation_time=5, birth_time=5)

    Parameters
    ----------
    width : int, optional
        Width of the ocean.
    height : int, optional
        Height of the ocean.
    predators : list of pairs, optional
        An array containing initial predators distribution in the ocean.
    victims : list of pairs, optional
        An array containing initial victims distribution in the ocean.
        Shouldn't contain pairs mentioned in predators.
    barriers : list of pairs, optional
        An array containing initial barriers distribution in the ocean.
        Shouldn't contain pairs mentioned in predators or victims.
    starvation_time: int, optional
        The maximum time predator can live without eating.
    birth_time: int, optional
        The time after which new inhabitants are born.
    '''

    def __init__(
            self, width=1, height=1, predators=(), victims=(),
            barriers=(), starvation_time=5, birth_time=5):
        self.width = width
        self.height = height
        self._ocean = [[{'cell': 'free', 'time_alive': 1}
                        for j in range(width)] for i in range(height)]
        for x, y in predators:
            self._ocean[x][y]['cell'] = 'predator'
            self._ocean[x][y]['hunger'] = 0
        for x, y in victims:
            self._ocean[x][y]['cell'] = 'victim'
        for x, y in barriers:
            self._ocean[x][y]['cell'] = 'barrier'
        self.birth_time = birth_time
        self.starvation_time = starvation_time

    def print_ocean(self):
        '''Prints ocean map. P - predator, V - victim, B - barrier,
        . - empty field.
        '''
        for i in range(self.width + 5):
            print('=', end='')
        print()
        for line in self._ocean:
            for cell in line:
                if cell['cell'] == 'free':
                    print('.', end='')
                elif cell['cell'] == 'barrier':
                    print('B', end='')
                elif cell['cell'] == 'victim':
                    print('V', end='')
                else:
                    print('P', end='')
            print()

    def _get_random_neighbour(self, i, j, ocean, cell_type):
        di = [0, 0, self.height - 1, self.height - 1, self.height - 1, 1, 1, 1]
        dj = [1, self.width - 1, 0, 1, self.width - 1, 0, 1, self.width - 1]
        neighbours = []
        for k in range(8):
            new_i = (i + di[k]) % self.height
            new_j = (j + dj[k]) % self.width
            if ocean[new_i][new_j]['cell'] == cell_type:
                neighbours.append((new_i, new_j))
        if len(neighbours) > 0:
            return rand(neighbours)
        return None

    def _count_creatures(self):
        num_predators = 0
        num_victims = 0
        for i in range(self.height):
            for j in range(self.width):
                if self._ocean[i][j]['cell'] == 'victim':
                    num_victims += 1
                elif self._ocean[i][j]['cell'] == 'predator':
                    num_predators += 1
        return (num_victims, num_predators)

    def _move_creatures(self):
        new_ocean = [deepcopy(line) for line in self._ocean]
        for i in range(self.height):
            for j in range(self.width):
                cur = self._ocean[i][j]['cell']
                if cur == 'free' or cur == 'barrier':
                    pass
                elif cur == 'victim':
                    # Victim can only move to another cell
                    new_ocean[i][j]['time_alive'] += 1
                    new_cell = self._get_random_neighbour(
                        i, j, new_ocean, 'free')
                    if new_cell is None:
                        continue
                    new_ocean[new_cell[0]][
                            new_cell[1]] = deepcopy(new_ocean[i][j])
                    new_ocean[i][j]['cell'] = 'free'
                else:
                    # Predator will first try to eat victim and if fail
                    # will try to move somewhere
                    new_cell = self._get_random_neighbour(
                            i, j, new_ocean, 'victim')
                    if new_cell is None:
                        new_cell = self._get_random_neighbour(
                                i, j, new_ocean, 'free')
                        if new_cell is None:
                            new_ocean[i][j]['hunger'] += 1
                            new_ocean[i][j]['time_alive'] += 1
                            continue
                        new_ocean[new_cell[0]][new_cell[1]][
                                'hunger'] = new_ocean[i][j]['hunger'] + 1
                    else:
                        new_ocean[new_cell[0]][new_cell[1]]['hunger'] = 0
                        self._ocean[new_cell[0]][new_cell[1]]['cell'] = 'free'
                        # We do not need to process 'eaten' cell anymore
                    new_ocean[i][j]['cell'] = 'free'
                    new_ocean[new_cell[0]][new_cell[1]][
                            'time_alive'] = new_ocean[i][j]['time_alive'] + 1
                    new_ocean[new_cell[0]][new_cell[1]]['cell'] = 'predator'
        return new_ocean

    def _new_generation(self):
        new_ocean = [deepcopy(line) for line in self._ocean]
        for i in range(self.height):
            for j in range(self.width):
                if (self._ocean[i][j]['cell'] == 'victim' and self.
                        _ocean[i][j]['time_alive'] % self.birth_time == 0):
                    new_cell = self._get_random_neighbour(
                                i, j, new_ocean, 'free')
                    if new_cell is None:
                        continue
                    new_ocean[new_cell[0]][new_cell[1]] = {
                            'cell': 'victim', 'time_alive': 1}
                elif (self._ocean[i][j]['cell'] == 'predator' and self.
                        _ocean[i][j]['time_alive'] % self.birth_time == 0 and
                        self._ocean[i][j]['hunger'] <=
                        self.starvation_time // 3):
                    new_cell = self._get_random_neighbour(
                            i, j, new_ocean, 'free')
                    if new_cell is None:
                        continue
                    new_ocean[new_cell[0]][new_cell[1]] = {
                            'cell': 'predator', 'time_alive': 0, 'hunger': 0}
        return new_ocean

    def _degenerate_creatures(self):
        for i in range(self.height):
            for j in range(self.width):
                # If predator hasn't eaten for starvation_time
                # iterations he will die.
                if (self._ocean[i][j]['cell'] == 'predator' and
                        self._ocean[i][j]['hunger'] >= self.starvation_time):
                    self._ocean[i][j]['cell'] = 'free'
        return self._ocean

    def run_simulation(self, num_it, console_simulation=False):
        '''Runs process of life in ocean simulation. On every iteration cells
        processed consequentially from top to bottom from left to right.

        Parameters
        ----------
        num_it : int
            Number of iterations to be ran. If all predators or all victims
            die earlier the simulation will stop.
        console_simulation : bool, optional
            If true the ocean map will be printed after finishing each
            iteration. On such map: P - predator, V - victim, B - barrier,
            . - empty field.

        Returns
        -------
        out : list
            An array containing (num_predators, num_victims) after each
            iteration up to last.
        '''

        result = []
        num_victims, num_predators = self._count_creatures()
        result.append((num_victims, num_predators))

        if console_simulation:
            self.print_ocean()

        for it in range(num_it):
            if num_victims == 0 or num_predators == 0:
                break
            self._ocean = self._move_creatures()
            self._ocean = self._new_generation()
            self._ocean = self._degenerate_creatures()
            num_victims, num_predators = self._count_creatures()
            result.append(self._count_creatures())
            if console_simulation:
                self.print_ocean()
        return result

if __name__ == '__main__':
    myocean = Ocean(
              width=10, height=10, predators=[(i, i) for i in range(5)],
              victims=[(i, 9 - i) for i in range(5)])
    myocean.run_simulation(10, console_simulation=True)

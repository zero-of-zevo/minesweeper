from game import *
import itertools
from typing import TypeAlias
from functools import reduce

offset: TypeAlias = tuple[int, int]

def diffrentarr(d):
    return list(dict.fromkeys(d, None).keys())

def diffrenttuple(d):
    return tuple(dict.fromkeys(d, None).keys())

class Solve:
    def __init__(self, game:Game) -> None:
        self.game = game
        self.openedblocks:set[offset] = set() # (x, y)
        # self.mineblocks:dict[offset:float] = {} #(x, y): percentage
        self.mineblocks:tuple[offset,...] = ()
        for j in range(game.size[1]):
            for i in range(game.size[0]):
                if self.game.field[j][i].state == State.OPENED and not self.game.field[j][i].around == 0 :
                    self.openedblocks.add((i, j))
        self.validblocks:list[offset] = []
        self.minesets:list[
            tuple[
                list[offset], # centerblock. around
                list[offset], # aroundclosedblockes
                tuple[tuple[offset, ...], ...] # combination of aroundclosedblockes
                ]
            ] = []
    def buildminesets(self):
        for x, y in self.openedblocks:
            aroundclosedblockes:list[offset] = []
            aroundflaggedblockes:list[offset] = []
            for j in (-1, 0, 1):
                for i in (-1, 0, 1):
                    if 0 <= y + j < self.game.size[1] and 0 <= x + i < self.game.size[0]:
                        if self.game.field[y + j][x + i].state == State.CLOSED:
                            aroundclosedblockes.append((x + i,y + j))
                        if self.game.field[y + j][x + i].state == State.FLAGGED:
                            aroundflaggedblockes.append((x + i,y + j))
            if self.game.field[y][x].around - len(aroundflaggedblockes) > 0:
                    self.validblocks.append((x,y))
                    self.minesets.append(
                        (
                            [(x,y)],
                            aroundclosedblockes,
                            tuple(
                                list(itertools.combinations(aroundclosedblockes, self.game.field[y][x].around - len(aroundflaggedblockes)))
                                # list(map(
                                #     lambda x : x*,
                                #     itertools.combinations(
                                #     aroundclosedblockes,
                                #     self.game.field[y][x].around - len(aroundflaggedblockes)
                                #     ))))
                                )))
        self.solveminesets()
    
    def solveminesets(self):
        # self.clearvalid()
        # minesetcouples = list(itertools.combinations(list(self.minesets), 2))
        newminesets:list[
            tuple[
                list[offset], # centerblock. around
                list[offset], # aroundclosedblockes
                tuple[tuple[offset, ...], ...] # combination of aroundclosedblockes
                ]
            ] = []
        
        print("p1")
        # if len([i for i in self.minesets[0][1] if i in self.minesets[1][1]])>0:
        newcenterblocks = self.minesets[0][0] + self.minesets[1][0]
        newaround = diffrentarr(self.minesets[0][1] + self.minesets[1][1])
        intersctrions:list[offset] = diffrentarr([i for i in self.minesets[0][1] if i in self.minesets[1][1]])
        newcombination:list[tuple[offset, ...]] = []
        print("p2")
        # for d0 in self.minesets[0][2]:
        #     for d1 in self.minesets[1][2]:
        #         if [i for i in intersctrions if i in d0] == [i for i in intersctrions if i in d1]:
        #             newcombination.append(diffrenttuple(d0 + d1))
        # for d0 in self.minesets[0][2]:
        #     for d1 in self.minesets[1][2]:
        #         boolean = True
        #         for i in intersctrions:
        #             if (i in d0) ^ (i in d1):
        #                 boolean = False
        #                 break
        #         if boolean:
        #             newcombination.append(diffrenttuple(d0+d1))
        def make_2n(d: tuple[offset, ...], intersctrions: list[offset]):
            n = 0
            for i in intersctrions:
                n = (n << 1) | (i in d)
            return n
        is_in_d0_list = [make_2n(d0, intersctrions) for d0 in self.minesets[0][2]]
        is_in_d1_list = [make_2n(d1, intersctrions) for d1 in self.minesets[1][2]]
        for i0, d0 in enumerate(self.minesets[0][2]):
            is_in_d0 = is_in_d0_list[i0]
            for i1, d1 in enumerate(self.minesets[1][2]):

                is_in_d1 = is_in_d1_list[i1]
                if not (is_in_d0 ^ is_in_d1):
                    newcombination.append(diffrenttuple(d0+d1))
            # print()
            # print(self.minesets[0])
            # print(self.minesets[1])
            # print((
            #         newcenterblocks,
            #         newaround,
            #         tuple(diffrentarr(newcombination))
            #         ))
        
        print("p3")

        newminesets.append((
            newcenterblocks,
            newaround,
            tuple(diffrentarr(newcombination))
            ))
            # else:
            #     newminesets.append(self.minesets[0])
            #     newminesets.append(self.minesets[1])

        print("p4")
        print(len(self.minesets))
        del self.minesets[0:2]
        for i in newminesets:
            self.minesets.insert(0, i)
            
            
        print("p5")
        if not len(self.minesets) == 1:
            self.solveminesets()
            for i in self.minesets[0][2]:
                print(i)
        else:
            print(len(self.minesets[0][2][0]))
            print(self.minesets[0][2][0])
            print(len(diffrentarr(self.minesets[0][2][0])))
            print(diffrentarr(self.minesets[0][2][0]))
            
            # print(len(tuple(set(self.minesets[0][2][0]))))
        #     self.solveminesets()
        
        # print(len(self.minesets))

        # print(minesetcouples[1])
        # print()
        # print(self.minesets[2])
        # print()
        # print(newminesets[2])
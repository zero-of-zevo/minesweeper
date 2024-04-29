from game import *
from typing import TypeAlias
import itertools
from copy import deepcopy

offset:TypeAlias = tuple[int, int]

def diffrentlist(d):
    return list(dict.fromkeys(d, None).keys())

def diffrenttuple(d):
    return tuple(dict.fromkeys(d, None).keys())

class Solve:
    def __init__(self, game:Game):
        self.game: Game = game
        self.validblocks: list[offset] = list()
        self.mineblocks: list[offset] = list()
        self.safeblocks: list[offset] = list()
        self.minepredictsets:list[
            tuple[
                tuple[offset, ...], # aroundclosedblockes
                tuple[tuple[offset, ...], ...] # combination of aroundclosedblockes
                ]
            ] = list()
        self.minepredicts:dict[offset,float] = dict()

    def solve(self):
        #0. valid block 채우기
        self.fillvalidblocks()
        #0. 데이터 정리
        self.cleandatas()
        #1. 확실한 친구 조지기
        self.checkprovedmines()
        
        #2. 안확실한 애들 조지기 준비
        self.setupprediction()

        # if not len(self.mineblocks) + len(self.safeblocks) > 0:
        #     #2. 안확실한 애들 조지기 (확률 계산 전 전처리 알고리즘)
        self.solveminepredictsets()
        
    def fillvalidblocks(self):
        self.validblocks = list()
        for j in range(self.game.size[1]):
            for i in range(self.game.size[0]):
                if self.game.field[j][i].state == State.OPENED and not self.game.field[j][i].around == 0 :
                    check =  False
                    for dj in (-1, 0, 1):
                        for di in (-1, 0, 1):
                            if 0 <=j+dj< self.game.size[1] and 0 <=i+di < self.game.size[0]:
                                if self.game.field[j+dj][i+di].state == State.CLOSED:
                                    if (i+di, j+dj) not in self.mineblocks and (i+di, j+dj) not in self.safeblocks:
                                        check = True
                                        break
                        if check == True:
                            self.validblocks.append((i, j))
                            break
                    
    def cleandatas(self):
        for i, j in self.safeblocks:
            if self.game.field[j][i].state == State.OPENED:
                self.safeblocks.remove((i, j))
        self.minepredictsets = list()
        self.minepredicts = dict()

    def checkprovedmines(self):
        prevminelen = len(self.mineblocks)
        prevsafelen = len(self.safeblocks)
        for x, y in self.validblocks:
            aroundclosedblocks:list[offset] = list()
            aroundmineblocks:list[offset] = list()
            aroundsafeblocks:list[offset] = list()
            for j in (-1, 0, 1):
                for i in (-1, 0, 1):
                    if 0 <= y + j < self.game.size[1] and 0 <= x + i < self.game.size[0]:
                        if self.game.field[y+j][x+i].state == State.FLAGGED:
                            aroundmineblocks.append((x+i,y+j))
                        if self.game.field[y+j][x+i].state == State.CLOSED:
                            if (x+i, y+j) in self.mineblocks:
                                aroundmineblocks.append((x+i,y+j))
                            elif (x+i, y+j) in self.safeblocks:
                                aroundsafeblocks.append((x+i, y+j))
                            else: aroundclosedblocks.append((x+i,y+j))
            around = self.game.field[y][x].around - len(aroundmineblocks)
            # print(around)
            # print(aroundclosedblocks)
            # print(aroundmineblocks)
            # print(aroundsafeblocks)
            if (len(aroundclosedblocks) == around):
                self.mineblocks.extend(aroundclosedblocks)
                self.validblocks.remove((x, y))
            elif(around == 0):
                self.safeblocks.extend(aroundclosedblocks)
                self.validblocks.remove((x, y))

        if not prevminelen == len(self.mineblocks) or not prevsafelen == len(self.safeblocks):
            self.fillvalidblocks()
            self.checkprovedmines()
        else:
            self.fillvalidblocks()
      
    def setupprediction(self):
        # prevresult = len(self.minepredictsets)
        for x, y in self.validblocks:
            aroundblocks:list[offset] = list()
            around = self.game.field[y][x].around
            for j in (-1, 0, 1):
                for i in (-1, 0, 1):
                    if 0 <= y + j < self.game.size[1] and 0 <= x + i < self.game.size[0]:
                        if self.game.field[j+y][i+x].state == State.CLOSED:
                            if (i+x, j+y) in self.mineblocks:
                                around -= 1
                            elif (i+x, j+y) not in self.safeblocks:
                                aroundblocks.append((i+x, j+y))
            self.minepredictsets.append((tuple(aroundblocks), tuple(itertools.combinations(aroundblocks, around))))
            self.minepredictsets = diffrentlist(self.minepredictsets)
        
        #     print(x,y)
        #     print(around)
        #     print((aroundblocks, list(itertools.combinations(aroundblocks, around))))
        # print(self.minepredictsets)
    
    # 여기까진 문제 없음
    
    # def solveminepredictsets(self):
    #     for ci, cj in list(itertools.combinations(range(len(self.minepredictsets)+1), 2)):
    #         print(ci, cj)

    def solveminepredictsets(self):
        print(self.minepredictsets)
        for ci, cj in list(itertools.combinations(range(len(self.minepredictsets)), 2)):
            print()
            intersections:tuple[offset, ...] = tuple(i for i in self.minepredictsets[ci][0] if i in self.minepredictsets[cj][0])
            # print(intersections)
            if len(intersections) > 0:
                newaround:tuple[offset, ...] = diffrenttuple(self.minepredictsets[ci][0]+self.minepredictsets[cj][0])
                print(newaround)
                newcombine:list[tuple[offset,...]] = list()
                print(self.minepredictsets[ci][1])
                print(self.minepredictsets[cj][1])
                for sdi in self.minepredictsets[ci][1]:
                    for sdj in self.minepredictsets[cj][1]:
                        print("i", sdi)
                        print("j", sdj)
            
        # check1 = False
        # naround:tuple[offset, ...] = tuple()
        # ncombine:list[tuple[offset, ...]] = list()
        # for ci, cj in list(itertools.combinations(range(len(self.minepredictsets)), 2)):
        #     intersections:set[offset] = set(self.minepredictsets[ci][0]).intersection(self.minepredictsets[cj][0])
        #     if len(intersections) > 0: check1 = True
        #     if check1:
        #         newaround:tuple[offset, ...] = diffrenttuple(self.minepredictsets[ci][0]+self.minepredictsets[cj][0])
        #         naround = diffrenttuple(self.minepredictsets[ci][0]+self.minepredictsets[cj][0])
        #         newcombine:list[tuple[offset, ...]] = list()
        #         for di in self.minepredictsets[ci][1]:
        #             for dj in self.minepredictsets[cj][1]:
        #                 interi = set(intersections).intersection(set(di))
        #                 interj = set(intersections).intersection(set(dj))
        #                 if interi == interj:
        #                     newcombine.append(diffrenttuple(di+dj))
        #                     ncombine.append(diffrenttuple(di+dj))
        #         break
        # print((naround, tuple(ncombine)))
            
                                
                                    

                            

                
                


        # # prevresult = deepcopy(self.minepredicts)
        # check1 = False
        # for di, dj in list(itertools.combinations(range(len(self.minepredictsets)), 2)):
        #     intersections:list[offset] = list()
        #     for i in self.minepredictsets[di][0]:
        #         if i in self.minepredictsets[dj][0]:
        #             intersections.append(i)
        #     intersections = diffrentlist(intersections)
        #     if len(intersections) > 0: check1 = True
        #     if check1:
        #         # print(di, dj)
        #         # print(self.minepredictsets[di][1])
        #         # print(self.minepredictsets[dj][1])
        #         newcombines:list[tuple[offset, ...]] = list()
        #         for i in self.minepredictsets[di][1]:
        #             for j in self.minepredictsets[dj][1]:
        #                 if len([x for x in intersections if x in diffrentlist(i)]) == len([x for x in intersections if x in diffrentlist(j)]):
        #                     newcombines.append(i + j)
        #         # print(newcombines)
        #         self.minepredictsets.append(
        #             (
        #                 self.minepredictsets[di][0] + self.minepredictsets[dj][0],
        #                 diffrenttuple(newcombines)
        #             )
        #         )
        #         del self.minepredictsets[di]
        #         del self.minepredictsets[dj]
        #         break
        # if check1:
        #     self.solveminepredictsets()
        # else:
        #     if len(self.minepredictsets) > 0:
        #         for i in self.minepredictsets:
        #             minepredictscount:dict[offset,int] = dict()
        #             t:int = 0
        #             for j in i[1]:
        #                 for x in j:
        #                     # print(x)
        #                     if not x in minepredictscount.keys():
        #                         minepredictscount[x] = 0
        #                     if x in minepredictscount.keys():
        #                         minepredictscount[x] += 1
        #                     t+=1
        #                     if not x in self.minepredicts.keys():
        #                         self.minepredicts[x] = 0
        #             for ddd in minepredictscount.keys():
        #                 if minepredictscount[ddd] == 0:
        #                     self.safeblocks.append(ddd)
        #                     print("added safe", ddd)
        #                 elif minepredictscount[ddd] == 1:
        #                     self.mineblocks.append(ddd)
        #                     print("added mine", ddd)

        #                 else: self.minepredicts[ddd] = minepredictscount[ddd]/t
                    
                    
        #     print(self.minepredicts)

        # if not self.minepredicts == prevresult:
        #     self.solveminepredictsets()
        #     print(len(self.minepredictsets))
                    # print(list(itertools.product(
                    #     list(map(lambda x: list(x), self.minepredictsets[di][1])), 
                    #     list(map(lambda x: list(x), self.minepredictsets[di][1])))))
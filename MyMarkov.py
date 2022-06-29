from distutils.dir_util import copy_tree

import numpy as np


class MyMarkov(object):
    def __init__(self, P1, P2, pi01, pi02, dura_set):
        self.n = P1.shape[0]
        self.m = P2.shape[0]
        self.P1 = P1
        self.P2 = P2
        self.pi01 = pi01
        self.pi02 = pi02
        self.dura_set = dura_set

    def generate(self, length=12, time_signature='4/4'):
        beats_list = self.generate_beats_list(length, time_signature)
        ready_index = [i for i in range(self.n)]
        num_list = []
        prev = None
        for measure_beats_list in beats_list:
            measure_note_list = []
            for measure_beats in measure_beats_list:
                if prev is None:
                    note_index = np.random.choice(ready_index, p=self.pi01)
                    measure_note_list.append((note_index, measure_beats))
                    prev = note_index
                    continue
                note_index = np.random.choice(ready_index, p=self.P1[prev])
                measure_note_list.append((note_index, measure_beats))
                prev = note_index
            num_list.append(measure_note_list)
        return num_list

    def generate_beats_list(self, length, time_signature):
        beats_list = []
        ready_index = [i for i in range(self.m)]
        prev = None
        for i in range(length):
            measure_beats_list = []
            measure_beats = 0
            while measure_beats < 4:
                # 方法1
                # beat_index = 6
                # if prev is None:
                #     measure_beats_list.append(self.dura_set[beat_index])
                #     measure_beats += self.dura_set[beat_index]
                #     prev = beat_index

                # 方法2
                if prev is None:
                    beat_index = np.random.choice(ready_index, p=self.pi02)
                    measure_beats_list.append(self.dura_set[beat_index])
                    measure_beats += self.dura_set[beat_index]
                    prev = beat_index
                    continue
                beat_index = np.random.choice(ready_index, p=self.P2[prev])
                if measure_beats + self.dura_set[beat_index] > 4:
                    if (4 - measure_beats) in self.dura_set:
                        measure_beats_list.append(4 - measure_beats)
                        prev = self.dura_set.index(4 - measure_beats)
                        measure_beats = 4
                    continue
                measure_beats_list.append(self.dura_set[beat_index])
                measure_beats += self.dura_set[beat_index]
                prev = beat_index
            beats_list.append(measure_beats_list)
        return beats_list

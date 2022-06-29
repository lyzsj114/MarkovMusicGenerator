import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from midi2audio import FluidSynth
from music21 import *

from MyMarkov import MyMarkov
from utils import *

MUSESCORE_PATH = 'C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe'
SOUND_FONT_PATH = os.path.join(os.getcwd(), 'MuseScore_General.sf3')
environment.set('musescoreDirectPNGPath', MUSESCORE_PATH)


def main_func():
    Z1, Z2, P1, P2, pi01, pi02, note_set, dura_set = get_markov_info_by_name(
        'bach')

    # 可视化矩阵信息
    # sns.heatmap(Z1, xticklabels=note_set, yticklabels=note_set)
    # sns.heatmap(Z2, xticklabels=dura_set, yticklabels=dura_set)
    # sns.heatmap(P1, xticklabels=note_set, yticklabels=note_set)
    # sns.heatmap(P1, xticklabels=dura_set, yticklabels=dura_set)
    # plt.show()

    # print('logging: Z1:\n', Z1, '\n')
    # print('logging: Z2:\n', Z2, '\n')
    print('logging: P1:\n', P1, '\n')
    print('logging: P2:\n', P2, '\n')
    print('logging: pi01:\n', pi01, '\n')
    print('logging: pi02:\n', pi02, '\n')
    print('logging: note_set:\n', note_set, '\n')
    print('logging: dura_set:\n', dura_set, '\n')

    bach_markov = MyMarkov(P1, P2, pi01, pi02, dura_set)
    # beats_list = bach_markov.generate_beats_list(12, '4/4')
    # print('logging: beats_list:\n', beats_list, '\n')
    num_list = bach_markov.generate(12, '4/4')
    print('logging: note_list:\n', num_list, '\n')

    # num_list = [[(4, 1.0), (8, 1.0), (9, 1.0), (7, 1.0)], [(5, 1.0), (6, 1.0), (6, 0.5), (8, 0.5), (6, 1.0)], [(4, 1.0), (7, 0.5), (5, 0.5), (6, 1.0), (8, 1.0)], [(6, 1.0), (7, 1.0), (11, 2.0)], [(13, 1.0), (11, 1.0), (4, 1.0), (3, 1.0)], [(4, 1.0), (4, 1.0), (4, 1.0), (6, 1.0)], [(8, 1.0), (9, 1.0), (9, 0.5), (9, 1.0), (7, 0.5)], [(6, 2.0), (8, 1.0), (6, 1.0)], [(4, 2.0), (0, 2.0)], [(6, 1.0), (7, 1.0), (4, 1.0), (6, 1.0)], [(8, 1.0), (10, 1.0), (11, 1.0), (9, 1.0)], [(11, 1.0), (9, 2.0), (9, 1.0)]]
    # note_set = ['D4', 'E4', 'F4', 'F#4', 'G4', 'A-4', 'A4', 'B-4', 'B4', 'C5', 'D-5', 'D5', 'E-5', 'E5', 'F5', 'F#5', 'G5', 'A5']
    print('Start Generate MIDI music.')
    stream0 = numlist2stream(num_list, note_set)
    stream0.write('midi', 'a.mid')
    print('Transfer MIDI format to MP3 format.')
    fs = FluidSynth(sound_font=SOUND_FONT_PATH)
    fs.midi_to_audio(r'C:\Users\GeniusGrass\Desktop\pymusic\a.mid',
                     r'C:\Users\GeniusGrass\Desktop\pymusic\a.wav') # 保存路径
    return num_list, note_set

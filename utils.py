import numpy as np
from music21 import *

MUSESCORE_PATH = 'C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe'
environment.set('musescoreDirectPNGPath', MUSESCORE_PATH)


def get_markov_info_by_name(name, threshold=21/17755):
    localCorpus = corpus.corpora.CoreCorpus()
    works = localCorpus.search(name, field='composer')
    all_note_list, all_first_note_list = get_all_note_list(works[:200])
    note_set = get_note_set(all_note_list, threshold)
    dura_set = get_dura_set(all_note_list)
    all_pairs = get_note_pairs(works)
    Z1, Z2 = get_transition_matrix(all_pairs, note_set, dura_set)
    P1 = (Z1.T / np.sum(Z1, axis=1)).T
    P2 = (Z2.T / np.sum(Z2, axis=1)).T
    pi01, pi02 = get_pi0(all_first_note_list, note_set, dura_set)
    return Z1, Z2, P1, P2, pi01, pi02, note_set, dura_set


def get_all_note_list(works):
    all_note_list = []
    all_first_note_list = []
    for i in range(len(works)):
        note_list = score2notelist(works[i].parse().parts[0])
        all_note_list.extend(note_list)
        if len(note_list) < 1:
            continue
        all_first_note_list.append(note_list[0])
    return all_note_list, all_first_note_list


def get_pi0(first_note_list, note_set, dura_set):
    pi01 = np.zeros(len(note_set))
    pi02 = np.zeros(len(dura_set))
    f_note = {s: i for i, s in enumerate(note_set)}
    f_dura = {d: i for i, d in enumerate(dura_set)}
    keys1 = f_note.keys()
    keys2 = f_dura.keys()
    for note in first_note_list:
        if note[0] not in keys1:
            continue
        if note[1] not in keys2:
            continue
        index1 = f_note[note[0]]
        index2 = f_dura[note[1]]
        pi01[index1] += 1
        pi02[index2] += 1
    pi01 = pi01 / np.sum(pi01)
    pi02 = pi02 / np.sum(pi02)
    return pi01, pi02


def score2notelist(score):
    note_list = []
    for i in score.flatten():
        if isinstance(i, note.Note):
            name = i.name
            if i.name == 'C#':
                name = 'D-'
            elif i.name == 'D#':
                name = 'E-'
            elif i.name == 'G-':
                name = 'F#'
            elif i.name == 'G#':
                name = 'A-'
            elif i.name == 'A#':
                name = 'B-'
            elif i.name == 'F##':
                name = 'G'
            elif i.name == 'B#':
                name = 'C'
            elif i.name == 'E#':
                name = 'F'
            present = (name+str(i.octave), i.duration.quarterLength)
            note_list.append(present)
    return note_list


def get_note_set(note_list, threshold):
    # 以bach中出现21次为阈值，待改进
    note_set = set([i for i, _ in note_list])
    all_pits = [i for i, _ in note_list]
    count = 0
    new_note_set = []
    for n in note_set:
        num = all_pits.count(n)
        if num > threshold*len(all_pits):
            count = count+1
            new_note_set.append(n)

    def rule(x):
        ET = {'C': 1, 'D-': 2, 'D': 3, 'E-': 4, 'E': 5, 'F': 6,
              'F#': 7, 'G': 8, 'A-': 9, 'A': 10, 'B-': 11, 'B': 12}
        return int(x[-1])*13 + ET[x[:-1]]

    new_note_set = sorted(new_note_set, key=rule)

    return new_note_set


def get_dura_set(note_list, unit=0.0625, max=4):
    all_dura = [j for _, j in note_list]
    dura_set = set(all_dura)
    new_dura_set = []

    for d in dura_set:
        if d % unit == 0 and d > 0 and d <= max:
            new_dura_set.append(d)
    new_dura_set = sorted(new_dura_set)

    return new_dura_set


def get_note_pairs(works):
    prev = None
    all_pairs = []
    for i in range(len(works)):
        score = works[i].parse().parts[0]
        for n in score2notelist(score):
            present = n
            if prev is None:
                prev = present
                continue
            pair = (present, prev)
            prev = present
            all_pairs.append(pair)
    return all_pairs


def get_transition_matrix(all_pairs, note_set, dura_set):
    n = len(note_set)
    m = len(dura_set)
    f_note = {s: i for i, s in enumerate(note_set)}
    f_dura = {d: i for i, d in enumerate(dura_set)}
    keys1 = f_note.keys()
    keys2 = f_dura.keys()
    Z1 = np.zeros((n, n))
    Z2 = np.zeros((m, m))
    for p in all_pairs:
        first, second = p
        if first[0] not in keys1 or second[0] not in keys1:
            continue
        if first[1] not in keys2 or second[1] not in keys2:
            continue
        i1 = f_note[first[0]]
        j1 = f_note[second[0]]
        i2 = f_dura[first[1]]
        j2 = f_dura[second[1]]
        Z1[i1, j1] += 1
        Z2[i2, j2] += 1
    return Z1, Z2


def numlist2stream(num_list, note_set, time_signature='4/4'):
    stream0 = stream.Stream()
    for index, num_measure_list in enumerate(num_list):
        temp_measure = stream.Measure(number=index)
        if index == 0:
            temp_measure.timeSignature = meter.TimeSignature(time_signature)
        for num in num_measure_list:
            temp_note = note.Note(note_set[num[0]])
            temp_note.duration = duration.Duration(num[1])
            temp_measure.append(temp_note)
        stream0.append(temp_measure)
    return stream0

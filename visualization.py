import os
import sys
from msilib.schema import Component

from manimlib import *
from OpenGL.GL.images import DATA_SIZE_NAMES
from typing_extensions import runtime

from my_main import main_func

sys.path.append(r'C:\Users\GeniusGrass\Desktop\pymusic') # 运行路径


class geometry(Scene):
    ONE_ROW_NUM = 6
    COLOR_LIST = [RED_E, RED_D, RED_C, RED_B, RED_A,
                  MAROON_E, MAROON_D, MAROON_C, MAROON_B, MAROON_A,
                  PURPLE_E, PURPLE_D, PURPLE_C, PURPLE_B, PURPLE_A,
                  BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A,
                  TEAL_E, TEAL_D, TEAL_C, TEAL_B, TEAL_A,
                  GREEN_E, GREEN_D, GREEN_C, GREEN_B, GREEN_A]

    def construct(self):
        self.note_list, self.note_set = main_func()
        # self.note_set = ['D4', 'E4', 'F4', 'F#4', 'G4', 'A-4', 'A4', 'B-4', 'B4', 'C5', 'D-5', 'D5', 'E-5', 'E5', 'F5', 'F#5', 'G5', 'A5']
        # self.note_list = [[(4, 1.0), (8, 1.0), (9, 1.0), (7, 1.0)], [(5, 1.0), (6, 1.0), (6, 0.5), (8, 0.5), (6, 1.0)], [(4, 1.0), (7, 0.5), (5, 0.5), (6, 1.0), (8, 1.0)], [(6, 1.0), (7, 1.0), (11, 2.0)], [(13, 1.0), (11, 1.0), (4, 1.0), (3, 1.0)], [(4, 1.0), (4, 1.0), (4, 1.0), (6, 1.0)], [(8, 1.0), (9, 1.0), (9, 0.5), (9, 1.0), (7, 0.5)], [(6, 2.0), (8, 1.0), (6, 1.0)], [(4, 2.0), (0, 2.0)], [(6, 1.0), (7, 1.0), (4, 1.0), (6, 1.0)], [(8, 1.0), (10, 1.0), (11, 1.0), (9, 1.0)], [(11, 1.0), (9, 2.0), (9, 1.0)]]
        print('Start Generate animate.')

        note_list_flatten = []
        for part in self.note_list:
            note_list_flatten.extend([note for note in part])
        self.pannel, self.note_map = self.construct_pannel(note_list_flatten)
        self.subpannel = self.construct_subpannel(note_list_flatten)

        self.add(self.pannel)

        self.wait(2)

        prev = None
        arrow = None
        for note in note_list_flatten:
            if prev is None:
                point = self.note_map[self.note_set[note[0]]]
                self.play(
                    FadeIn(self.subpannel[point[0]][point[1]]).set_run_time(note[1]/2))
                prev = note
                continue
            if arrow is not None:
                arrow = self.play_note_trans(prev, note, arrow)
            else:
                arrow = self.play_note_trans(prev, note)
            prev = note
        self.play(FadeOut(arrow))
        point = self.note_map[self.note_set[note[0]]]
        self.play(FadeOut(self.subpannel[point[0]]
                  [point[1]]).set_run_time(note[1]/2))
        self.play(FadeOut(self.pannel))
        self.wait(1)
        # self.play(ShowCreation(arrow).set_run_time(0.125))
        # self.play(ShowCreation(arrow).set_run_time(0.25))
        # self.play(ShowCreation(arrow).set_run_time(0.5))
        # self.play(ShowCreation(arrow).set_run_time(1))
        # self.play(FadeOut(arrow).set_run_time(1))

    def construct_pannel(self, note_list_flatten):
        note_map = {}
        real_note_set = set([note[0] for note in note_list_flatten])
        pannel = Group()
        rows = []
        count = 0
        for i in range(len(self.note_set)):
            if i not in real_note_set:
                continue
            c = Circle(radius=0.5)
            # c.set_fill(self.COLOR_LIST[count], opacity=1)
            c.set_stroke(self.COLOR_LIST[count])
            t = Text(self.note_set[i])
            temp = Group(c, t)
            if count % self.ONE_ROW_NUM == 0:
                rows.append([])
            note_map[self.note_set[i]] = (
                count // self.ONE_ROW_NUM, count % self.ONE_ROW_NUM)
            rows[count // self.ONE_ROW_NUM].append(temp)
            count += 1

        for r in rows:
            row = Group()
            for item in r:
                row.add(item)
            row.arrange(RIGHT, buff=0.5)
            pannel.add(row)
        pannel.arrange(DOWN, buff=0.5)
        return pannel, note_map

    def construct_subpannel(self, note_list_flatten):
        real_note_set = set([note[0] for note in note_list_flatten])
        pannel = Group()
        rows = []
        count = 0
        for i in range(len(self.note_set)):
            if i not in real_note_set:
                continue
            c = Circle(radius=0.5)
            c.set_fill(self.COLOR_LIST[count], opacity=1)
            c.set_stroke(self.COLOR_LIST[count])
            t = Text(self.note_set[i])
            temp = Group(c, t)
            if count % self.ONE_ROW_NUM == 0:
                rows.append([])
            rows[count // self.ONE_ROW_NUM].append(temp)
            count += 1

        for r in rows:
            row = Group()
            for item in r:
                row.add(item)
            row.arrange(RIGHT, buff=0.5)
            pannel.add(row)
        pannel.arrange(DOWN, buff=0.5)
        return pannel

    def play_note_trans(self, note1, note2, prev_arrow=None):
        start_point = self.note_map[self.note_set[note1[0]]]
        end_point = self.note_map[self.note_set[note2[0]]]
        if start_point[0] == 0 and end_point[0] == 0:
            if start_point[1] > end_point[1]:
                angle = TAU / 4.
            else:
                angle = -TAU / 4.
                # angle = TAU / 4. * 2
            start_point_pos = self.pannel[start_point[0]
                                          ][start_point[1]].get_top()
            end_point_pos = self.pannel[end_point[0]][end_point[1]].get_top()
        elif start_point[0] == 0 and end_point[0] == 1:
            start_point_pos = self.pannel[start_point[0]
                                          ][start_point[1]].get_top()
            end_point_pos = self.pannel[end_point[0]][end_point[1]].get_top()
            angle = TAU / 4. * 2
        else:
            start_point_pos = self.pannel[start_point[0]
                                          ][start_point[1]].get_bottom()
            end_point_pos = self.pannel[end_point[0]
                                        ][end_point[1]].get_bottom()
            if start_point[1] > end_point[1]:
                angle = -TAU / 4. * 2
            else:
                angle = TAU / 4. * 2

        if start_point == end_point:
            start_point_pos = self.pannel[start_point[0]
                                          ][start_point[1]].get_top()
            end_point_pos = self.pannel[end_point[0]
                                        ][end_point[1]].get_bottom()
            angle = -TAU / 4. * 3

        arrow = CurvedArrow(
            start_point=start_point_pos,
            end_point=end_point_pos,
            angle=angle
        )
        # elif start_point[0] == 0 and end_point[0] == 1:
        #     arrow = CurvedArrow(
        #         start_point=self.pannel[start_point[0]][start_point[1]].get_top(),
        #         end_point=self.pannel[end_point[0]][end_point[1]].get_top(),
        #         angle= PI*int(start_point[0] > end_point[0]) - TAU / 4.
        #     )

        if prev_arrow is not None:
            self.play(FadeOut(prev_arrow), FadeOut(self.subpannel[start_point[0]][start_point[1]]), ShowCreation(
                arrow), FadeIn(self.subpannel[end_point[0]][end_point[1]]), run_time=note2[1]/2)
        else:
            self.play(FadeOut(self.subpannel[start_point[0]][start_point[1]]), ShowCreation(
                arrow), FadeIn(self.subpannel[end_point[0]][end_point[1]]), run_time=note2[1]/2)
        # self.play(FadeOut(arrow).set_run_time(0.25))
        return arrow


if __name__ == "__main__":
    print('Start Generate Markov Model.')
    os.system(
        "manimgl {} geometry -ow".format(os.path.join(os.getcwd(), 'visualization.py')))
    os.system("ffmpeg -i {} -i {} -filter_complex \"[1]adelay=2000|2000[del1],[0][del1]amix\" {}".format(
        r'C:\Users\GeniusGrass\Desktop\pymusic\background.wav',
        r'C:\Users\GeniusGrass\Desktop\pymusic\a.wav',
        r'C:\Users\GeniusGrass\Desktop\pymusic\full_music.mp3')) # 文件路径及保存路径
    print('Start Generate Final video.')
    os.system("ffmpeg  -y -i {} -i {} -c:v copy -c:a aac -strict experimental {}".format(
        r'C:\Users\GeniusGrass\Desktop\pymusic\videos\geometry.mp4',
        r'C:\Users\GeniusGrass\Desktop\pymusic\full_music.mp3',
        r'C:\Users\GeniusGrass\Desktop\pymusic\videos\new.mp4'
    )) # 文件路径及保存路径

# MarkovMusicGenerator

![](https://github.com/lyzsj114/MarkovMusicGenerator/blob/main/example_Moment.jpg)

MarkovMusicGenerator是一个基于python的`music21`库构建的MIDI音乐生成及可视化框架，简单构造了Markov模型，并利用`music21`库中包含的语料库进行学习，实现了初步的MIDI旋律生成，同时结合`manimn`库实现了自动生成MIDI旋律可视化视频。

## Requirements

仅列出不常见的包:

- music21
- midi2audio
- manimlib
- ffmpeg

## Installation

music21

```
pip install music21
```

*若需要music21内的show()实现打谱，需要安装打谱软件，如免费的[MuseScore3](https://musescore.org/en/3.0)。*

midi2audio 需先安装 [FluidSynth](https://github.com/FluidSynth/fluidsynth)

```
pip install midi21audio
```

manimlib 需先安装Latex、ffmpeg等依赖，详细安装见于[manimlib](https://github.com/3b1b/manim)

## Run

首先，修改各py文件内的依赖软件路径及运行与保存路径，如`my_main.py`中的`MUSESCORE_PATH`、`SOUND_FONT_PATH`，`visualization`中的多个保存路径等。

其后，直接运行`visualization.py`即可。

```
python visualization.py
```

## Others

本项目主要目的是完成课程目标，代码架构仍不完整且缺乏注释，同时由于目标过于理想，导致实现所需依赖较为复杂，综合而言复现具有一定难度。最后，如果对该项目感兴趣，或想进一步扩展可以与我联系`lyzsj114@gmail.com`。

import cv2
import os
import click
from parselmouth import Sound
import matplotlib.pyplot as plt
from pathlib import Path

from lingualabpy.plot import draw_pitch, draw_spectrogram


@click.command()
@click.option("--output", default=None, help="")
@click.argument("audiofile", nargs=1, type=click.Path(exists=True))
def main(audiofile, output):
    if not output:
        output = Path(audiofile).stem + ".png"

    sound = Sound(audiofile)

    pitch = sound.to_pitch()

    # If desired, pre-emphasize the sound fragment before calculating the spectrogram
    pre_emphasized_snd = sound.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(
        window_length=0.03, maximum_frequency=8000
    )

    # amplitude figure
    tmp_amplitude_png = "tmp_amplitude.png"
    amplitude = plt.figure()
    plt.plot(sound.xs(), sound.values.T)
    plt.xlim([sound.xmin, sound.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")
    amplitude.set_figwidth(sound.xmax / 4)
    plt.savefig(tmp_amplitude_png)

    # spectro pitch figure
    tmp_spectro_pitch_png = "tmp_spectro_pitch.png"
    spectro_pitch = plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch(pitch)
    plt.xlim([sound.xmin, sound.xmax])
    spectro_pitch.set_figwidth(sound.xmax / 4)
    plt.savefig(tmp_spectro_pitch_png)

    # concatenation
    fig_concat = cv2.vconcat(
        [cv2.imread(tmp_amplitude_png), cv2.imread(tmp_spectro_pitch_png)]
    )
    cv2.imwrite(output, fig_concat)
    os.remove(tmp_amplitude_png)
    os.remove(tmp_spectro_pitch_png)

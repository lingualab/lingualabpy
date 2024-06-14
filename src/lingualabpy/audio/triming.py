from pydub import AudioSegment


def extract_audio(audio: AudioSegment, intervals: list[list[float]]) -> AudioSegment:
    """"""
    new_audio = AudioSegment.empty()

    for start, end in intervals:
        new_audio += audio[start * 1000 : end * 1000]

    return new_audio

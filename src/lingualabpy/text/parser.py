import re
from docx import Document
from collections import defaultdict


def parse_waywithwords(document: Document) -> dict:
    """"""
    waywithwords = {
        "IV": "interviewer",
        "IE": "interviewee",
    }

    results = defaultdict(list)

    for para in document.paragraphs:
        try:
            content = para.text.split()
            speaker = content[0]
            transcription = " ".join(content[1:])
        except:
            speaker = None

        if (
            speaker in waywithwords.keys()
            and not transcription.lower() in waywithwords.values()
        ):
            results[waywithwords[speaker]].append(transcription)

        elif re.findall(r"[0-9][0-9]:[0-5][0-9]:[0-5][0-9]", para.text):
            results["time"].append(para.text)

        else:
            results["remainder"].append(para.text)

    return results

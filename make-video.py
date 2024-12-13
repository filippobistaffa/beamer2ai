import warnings
warnings.filterwarnings("ignore", ".*To copy construct from a tensor, it is recommended to use*")
warnings.filterwarnings("ignore", ".*It is possible to construct malicious pickle data which*")
warnings.filterwarnings("ignore", ".*is deprecated*")

import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

# PDF image extraction
import fitz

# Bark
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
# download and load all models
print("Loading Bark models into GPU...")
preload_models()

# standard packages
import numpy as np
import subprocess
import tempfile


def text_to_audio(text, audio_path, voice_preset):
    print("Generating audio from sentences...")
    silence = np.zeros(int(0.25 * SAMPLE_RATE))
    sentences = text.split(".")
    audio_chunks = []
    for sentence in sentences:
        if len(sentence) == 0:
            continue
        print(sentence.strip())
        audio_array = generate_audio(sentence.strip() + '.', history_prompt=voice_preset)
        audio_chunks += [audio_array, silence.copy()]
    write_wav(audio_path, rate=SAMPLE_RATE, data=np.concatenate(audio_chunks))


def page_audio_to_video(pdf_path, page_number, audio_path, video_path, resolution):
    print("Encoding video and muxing audio...")
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]
    pix = page.get_pixmap(dpi=600)
    temp_image = tempfile.NamedTemporaryFile(suffix=".png")
    image_path = temp_image.name
    pix.save(image_path)
    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-vf", "scale={}:{}".format(*resolution),
        "-pix_fmt", "yuv420p",
        "-shortest",
        video_path
    ]
    with open(os.devnull, "w") as devnull:
        subprocess.run(ffmpeg_command, check=True, stdout=devnull, stderr=devnull)
    temp_image.close()
    doc.close()


def text_page_to_video(text, voice_preset, pdf_path, page_number, video_path, resolution):
    temp_audio = tempfile.NamedTemporaryFile(suffix=".wav")
    audio_path = temp_audio.name
    text_to_audio(
        text=text,
        audio_path=audio_path,
        voice_preset=voice_preset
    )
    page_audio_to_video(
        pdf_path=pdf_path,
        page_number=page_number,
        audio_path=audio_path,
        video_path=video_path,
        resolution=resolution
    )
    temp_audio.close()


def concatenate_videos(video_list, video_path):
    print("Concatenating video chunks...")
    temp_list = tempfile.NamedTemporaryFile(suffix=".txt")
    list_path = temp_list.name
    with open(list_path, "w") as f:
        for video in video_list:
            f.write(f"file \'{os.path.abspath(video)}\'\n")
    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        video_path
    ]
    with open(os.devnull, "w") as devnull:
        subprocess.run(ffmpeg_command, check=True, stdout=devnull, stderr=devnull)
    temp_list.close()


if __name__ == "__main__":

    # https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c
    voice_preset = "v2/en_speaker_8"

    text_page_to_video(
        text='Hello everyone, welcome to the presentation of our work entitled "Recommending Green Routes for Pedestrians to Reduce the Exposure to Air Pollutants in Barcelona". This is a joint work between the Artificial Intelligence Research Institute and the University of Pompeu Fabra in Barcelona.',
        voice_preset=voice_preset,
        pdf_path="../main.pdf",
        page_number=1,
        video_path="1.mp4",
        resolution=(3840, 2160)
    )

    text_page_to_video(
        text='The main issue we tackle in this work is how to recommend green routes to pedestrians that minimize the exposure to air pollutants in a city. Pedestrians are the most vulnerable individuals when it comes to air pollution, which can lead to serious health problems.',
        voice_preset=voice_preset,
        pdf_path="../main.pdf",
        page_number=2,
        video_path="2.mp4",
        resolution=(3840, 2160)
    )

    concatenate_videos(
        [
            "1.mp4",
            "2.mp4",
        ],
        "output.mp4"
    )

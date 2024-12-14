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
import re


def text_to_audio(text, output_audio_path, voice_preset):
    print("Generating audio from sentences...")
    silence = np.zeros(int(0.25 * SAMPLE_RATE))
    sentences = re.split(r'(?<!\d)\.', text)
    audio_chunks = []
    for sentence in sentences:
        if len(sentence) == 0:
            continue
        print(sentence.strip())
        audio_array = generate_audio(sentence.strip() + '.', history_prompt=voice_preset)
        audio_chunks += [audio_array, silence.copy()]
    write_wav(output_audio_path, rate=SAMPLE_RATE, data=np.concatenate(audio_chunks))


def page_audio_to_video(input_pdf_path, page_number, input_audio_path, output_video_path, resolution):
    with tempfile.NamedTemporaryFile(suffix=".png") as temp_image:
        print("Encoding video and muxing audio...")
        doc = fitz.open(input_pdf_path)
        page = doc[page_number - 1]
        pix = page.get_pixmap(dpi=600)
        pix.save(temp_image.name)
        ffmpeg_command = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", temp_image.name,
            "-i", input_audio_path,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-vf", "scale={}:{}".format(*resolution),
            "-pix_fmt", "yuv420p",
            "-shortest",
            output_video_path
        ]
        with open(os.devnull, "w") as devnull:
            subprocess.run(ffmpeg_command, check=True, stdout=devnull, stderr=devnull)
        doc.close()


def text_page_to_video(text, voice_preset, input_pdf_path, page_number, output_video_path, resolution):
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio:
        text_to_audio(
            text=text,
            output_audio_path=temp_audio.name,
            voice_preset=voice_preset
        )
        page_audio_to_video(
            input_pdf_path=input_pdf_path,
            page_number=page_number,
            input_audio_path=temp_audio.name,
            output_video_path=output_video_path,
            resolution=resolution
        )


def concatenate_chunks(temp_chunks, output_video_path):
    print("Concatenating video chunks...")
    with tempfile.NamedTemporaryFile(suffix=".txt") as temp_list:
        with open(temp_list.name, "w") as f:
            for temp_chunk in temp_chunks:
                f.write(f"file \'{os.path.abspath(temp_chunk.name)}\'\n")
        ffmpeg_command = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", temp_list.name,
            "-c", "copy",
            output_video_path
        ]
        with open(os.devnull, "w") as devnull:
            subprocess.run(ffmpeg_command, check=True, stdout=devnull, stderr=devnull)


def generate_video(input_pdf_path, scripts, voice_preset, output_video_path, resolution, repeat=1, skip=False):
    if not(skip):
        for i in range(repeat):
            temp_chunks = []
            for script in scripts:
                temp_chunk = tempfile.NamedTemporaryFile(suffix=".mp4")
                temp_chunks.append(temp_chunk)
                text_page_to_video(
                    text=script["text"],
                    page_number=script["pdf_page_number"],
                    voice_preset=voice_preset,
                    input_pdf_path=input_pdf_path,
                    output_video_path=temp_chunk.name,
                    resolution=resolution
                )
            concatenate_chunks(
                temp_chunks=temp_chunks,
                output_video_path=output_video_path.format(i)
            )
            for temp_chunk in temp_chunks:
                temp_chunk.close()

import warnings
warnings.filterwarnings("ignore", ".*dropout option adds dropout after all but last recurrent layer*")
warnings.filterwarnings("ignore", ".*To copy construct from a tensor, it is recommended to use*")
warnings.filterwarnings("ignore", ".*It is possible to construct malicious pickle data which*")
warnings.filterwarnings("ignore", ".*is deprecated*")

import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

# PDF image extraction
import fitz

# StyleTTS2
from styletts2 import tts
model = tts.StyleTTS2()
SAMPLE_RATE = 24000

# standard packages
from scipy.io.wavfile import write as write_wav
import numpy as np
import subprocess
import tempfile
import re


def text_to_audio(text, output_audio_path):
    print("Generating audio from sentences...")
    silence = np.zeros(int(0.25 * SAMPLE_RATE))
    sentences = re.split(r'(?<!\d)\.', text)
    audio_chunks = []
    for sentence in sentences:
        if len(sentence) == 0:
            continue
        print(sentence.strip())
        audio_array = model.inference(
            sentence.strip() + '.',
            output_sample_rate=SAMPLE_RATE,
            #diffusion_steps=10,
            alpha=1,
            beta=1
        )
        audio_chunks += [audio_array, silence.copy()]
    write_wav(output_audio_path, rate=SAMPLE_RATE, data=np.concatenate(audio_chunks))


def page_audio_to_video(input_pdf_path, dpi, page_number, input_audio_path, output_video_path, resolution, show_ffmpeg):
    print("Encoding video and muxing audio...")
    with tempfile.NamedTemporaryFile(suffix=".png") as temp_image:
        with fitz.open(input_pdf_path) as pdf:
            page = pdf[page_number - 1]
            pix = page.get_pixmap(dpi=dpi)
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
            if show_ffmpeg:
                subprocess.run(ffmpeg_command, check=True)
            else:
                with open(os.devnull, "w") as devnull:
                    subprocess.run(ffmpeg_command, check=True, stdout=devnull, stderr=devnull)


def text_page_to_video(text, input_pdf_path, dpi, page_number, output_video_path, resolution, show_ffmpeg):
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio:
        text_to_audio(
            text=text,
            output_audio_path=temp_audio.name,
        )
        page_audio_to_video(
            input_pdf_path=input_pdf_path,
            dpi=dpi,
            page_number=page_number,
            input_audio_path=temp_audio.name,
            output_video_path=output_video_path,
            resolution=resolution,
            show_ffmpeg=show_ffmpeg
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


def generate_video(input_pdf_path, dpi, scripts, output_video_path, resolution, show_ffmpeg=False, skip=False):
    if not(skip):
        temp_chunks = []
        for script in scripts:
            temp_chunk = tempfile.NamedTemporaryFile(suffix=".mp4")
            temp_chunks.append(temp_chunk)
            text_page_to_video(
                text=script["text"],
                page_number=script["pdf_page_number"],
                input_pdf_path=input_pdf_path,
                dpi=dpi,
                output_video_path=temp_chunk.name,
                resolution=resolution,
                show_ffmpeg=show_ffmpeg
            )
        concatenate_chunks(
            temp_chunks=temp_chunks,
            output_video_path=output_video_path
        )
        for temp_chunk in temp_chunks:
            temp_chunk.close()

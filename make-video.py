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


def text_to_audio(text, output_audio_path, voice_preset):
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


def generate_video(input_pdf_path, scripts, voice_preset, output_video_path, resolution):
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
        output_video_path=output_video_path
    )
    for temp_chunk in temp_chunks:
        temp_chunk.close()


if __name__ == "__main__":

    # Bark voice presets
    # https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c

    generate_video(
        input_pdf_path="../main.pdf",
        scripts=[
            {
                "text": 'Welcome to the presentation of our work entitled "Recommending Green Routes for Pedestrians ' +
                        'to Reduce the Exposure to Air Pollutants in Barcelona". This is joint work between the ' +
                        'Artificial Intelligence Research Institute and the UPF University in Barcelona.',
                "pdf_page_number": 1,
            },
            {
                "text": 'The main issue we tackle in this work is how to recommend green routes to pedestrians ' +
                        'that minimize the exposure to air pollutants in a city. Now, pedestrians are the most vulnerable ' +
                        'individuals when it comes to air pollution, which can lead to serious health problems.',
                "pdf_page_number": 2,
            },
            {
                "text": 'Along these lines, answering this research question could be of great interest for citizens ' +
                        'that wonder if there are greener alternatives for their commute, even if it implies walking a little longer.',
                "pdf_page_number": 3,
            },
            {
                "text": 'Similarly, public administrations concerned with their citizens\'s health could be interested ' +
                        'in a tool capable of providing greener alternatives to the routes computed by Google Maps, ' +
                        'which disregard the exposure to air pollutants.',
                "pdf_page_number": 4,
            },
            {
                "text": 'In this work we provide a solution to these research questions with our green route prototype, showcasing it ' +
                        'for the city of Barcelona. Specifically, we can compute routes that minimize the exposure to air pollutants, ' +
                        'rather than minimizing the total distance as usually done in normal routing problems.',
                "pdf_page_number": 5,
            },
            {
                "text": 'The exposure is computed by considering historical air quality data provided by the Barcelona\' city council. ' +
                        'This data source is characterized by very high spatial resolution, since it provides a measurement for each road. ' +
                        'On the other hand, it is characterized by low temporal resolution, since it is published once per year.',
                "pdf_page_number": 6,
            },
            {
                "text": 'Our prototype can also incorporate the data provided by seven real-time air quality sensors in Barcelona. ' +
                        'Since there are few data points, this data source has very low spatial resolution, compared to the historical one.',
                "pdf_page_number": 7,
            },
            {
                "text": 'To account for this heterogeneity, our prototype incorporates the technique we recently proposed ' +
                        'based a Graph Neural Network trained on the high-resolution historical data. ' +
                        'This aspect is fundamental as real-time data can differ significantly from historical data in a certain location. ' +
                        'Therefore, accounting for real-time data allows us to recommend green routes with more accurate, hence lower, exposure.',
                "pdf_page_number": 8,
            },
            {
                "text": 'This is the architecture of our prototype, showing how the different components interact. ' +
                        'Each component is implemented in Python, using state of the art libraries for fetching data from OpenStreetMap, ' +
                        'routing and showing the results to the user.',
                "pdf_page_number": 9,
            },
        ],
        voice_preset="v2/en_speaker_8",
        output_video_path="output.mp4",
        resolution=(3840, 2160)
    )

# PDF image extraction
import fitz

# standard packages
import subprocess
import tempfile
import time
import os

# global timers
piper_time = 0
ffmpeg_time = 0
timing_function = time.time


def text_to_audio(text, output_audio_path, model_path):
    global piper_time
    print("Generating audio from sentences...")
    piper_command = [
        os.path.join("piper", "piper"),
        "--model", model_path,
        "--output_file", output_audio_path
    ]
    start_time = timing_function()
    subprocess.run(
        piper_command,
        input=(text.strip() + '.').encode("utf-8"),
        check=True
    )
    end_time = timing_function()
    piper_time += end_time - start_time


def page_audio_to_video(input_pdf_path, dpi, page_number, input_audio_path, output_video_path, resolution, show_ffmpeg):
    global ffmpeg_time
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
            start_time = timing_function()
            if show_ffmpeg:
                subprocess.run(ffmpeg_command, check=True)
            else:
                with open(os.devnull, "w") as devnull:
                    subprocess.run(ffmpeg_command, check=True, stdout=devnull, stderr=devnull)
            end_time = timing_function()
            ffmpeg_time += end_time - start_time


def text_page_to_video(text, model_path, input_pdf_path, dpi, page_number, output_video_path, resolution, show_ffmpeg):
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio:
        text_to_audio(
            text=text,
            output_audio_path=temp_audio.name,
            model_path=model_path
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
    global ffmpeg_time
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
        start_time = timing_function()
        with open(os.devnull, "w") as devnull:
            subprocess.run(ffmpeg_command, check=True, stdout=devnull, stderr=devnull)
        end_time = timing_function()
        ffmpeg_time += end_time - start_time


def generate_video(input_pdf_path, dpi, scripts, model_path, output_video_path, resolution, show_ffmpeg=False, skip=False):
    global ffmpeg_time
    ffmpeg_time = 0
    global piper_time
    piper_time = 0
    if not skip:
        temp_chunks = []
        start_time = timing_function()
        for script in scripts:
            temp_chunk = tempfile.NamedTemporaryFile(suffix=".mp4")
            temp_chunks.append(temp_chunk)
            text_page_to_video(
                text=script["text"],
                page_number=script["pdf_page_number"],
                model_path=model_path,
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
        end_time = timing_function()
        # Print timing results
        total_runtime = end_time - start_time
        print(f"\033[1mTotal runtime: {total_runtime:.2f} seconds\033[0m")
        print(f"\033[1mTotal Piper runtime: {piper_time:.2f} seconds ({(piper_time / total_runtime) * 100:.2f}%)\033[0m")
        print(f"\033[1mTotal FFmpeg runtime: {ffmpeg_time:.2f} seconds ({(ffmpeg_time / total_runtime) * 100:.2f}%)\033[0m")

Generate Video Presentations from Beamer Slides
===================
This project allows one to generate a video presentation based on Beamer slides. Specifically, provided a text script for each slide, the presentation is narrated using the voice generated with [MeloTTS](https://github.com/myshell-ai/MeloTTS), a SOTA TTS AI model.


Dependencies
----------

This project requires a modern version of `ffmpeg` to render the video. On Ubuntu, it can be installed with:

    sudo apt install ffmpeg

Although not mandatory, running the project in a Python *virtual environment* is recommended:

    python3 -m venv venv
    source venv/bin/activate

Required Python dependencies can then be installed via `pip` with the following command:

    pip install --upgrade -r requirements.txt

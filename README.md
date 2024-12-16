Generate Video Presentations from PDF Slides
===================
This project allows one to generate a video presentation based on PDF slides. Specifically, provided a text script for each slide, the presentation is narrated using the voice generated with [MeloTTS](https://github.com/myshell-ai/MeloTTS), a SOTA TTS model.


Dependencies
----------

This project requires a modern version of `ffmpeg` to render the video. On Ubuntu, it can be installed with:

    sudo apt install ffmpeg

Although not mandatory, running the project in a Python *virtual environment* is recommended:

    python3 -m venv venv
    source venv/bin/activate

Required Python dependencies can then be installed via `pip` with the following command:

    pip install --upgrade -r requirements.txt


Notes on MeloTTS _vs_ Bark
----------

- MeloTTS generates a voice arguably less realistic than [Bark](https://github.com/filippobistaffa/beamer2ai/tree/bark), but it's more reliable.
- MeloTTS works better than Bark with [non-English languages](https://github.com/myshell-ai/MeloTTS?tab=readme-ov-file#introduction) as well (see the [example](https://github.com/filippobistaffa/beamer2ai/blob/melo/spanish.py) for Spanish).
- MeloTTS is faster than Bark (fast enough for CPU real-time inference).

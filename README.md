Generate Video Presentations from PDF Slides
===================
This project allows one to generate a video presentation based on PDF slides. Specifically, provided a text script for each slide, the presentation is narrated using the voice generated with [Piper](https://github.com/rhasspy/piper), a SOTA TTS model.


Installing Piper
----------

[Piper's files](https://github.com/rhasspy/piper?tab=readme-ov-file#installation) (`piper` binary and all necessary libraries) need to be placed in the `piper` subfolder.


Dependencies
----------

This project requires a modern version of `ffmpeg` to render the video. On Ubuntu, it can be installed with:

    sudo apt install ffmpeg

Although not mandatory, running the project in a Python *virtual environment* is recommended:

    python3 -m venv venv
    source venv/bin/activate

Required Python dependencies can then be installed via `pip` with the following command:

    pip install --upgrade -r requirements.txt


Notes on Piper _vs_ Bark
----------

- Piper generates a voice arguably less realistic than [Bark](https://github.com/filippobistaffa/beamer2ai/tree/bark), but it's more reliable.
- Piper works better than Bark with [non-English languages](https://github.com/rhasspy/piper/blob/master/VOICES.md) as well ([listen to voice samples](https://rhasspy.github.io/piper-samples) of available languages)
- Piper is faster than Bark (fast enough for CPU real-time inference).

Generate Video Presentations from PDF Slides
===================
This project allows one to generate a video presentation based on PDF slides. Specifically, given a text script for each slide, the presentation is narrated using the voice generated with [Bark](https://github.com/suno-ai/bark), a SOTA TTS model. We also provide a version of this project using [MeloTTS](https://github.com/filippobistaffa/beamer2ai/tree/melo) and [StyleTTS2](https://github.com/filippobistaffa/beamer2ai/tree/styletts2) models.


Dependencies
----------

This project requires a modern version of `ffmpeg` to render the video. On Ubuntu, it can be installed with:

    sudo apt install ffmpeg

Although not mandatory, running the project in a Python *virtual environment* is recommended:

    python3 -m venv venv
    source venv/bin/activate

Required Python dependencies can then be installed via `pip` with the following command:

    pip install --upgrade -r requirements.txt


Notes on Bark
----------

Bark supports a variety of voices and languages, which can be explored [here](https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c).
Each Bark execution generates "stochastic" voices from scratch, so results can vary from one execution to another. For this reason, it is convenient to [generate multiple instances](https://github.com/filippobistaffa/beamer2ai/blob/83f22dec2bcf6ec13a4c6863ea7c2e642b870045/example.py#L71) of the same video and later select the best one.

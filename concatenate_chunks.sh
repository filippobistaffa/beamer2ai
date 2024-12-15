#!/bin/bash

ffmpeg -y -f concat -safe 0 -i chunk_list.txt -c copy es_concatenated.mp4

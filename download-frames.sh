#!/bin/sh

pip install --upgrade youtube-dl

# Temporary workaround.
pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"

sudo apt update
sudo apt install -y ffmpeg

mkdir assets
cd assets

VIDEO="https://www.youtube.com/watch?v=FtutLA63Cp8"
FILE_NAME="bad-apple.mp4"
OUTPUT_DIGITS="4"
OUTPUT_FPS="30"
OUTPUT_DIMENSIONS="178x128"

youtube-dl -f mp4 -o $FILE_NAME $VIDEO

mkdir frames
cd frames

ffmpeg -r $OUTPUT_FPS -i ../$FILE_NAME -s $OUTPUT_DIMENSIONS -vf format=gray "frame%0${OUTPUT_DIGITS}d.png"

cd ..
mkdir audio
cd audio

# ffmpeg -i ../$FILE_NAME -vn bad-apple-audio.mp3
# ffmpeg -i ../$FILE_NAME -vn bad-apple-audio.ogg
ffmpeg -i ../$FILE_NAME -vn bad-apple-audio.wav

rm ../$FILE_NAME

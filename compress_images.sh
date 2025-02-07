#!/bin/sh
set -xe

mkdir build || true

for image in ./images/*.bmp
do
    base="$(basename "$image" .bmp)"
    for quality in 25 50 75
    do
        compressed_image=./build/"$base-q$quality.jpg"
        (set -x; ffmpeg -loglevel quiet -y -i "$image" -q:v "$quality" "$compressed_image")
    done
done

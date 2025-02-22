#!/bin/sh
set -e

for script in \
  ./src/step0_preprocessing.py \
  ./src/step1_color_space_conversion.py
do
  (
    set -x
    python "$script"
  )
done

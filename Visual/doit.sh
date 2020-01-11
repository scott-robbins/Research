#!/bin/sh
python video_stylist.py -run
ffmpeg -r 25 -i results/img%03d.png -vf fps=35 -pix_fmt yuv420p stylized_treflip.mp4
#EOF


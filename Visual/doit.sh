#!/bin/sh
python video_stylist.py -run
ffmpeg -r 15 -i Images/img%03d.png -vf fps=13 -pix_fmt yuv420p stylized_hardflip.mp4
#EOF


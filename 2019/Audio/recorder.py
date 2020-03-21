import os

rec_cmd = 'echo "enter filename: ";read fname; sox -t alsa default $fname'
os.system(rec_cmd)

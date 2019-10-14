from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
import os
tic = time.time()

base_cmd = 'ffmpeg -loglevel quiet -i '
extract_frame_cmd = ' -vf fps=2 Images/img%03d.jpg -hide_banner'
pack_vid_cmd = 'ffmpeg -r 1/5 -i Images/img%03d.png -c:v libx264 -vf fps=3 -pix_fmt yuv420p '  # out.mp4
'''
[1] Extract Images from Video
[2] Iterate through Each image and apply style transfer to each frame
[3] Reassemble stylized frames into an output video. 
'''

if '-vi' in sys.argv and len(sys.argv) >=3:
    video_in = sys.argv[2]
    if os.path.isdir('Images/'):
        extraction = base_cmd + video_in + extract_frame_cmd
    else:
        extraction = 'mkdir Images;'+base_cmd + video_in + extract_frame_cmd
    os.system(extraction)

if '-cut' in sys.argv and len(sys.argv) >= 4:
    video_in = sys.argv[2]
    start = sys.argv[3]
    duration = sys.argv[4]
    try:
        file_out = video_in.split('.')[0] + 'cutfile.' + video_in.split('.')[1]
    except IndexError:
        print 'Something Went Wrong!'
        exit()
    ''' snipping: ffmpeg -i <input.mp4> -c copy -ss 00:00:08 -t 00:00:10 <output.mp4>'''
    snip = 'ffmpeg -i '+video_in + ' -c copy -ss ' + start + ' -t '+duration + ' ' + file_out
    os.system(snip)

if '-frame' in sys.argv and len(sys.argv) >= 3:
    img_name = sys.argv[2]
    frame = np.array(plt.imread(img_name))
    width = frame.shape[0]
    height = frame.shape[1]
    print '%s is [%s x %s]' % (img_name,width,height)

if '-styled' in sys.argv and len(sys.argv) >= 3:
    img_name = sys.argv[2]
    cmd = 'ls results/*00.png | while read n; do rm $n; mv results/results.png %s; rm %s' %\
          (img_name.split('.')[0]+'.png;done', img_name)
    print cmd
    os.system(cmd)

if '-run' in sys.argv:
    ''' Use -vi option to extract a video into still frames '''
    run_cmd_base = 'ls Frames/img*.png| while read n; do ' \
                   'python ex.py -do $n Seeds/lateralus_slice.jpg;' \
                   'python video_stylist.py -styled $n; done'
    os.system(run_cmd_base)
    ''' Now Reassamble into stylized video'''
    #recombine = pack_vid_cmd+'stylized.mp4'
    #os.system(recombine)
    ''' Look at the Training Graphs'''
    #os.system('tensorboard --logdir logs')
    ''' clean up'''
    # rm_imgs = 'ls *.jpg | while read n; do rm $n; done'
if 'ani' in sys.argv:
    f = plt.figure()
    reel = []
    frame_nums = []
    for img in os.listdir('Frames/'):
        frame_nums.append(int(img.split('img')[1].split('.')[0]))
    frame_nums = np.array(frame_nums)
    frame_nums.sort()
    for ii in frame_nums:
        frame = 'Frames/img%03d.png' % ii
        state = np.array(plt.imread(frame))
        reel.append([plt.imshow(state)])
    a = animation.ArtistAnimation(f,reel,interval=180,blit=True,repeat_delay=900)
    w = FFMpegWriter(fps=5, bitrate=1800)
    a.save('stylized_kickflip.mp4', writer=w)
    plt.show()
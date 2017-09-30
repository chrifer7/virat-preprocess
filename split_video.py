import csv
import glob
import os
import os.path
from subprocess import call


base_path = '/media/grupoavatar/DATOS/VIRAT/VIRAT_Video_Dataset_Release_1.0/Sample_Dataset/'
annotations_path = base_path+'annotations/'
video_path = base_path+'videos/'
video_name = 'VIRAT_S_050203_09_001960_002083'


vfile = open(annotations_path+video_name+'.viratdata.events.txt', 'r')

i = 0
for line in vfile:
    vdata = line.split(' ')
    print ('Event: ', vdata[1])
    call(["ffmpeg", "-i", video_path+video_name+'.mp4', video_path+video_name+'_frames'+'-%04d.jpg'])
    i = i + 1






import sys
import os
import os.path
import re
import csv
import glob
import datetime
import subprocess
from subprocess import call

_base_path = '/media/grupoavatar/DATOS/VIRAT/VIRAT_Video_Dataset_Release_1.0/Sample_Dataset/'
_annotations_path = _base_path + 'annotations/'
_video_path = _base_path + 'videos/'
_video_name = 'VIRAT_S_050203_09_001960_002083'


def get_path_and_file(data_arg):
    _path = ''
    _file = ''
    path_splitted = data_arg.split('/')
    _len = len(path_splitted)
    if _len > 1:
        _path = '/'.join(path_splitted[0:(_len - 1)])
        _file = path_splitted[_len - 1]
    elif _len == 1:
        _file = path_splitted[_len - 1]

    # print('_path', _path, '_file', _file)

    return _path, _file


if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print('Arguments must match:\npython code/split_video.py <video_path> <annotations_path>')
        sys.exit(2)
    else:
        video_arg = sys.argv[1]
        annotation_arg = sys.argv[2]

        # print('video_arg: ', video_arg, 'annotation_arg: ', annotation_arg)

        video_path, video_file = get_path_and_file(video_arg)
        video_file_len = len(video_file.split('.'))
        video_name = video_file.split('.')[video_file_len - 2]
        annotation_path, annotation_file = get_path_and_file(annotation_arg)

        vfile = open(annotation_arg, 'r')

        #https://askubuntu.com/questions/110264/how-to-find-frames-per-second-of-any-video-file
        #fps = call(['ffmpeg -i "' + video_arg + '" 2>&1 | sed -n "s/.*, \(.*\) fp.*/\\1/p"'])

        #pattern = re.compile(r'(\d{2}.\d{3}) fps')
        #mplayerOutput = subprocess.Popen(("mplayer", "-identify", "-frames", "0", "o-ao", "null", video_arg),
        #                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        #fps = pattern.search(mplayerOutput).groups()[0]

        fps = -1
        out = subprocess.check_output(["ffprobe", video_arg, "-v", "0", "-select_streams", "v", "-print_format", "flat", "-show_entries",
             "stream=r_frame_rate"])
        #b'streams.stream.0.r_frame_rate="30000/1001"\n'
        rate = str(out).split('=')[1].strip()[1:-4].split('/')
        print ('rate: ', rate)
        if len(rate) == 1:
            fps = float(rate[0])
        if len(rate) == 2:
            fps = float(rate[0]) / float(rate[1])

        print('fps: ', fps)

        i = 0
        for line in vfile:
            vdata = line.split(' ')
            start_time = a = str(datetime.timedelta(seconds=int(int(vdata[3]) / fps)))

            print('Event: ', vdata[1], '\nstart: ', start_time, '\nframes: ', vdata[2])

            video_path_frames = video_path + '/' + vdata[0] + '-' + vdata[1] + '-' + video_name

            # print('Video: ', video_arg, ' Frames: ', video_path_frames)
            if not os.path.exists(video_path_frames):
                os.makedirs(video_path_frames)

            call(["ffmpeg", "-i", video_arg, '-ss', start_time, '-vframes', vdata[2],
                  video_path_frames + '/' + video_name + '_frames' + '-%06d.jpg'])
            i = i + 1





def _old_main():
    vfile = open(_annotations_path + video_name + '.viratdata.events.txt', 'r')

    i = 0
    for line in vfile:
        vdata = line.split(' ')
        print('Event: ', vdata[1])
        video_path_frames = video_path + video_name + '/' + video_name
        if not os.path.exists(video_path_frames):
            os.makedirs(video_path_frames)
        call(["ffmpeg", "-i", video_path + video_name + '.mp4', video_path_framesgit + '_frames' + '-%04d.jpg'])
        i = i + 1

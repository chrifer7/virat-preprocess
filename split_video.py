import sys
import os
import os.path
import csv
import glob
import datetime
from subprocess import call


_base_path = '/media/grupoavatar/DATOS/VIRAT/VIRAT_Video_Dataset_Release_1.0/Sample_Dataset/'
_annotations_path = _base_path+'annotations/'
_video_path = _base_path+'videos/'
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
		
	#print('_path', _path, '_file', _file)
		
	return _path,  _file
	
if __name__ == '__main__':
	if not len(sys.argv) == 3:
		print('Arguments must match:\npython code/split_vode.py <video_path> <annotations_path>')
		sys.exit(2)
	else:
		video_arg = sys.argv[1]
		annotation_arg = sys.argv[2]
		
		#print('video_arg: ', video_arg, 'annotation_arg: ', annotation_arg)

		video_path, video_file = get_path_and_file(video_arg)
		video_file_len = len(video_file.split('.'))
		video_name = video_file.split('.')[video_file_len - 2]
		annotation_path, annotation_file = get_path_and_file(annotation_arg)

		vfile = open(annotation_arg, 'r')
		
		i = 0
		for line in vfile:
			vdata = line.split(' ')			
			start_time = a = str(datetime.timedelta(seconds=int(int(vdata[2]) / 24)))
			
			print ('Event: ', vdata[1], '\nstart: ', start_time, '\nframes: ', vdata[3])
			
			video_path_frames = video_path+'/'+vdata[1]+video_name
			
			#print('Video: ', video_arg, ' Frames: ', video_path_frames)
			if not os.path.exists(video_path_frames):
				  os.makedirs(video_path_frames)
			
			call(["ffmpeg", "-i", video_arg, '-ss', start_time, '-vframes', vdata[3], video_path_frames+'/'+video_name+'_frames'+'-%06d.jpg'])
			i = i + 1









def _old_main():	  
	vfile = open(annotations_path+video_name+'.viratdata.events.txt', 'r')

	i = 0
	for line in vfile:
		vdata = line.split(' ')
		print ('Event: ', vdata[1])
		video_path_frames = video_path+video_name+'/'+video_name
		if not os.path.exists(video_path_frames):
				os.makedirs(video_path_frames)
		call(["ffmpeg", "-i", video_path+video_name+'.mp4', video_path_framesgit +'_frames'+'-%04d.jpg'])
		i = i + 1

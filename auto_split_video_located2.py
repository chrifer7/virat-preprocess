import sys
import os
import os.path
import re
import csv
import glob
import datetime
import subprocess
from subprocess import call

from tqdm import tqdm
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

'''
Extrae los eventos de cada video en forma de frames de acuerdo a las anotaciones realizadas
Y al área demarcada por la acción (un rectángulo de resolución menor a la del frame)
Crea carpetas con los nombres de los videos y los frames cropeados dentro
'''

#_base_path = '/media/grupoavatar/DATOS/VIRAT/VIRAT_Video_Dataset_Release_1.0/Sample_Dataset/'
#_annotations_path = _base_path + 'annotations/'
#_video_path = _base_path + 'videos/'
#_video_name = 'VIRAT_S_050203_09_001960_002083'


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

def split_and_save(video_arg, annotation_arg, crop_frames, draw_rectangle):
    # print('video_arg: ', video_arg, 'annotation_arg: ', annotation_arg)

    video_path, video_file = get_path_and_file(video_arg)
    video_file_len = len(video_file.split('.'))
    video_name = video_file.split('.')[video_file_len - 2]
    annotation_path, annotation_file = get_path_and_file(annotation_arg)

    vfile = open(annotation_arg, 'r')

    # https://askubuntu.com/questions/110264/how-to-find-frames-per-second-of-any-video-file
    # fps = call(['ffmpeg -i "' + video_arg + '" 2>&1 | sed -n "s/.*, \(.*\) fp.*/\\1/p"'])

    # pattern = re.compile(r'(\d{2}.\d{3}) fps')
    # mplayerOutput = subprocess.Popen(("mplayer", "-identify", "-frames", "0", "o-ao", "null", video_arg),
    #                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    # fps = pattern.search(mplayerOutput).groups()[0]

    # Imprime los detalles del video
    fps = -1
    out = subprocess.check_output(
        ["ffprobe", video_arg, "-v", "0", "-select_streams", "v", "-print_format", "flat", "-show_entries",
         "stream=r_frame_rate"])
    # b'streams.stream.0.r_frame_rate="30000/1001"\n'
    rate = str(out).split('=')[1].strip()[1:-4].split('/')
    #print('rate: ', rate)
    if len(rate) == 1:
        fps = float(rate[0])
    if len(rate) == 2:
        fps = float(rate[0]) / float(rate[1])

    #print('fps: ', fps)

    # Se crea la carpeta para los frames globales del video
    video_global_frames = video_path + '/' + video_name + '/' + 'FRAMES-' + video_name
    if not os.path.exists(video_global_frames):
        os.makedirs(video_global_frames)

    # Extrae todos los frames del video en una carpeta global para dicho video
    call(["ffmpeg", "-i", video_arg, video_global_frames + '/' + video_name + '_frame-%d' + '.jpg'])

    #pbar = tqdm(total=len(vfile))

    pbar = tqdm(vfile)

    i = 0
    event_id = -1
    #for line in vfile:
    for line in pbar:

        # Dado que las anotaciones están realizadas a razón de un frame por cada línea (curr_frame)
        # trato cada frame de forma independiente
        vdata = line.split(' ')
        # if vdata[0] != event_id:
        event_id = vdata[0]

        start_time = a = str(datetime.timedelta(seconds=int(int(vdata[3]) / fps)))

        # Imprimo info extra
        #print('Event: ', vdata[1], '\nstart: ', start_time, '\nframes: ', vdata[2])

        # Creo la carpeta para el evento en particular
        video_path_frames = video_path + '/' + video_name + '/' + vdata[0] + '-' + vdata[1] + '-' + video_name

        # print('Video: ', video_arg, ' Frames: ', video_path_frames)
        if not os.path.exists(video_path_frames):
            os.makedirs(video_path_frames)

        # call(["ffmpeg", "-i", video_arg, '-ss', start_time, '-vframes', str(1), #only 1 frame
        #    video_path_frames + '/' + video_name + '_frames_' + vdata[5] + '.jpg'])
        i = i + 1

        # Obtengo el frame en cuestión de la carpeta global del video
        source_img = None
        try:
            source_img = Image.open(video_global_frames + '/' + video_name + '_frame-' + vdata[5] + '.jpg').convert("RGB")
        except Exception:
            continue

        if (crop_frames):
            # Grabo el frame con el rectángulo cropeado en la carpeta del evento
            source_img.crop((int(vdata[6]), int(vdata[7]), (int(vdata[6]) + int(vdata[8])),
                            (int(vdata[7]) + int(vdata[9]))))\
                            .save(video_path_frames + '/' + video_name + 
                            '_frame-' + vdata[5] + '.jpg', "JPEG")
                            
        elif (draw_rectangle):
            # dibujo un rectágulo alrededor del frame
            draw = ImageDraw.Draw(source_img)
            # draw.rectangle(((int(vdata[8]), int(vdata[9])), (int(vdata[6]), int(vdata[7]))), fill=None)
            draw.rectangle(
                ((int(vdata[6]), int(vdata[7])), (int(vdata[6]) + int(vdata[8]), int(vdata[7]) + int(vdata[9]))),
                fill=None)

            # Grabo el frame con el rectángulo dibujado en la carpeta global del video
            source_img.save(video_global_frames + '/' + video_name + '_frame-' + vdata[5] + '.jpg', "JPEG")

            # Grabo el frame con el rectángulo dibujado en la carpeta del evento
            source_img.save(video_path_frames + '/' + video_name
                            + '_frame-' + vdata[5] + '.jpg', "JPEG")
                            
        else:
            #No cropeo ni dibujo rectágulo, solo guardo el frame completo
            # Grabo el frame con el rectángulo dibujado en la carpeta del evento
            source_img.save(video_path_frames + '/' + video_name
                            + '_frame-' + vdata[5] + '.jpg', "JPEG")
            

        pbar.set_description("Processing frame %d" % i)
        pbar.update(1)

    pbar.close()


if __name__ == '__main__':
    if not len(sys.argv) >= 3:
        print('Arguments must match:\npython code/auto_split_video_located2.py <videos_path> <annotations_path> OPTIONAL[<crop> <drawrec>]')
        sys.exit(2)
    else:
        video_dir = sys.argv[1]
        annotation_dir = sys.argv[2]
        crop_frames = False
        draw_rectangle = False
        
        for i in range(len(sys.argv)):
            if (i > 3):
                if (sys.argv[i].lower() == 'crop'):
                  crop_frames = True
                if (sys.argv[i].lower() == 'drawrec'):
                  draw_rectangle = True                  

        pbar = tqdm(total=len(next(os.walk(video_dir))[2]))

        files = []
        for filename in os.listdir(video_dir):
            filename_arr = filename.split('.')
            filename_arr = filename_arr[0:len(filename_arr) - 1]
            # filename_arr = filename_arr.append('mp4')
            
            if len(filename_arr) > 0:
              print("filename_arr: "+str(filename_arr))
              # print(filename)
              video_arg = filename
              annotation_arr = [filename_arr[0], 'viratdata', 'events', 'txt']
              # print(annotation_arr)
              annotation_arg = '.'.join(annotation_arr)

              video_arg = video_dir + '/' + video_arg
              annotation_arg = annotation_dir + '/' + annotation_arg

              print('video_arg: ', video_arg, 'annotation_arg: ', annotation_arg)

              if (os.path.isfile(video_arg) and os.path.isfile(annotation_arg)):
                  pbar.update(1)
                  split_and_save(video_arg, annotation_arg, crop_frames, draw_rectangle)

              # print('video_arg: ', video_arg, 'annotation_arg: ', annotation_arg)

        pbar.close()

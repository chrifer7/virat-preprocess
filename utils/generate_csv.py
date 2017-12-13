"""
==========================
Annotation Files
==========================

Annotations files include three types of annotations per clip
1) Event file (selected events annotated)
2) Mapping file (from event to object)
3) Object file (all objects annotated)

The detailed formats of the above three types of (linked) files are described below.


1) Event file format

Files are named as '%s.viratdata.events.txt' where %s is clip id.
Each line in event file captures information about a bounding box of an event at the corresponding frame

Event File Columns
1: event ID        (unique identifier per event within a clip, same eid can exist on different clips)
2: event type      (event type)
3: duration        (event duration in frames)
4: start frame     (start frame of the event)
5: end frame       (end frame of the event)
6: current frame   (current frame number)
7: bbox lefttop x  (horizontal x coordinate of left top of bbox, origin is lefttop of the frame)
8: bbox lefttop y  (vertical y coordinate of left top of bbox, origin is lefttop of the frame)
9: bbox width      (horizontal width of the bbox)
10: bbox height    (vertical height of the bbox)

Event Type ID (for column 2 above)
1: Person loading an Object to a Vehicle
2: Person Unloading an Object from a Car/Vehicle
3: Person Opening a Vehicle/Car Trunk
4: Person Closing a Vehicle/Car Trunk
5: Person getting into a Vehicle
6: Person getting out of a Vehicle
7: Person gesturing
8: Person digging
9: Person carrying an object
10: Person running
11: Person entering a facility
12: Person exiting a facility
"""

import sys
import os
import shutil

from tqdm import tqdm

number_of_categories = 0
array_of_categories = [0] * 13 # Cantidad de tipos eventos (no considero el cero) --por mejorar
array_of_name_categories = ["",
                            "1: Person loading an Object to a Vehicle",
                            "2: Person Unloading an Object from a Car/Vehicle",
                            "3: Person Opening a Vehicle/Car Trunk",
                            "4: Person Closing a Vehicle/Car Trunk",
                            "5: Person getting into a Vehicle",
                            "6: Person getting out of a Vehicle",
                            "7: Person gesturing",
                            "8: Person digging",
                            "9: Person carrying an object",
                            "10: Person running",
                            "11: Person entering a facility",
                            "12: Person exiting a facility"
                            ]

if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print('Falta la ruta de los archivos')
        sys.exit(2)
    else:
        video_dir = sys.argv[1]
        
        list_csv = []

        pbar_video_dir = tqdm(total=len(os.listdir(video_dir)))
        pbar_video_dir.set_description("\nGenerando CSV\n")

        for cat_id in os.listdir(video_dir):
            pbar_video_dir.update(1)
            #print (filename)
            #pbar_video_dir_names = tqdm(total=len(os.listdir(video_dir)))
            #pbar_video_dir_names.set_description("\nMoviendo carpetas de video de: %s\n" % (dir_name))
            for video_dir_name in os.listdir(os.path.join(video_dir,cat_id)):
                n_frames = len(os.listdir(os.path.join(video_dir,cat_id,video_dir_name)))
                list_csv.append(','.join(['train', cat_id, video_dir_name, n_frames, os.path.join(video_dir,cat_id,video_dir_name)]))

            #pbar_video_dir_names.close()
        pbar_video_dir.close()
        
        

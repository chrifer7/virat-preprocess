
import sys
import os
import shutil

import cv2
import numpy as np

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
        dest_dir = sys.argv[2]

        pbar_video_dir = tqdm(total=len(os.listdir(video_dir)))
        pbar_video_dir.set_description("\nMoviendo directorios de: %s\n" % (video_dir))

        #por cada categoría
        for dir_name in os.listdir(video_dir):
            pbar_video_dir.update(1)
            
            if not os.path.exists(os.path.join(dest_dir,dir_name)):
                '''Creo el directorio de la categoría'''
                os.makedirs(os.path.join(dest_dir,dir_name))

                print("Directorio creado:\n\t", os.path.join(dest_dir,dir_name))

            #por cada muestra en la categoría
            for video_dir_name in os.listdir(os.path.join(video_dir,dir_name)):
                
                dest_video_cat_dir = os.path.join(dest_dir,dir_name,video_dir_name)
                if not os.path.exists(dest_video_cat_dir):
                    '''Creo el directorio'''
                    os.makedirs(dest_video_cat_dir)
                    
                    print("Directorio creado:\n\t", dest_video_cat_dir)
               
                source_path = os.path.join(video_dir, dir_name, video_dir_name)
                dest_path = dest_video_cat_dir#os.path.join(dest_video_cat_dir, video_dir_name)

                #print('source_path: ', source_path)
                #print('dest_path: ', dest_path)

                if os.path.exists(dest_path):
                    #debo hacerlo un archivo a la vez
                    i = 0

                    for video_frame in os.listdir(source_path):
                        source_path_file = os.path.join(source_path, video_frame)
                        dest_path_file = os.path.join(dest_path, video_frame)

                        ''' OPTICAL FLOW '''

                        frame = cv2.imread(video_frame)
                        prvs = None
                        hsv = None

                        #El primer frame será el prev frame
                        if (i == 0):
                            prvs = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                            hsv = np.zeros_like(frame)
                            hsv[...,1] = 255

                        #El primer frame se calcula sobre sí mismo
                        next = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

                        flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

                        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
                        hsv[...,0] = ang*180/np.pi/2
                        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
                        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

                        #cv2.imwrite('flow/f_'+str(i)+'_opticalfb.png',frame)
                        #cv2.imwrite('flow/f_'+str(i)+'_opticalhsv.png',rgb)

                        cv2.imwrite(dest_path_file, rgb)

                        i = i + 1
        pbar_video_dir.close()


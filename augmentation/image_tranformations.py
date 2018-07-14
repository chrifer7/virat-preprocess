"""
==========================
Objetivo
==========================

"""
import random
import sys
import os
import shutil

import math
from tqdm import tqdm

number_of_categories = 0
array_of_categories = [0] * 13  # Cantidad de tipos eventos (no considero el cero) --por mejorar
array_of_full_name_categories = ["",
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
array_of_name_categories = ["",
                            "LoadingObjectToVehicle",
                            "UnloadingObjectFromVehicle",
                            "OpeningVehicleCarTrunk",
                            "ClosingVehicleCarTrunk",
                            "GettingIntoVehicle",
                            "GettingOutOfVehicle",
                            "Gesturing",
                            "Digging",
                            "CarryingObject",
                            "Running",
                            "EnteringFacility",
                            "ExitingFacility"
                            ]

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print('Falta la ruta de los archivos y el ratio de muestras para entrenamiento')
        sys.exit(2)
    else:
        video_dir = sys.argv[1]

        pbar_video_dir = tqdm(total=len(os.listdir(video_dir)))
        pbar_video_dir.set_description("\nGenerando data aumentada\n")

        # Para cada carpeta que contiene las muestras de una categoría
        for cat_id in os.listdir(video_dir):
            pbar_video_dir.update(1)
            # print (filename)
            # pbar_video_dir_names = tqdm(total=len(os.listdir(video_dir)))
            # pbar_video_dir_names.set_description("\nMoviendo carpetas de video de: %s\n" % (dir_name))

            # Cantidad de video para distribuir entre las carpetas de train y test
            video_list_dir = os.listdir(os.path.join(video_dir, cat_id))
            n_samples = len(video_list_dir)

            n_train_samples = int(math.ceil(train_ratio * float(n_samples)))
            n_test_samples = n_samples - n_train_samples

            # print('\nn_train_samples: '+str(n_train_samples))
            # print('n_test_samples: '+str(n_test_samples))

            group_sample = 'train'
            i = 0
            random.shuffle(video_list_dir)
            for video_dir_name in video_list_dir:
                n_frames = len(os.listdir(os.path.join(video_dir, cat_id, video_dir_name)))

                # list_csv.append(','.join([group_sample, array_of_name_categories[int(cat_id)], video_dir_name, str(n_frames), os.path.join(video_dir,cat_id,video_dir_name)]))
                list_csv.append(','.join(
                    [group_sample, cat_id, video_dir_name, str(n_frames),
                     os.path.join(video_dir, cat_id, video_dir_name)]))

                i = i + 1

                if i >= n_train_samples:
                    group_sample = 'test'

                    # pbar_video_dir_names.close()
        pbar_video_dir.close()

        file_csv = open('virat_complete.csv', 'w')
        file_csv.write("\n".join(list_csv))


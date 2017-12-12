import sys
import os
import shutil

number_of_categories = 0
array_of_categories = [0] * 15

if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print('Falta la ruta de los archivos')
        sys.exit(2)
    else:
        video_dir = sys.argv[1]
        dest_dir = sys.argv[2]
        for dir_name in os.listdir(video_dir):
            #print (filename)
            for video_dir_name in os.listdir(os.path.join(video_dir,dir_name)):
                #print(video_dir_name)
                video_cat = video_dir_name.split('-')
                #print(video_cat[1])
                dest_video_cat_dir = os.path.join(dest_dir,video_cat[1])
                if not os.path.exists(dest_video_cat_dir):
                    os.makedirs(dest_video_cat_dir)
                    number_of_categories = number_of_categories + 1
                    print(dest_video_cat_dir)
                array_of_categories[int(video_cat[1])] = array_of_categories[int(video_cat[1])] + 1
                shutil.move(os.path.join(video_dir, dir_name, video_dir_name), dest_video_cat_dir)

        print (array_of_categories)

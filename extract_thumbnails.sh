#ffmpeg -ss 01:23:45 -i input -vframes 1 -q:v 2 output.jpg

#for i in *.avi; do ffmpeg -i "$i" "${i%.*}.mp4"; done

for i in *.avi; do ffmpeg -ss 00:00:05 -i "$i" -vframes 1 -q:v 2 "/home/grupoavatar/thumbs/${i%.*}.jpg"; done

# virat-preprocess

1. Extract the frames from videos according to the event annotation files (virat-preprocess/auto_split_video_located.py or auto_split_video_located2.py)
2. Distribute the frames extracted in folders per every category (virat-preprocess/utils/categorize_videos.py)
3. Generate CSV file with data (virat-preprocess/utils/generate_csv.py)
4. Subsample the frames until get 40 frames per action sequence and Extract features from frames (extract_features_virat_cropped.py) -- No se consideran lo videos  de menos de 40 frames
5. Train the model
6. Test

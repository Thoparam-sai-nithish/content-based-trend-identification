import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
tf.get_logger().setLevel('ERROR')
# Disable TensorFlow eager execution
tf.compat.v1.disable_eager_execution()

import preprocessAudio
from videoToAudio import convertVideoToWav
from spleeter.separator import Separator
from speechToText import batchSpeechToText
import shutil
import time

def main():
    video_dir = 'videos'
    raw_audio_dir = 'rawAudio'
    spleetered_audio_dir = 'spleeteredAudio'
    text_dir = "textFiles"
    convertVideoToWav(video_dir, raw_audio_dir)
    print()
    # Create a common separator
    separator = Separator('spleeter:2stems')


    raw_files = os.listdir(raw_audio_dir)
    for file_name in raw_files:
        try:
            preprocessAudio.preprocess(raw_audio_dir, spleetered_audio_dir, file_name, separator)

            os.makedirs(spleetered_audio_dir, exist_ok=True)

            batchSpeechToText(spleetered_audio_dir, text_dir, file_name)

            time.sleep(1)
            shutil.rmtree(spleetered_audio_dir)
            print(f"🚮  Deleted Directory: {spleetered_audio_dir} for {file_name}")

        except Exception as e:
            print(print(f"❌ Error processing file {file_name}: {e}"))

        print()

if __name__ == "__main__":
    main()
    if tf.executing_eagerly():
        tf.keras.backend.clear_session()
import os
import tensorflow as tf
import preprocessAudio
from videoToAudio import convertVideoToWav
from spleeter.separator import Separator
from faster_whisper import WhisperModel
from speechToText import batchSpeechToText
import shutil
import time

# Optimize TensorFlow for Colab
tf.config.optimizer.set_jit(True)

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    print(f"Using GPU: {physical_devices[0]}")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

def main():
    video_dir = 'videos'
    raw_audio_dir = 'rawAudio'
    spleetered_audio_dir = 'spleeteredAudio'
    text_dir = "textFiles"
    convertVideoToWav(video_dir, raw_audio_dir)
    print()
    # Create a common separator
    separator = Separator('spleeter:5stems')
    # Create a common STT model
    stt_model = WhisperModel("large-v3", device="cuda", compute_type="float16")

    raw_files = os.listdir(raw_audio_dir)
    for file_name in raw_files:
        try:
            preprocessAudio.preprocess(raw_audio_dir, spleetered_audio_dir, file_name, separator)

            os.makedirs(spleetered_audio_dir, exist_ok=True)

            batchSpeechToText(spleetered_audio_dir, text_dir, file_name, stt_model)

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
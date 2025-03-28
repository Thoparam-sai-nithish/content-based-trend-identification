import os
from utils import rmRecur
import preprocessAudio
from spleeter.separator import Separator
import tensorflow as tf
from speechToText import batchSpeechToText
from videoToAudio import convertVideoToWav
from languageTranslator import translate_text_files
from ldaAnalyser import lda_analyser

# AVOID CUDA WARNINGS
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# DISABLE EAGER EXECUTION
tf.get_logger().setLevel('ERROR')
tf.compat.v1.disable_eager_execution()


def main():
    video_dir = 'videos'
    raw_audio_dir = 'rawAudio'
    spleetered_audio_dir = 'spleeteredAudio'
    text_dir = "textFiles"
    convertVideoToWav(video_dir, raw_audio_dir)
    print()

    # Create a common separator
    separator = Separator('spleeter:2stems')

    # Create a common STT model
    # stt_model = WhisperModel("large-v2", device="cpu", compute_type="int8")
    stt_model = "stt_model"

    raw_files = os.listdir(raw_audio_dir)
    for file_name in raw_files:
        try:
            preprocessAudio.preprocess(raw_audio_dir, spleetered_audio_dir, file_name, separator)

            os.makedirs(spleetered_audio_dir, exist_ok=True)

            batchSpeechToText(spleetered_audio_dir, text_dir, file_name, stt_model)

            rmRecur(spleetered_audio_dir)

        except Exception as e:
            print(print(f"❌ Error processing file {file_name}: {e}"))

        print()
    translate_text_files('textFiles', 'translatedFiles')
    print(lda_analyser('translatedFiles'))


if __name__ == "__main__":
    main()
    if tf.executing_eagerly():
        tf.keras.backend.clear_session()
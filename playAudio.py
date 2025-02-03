import soundfile as sf
import sounddevice as sd


def play(file_path):
    data, sr = sf.read(file_path)
    print(f"Playing Audio {file_path}")
    sd.play(data, sr)
    sd.wait()

if __name__ == "__main__":
    print("Play Audio Main Function")
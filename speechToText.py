import os 

def convertToText(input_file_path, output_file_path, stt_model):
    if not os.path.exists(input_file_path):
        print(f"⚠️  Skipping: {input_file_path} (File not found)")
        return
    
    try:
        print(f"⛏️  Extracting text from {input_file_path}...")
        # stt_model = WhisperModel("large", device="cpu", compute_type="int8")

        segments, info = stt_model.transcribe(input_file_path)
        
        text = " ".join(segment.text for segment in segments).strip()
        # print(f"Text : \n{text}")

        if not text:
            print(f"⚠️  No speech detected in {input_file_path}")
            return

        with open(output_file_path, "a", encoding="utf-8") as f:
            f.write(text + "\n")
            print(f"✅  Text appended to {output_file_path}")

    except Exception as e:
        print(f"❌  Error processing {input_file_path}: {e}")


def batchSpeechToText(input_dir, output_dir, base_file_name, stt_model):
    print(f"🔠 Converting {base_file_name} chunks into text")

    if not os.path.exists(input_dir):
        print(f"❌  Directory '{input_dir}' does not exists")
        return

    os.makedirs(output_dir, exist_ok=True)
    output_file_name = os.path.splitext(base_file_name)[0]+'.txt'
    output_file_path = os.path.join(output_dir, output_file_name)

    with open(output_file_path, "w", encoding="utf-8") as f:
        print(f"📝 Created a empty file at {output_file_path}")
 
    chunks_dirs_list = os.listdir(input_dir)
    print(f"📂 Spleetered chunks found: {chunks_dirs_list}")

    for chunk_dir in chunks_dirs_list:
        input_file_path = os.path.join(input_dir, chunk_dir,"vocals.wav")
        convertToText(input_file_path,  output_file_path,stt_model)


if __name__ == "__main__":
    batchSpeechToText("spleeteredAudio", "textFiles", "alalundani.wav")
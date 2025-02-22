import os
from deep_translator import GoogleTranslator

def translate_text_files(input_folder, output_folder):
    translator = GoogleTranslator(source='auto', target='en')  # Auto-detect source language
    
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            with open(input_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            try:
                translated_text = translator.translate(text)
            except Exception as e:
                print(f"Error translating {filename}: {e}")
                translated_text = text  # Fallback to original text
            
            with open(output_path, 'a', encoding='utf-8') as file:
                file.write(translated_text)
            
            print(f'🔤  Translated {filename} and saved to {output_path}')
    
    print('Translation completed!')

# Define input and output folder paths
input_folder = "textFiles"
output_folder = "translatedFiles"

# Run the translation function
translate_text_files(input_folder, output_folder)

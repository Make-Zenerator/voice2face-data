import os
import librosa
import noisereduce as nr
from spleeter.separator import Separator
from pydub import AudioSegment
from pydub.effects import normalize
import tempfile

def process_audio(input_file, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Step 1: Separate vocals from the rest
    separator = Separator('spleeter:2stems')
    with tempfile.TemporaryDirectory() as temp_dir:
        separator.separate_to_file(input_file, temp_dir)
        vocal_path = os.path.join(temp_dir, 'input_audio', 'vocals.wav')
        
        # Step 2: Reduce noise
        y, sr = librosa.load(vocal_path, sr=None)
        reduced_noise = nr.reduce_noise(y=y, sr=sr)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_vocal_file:
            cleaned_vocal_path = temp_vocal_file.name
            librosa.output.write_wav(cleaned_vocal_path, reduced_noise, sr)
        
        # Step 3: Amplify audio
        audio = AudioSegment.from_file(cleaned_vocal_path)
        normalized_audio = normalize(audio)
        final_output_path = os.path.join(output_dir, 'final_output.wav')
        normalized_audio.export(final_output_path, format="wav")
        
        # Clean up the temporary vocal file
        os.remove(cleaned_vocal_path)
    
    return final_output_path
from vosk import Model, KaldiRecognizer
import wave
import json
import ffmpeg
from django.core.files.uploadedfile import UploadedFile
import tempfile

def get_transcription(audio_file: UploadedFile) -> list:
    '''
        Given a audio file, get the transcription
    '''

    '''
        Convert audio file to WAV (PCM 16 Khz, Mono)
        Transcribe
        Return info        
    '''

    # Convert audio file to a format compatible with Vosk

    with (        
          tempfile.NamedTemporaryFile(suffix='.wav') as temp_in
        , tempfile.NamedTemporaryFile(suffix='.wav') as temp_out):

        if hasattr(audio_file, 'temporary_file_path'):
            input_path = audio_file.temporary_file_path()
        else:
            temp_in.write(audio_file.read())
            temp_in.seek(0)
            input_path = temp_in.name

        
        (
            ffmpeg
            .input(input_path)
            .output(temp_out.name, **{'ac': 1, 'ar': 16000})
            .run(overwrite_output=True, quiet=True)
        )

        with wave.open(temp_out.name, 'rb') as wave_file:
            model = Model(lang='es') # TODO: Allow user select the language model. If application have success..
            recognizer = KaldiRecognizer(model, wave_file.getframerate())

            transcription = []

            while True:
                data = wave_file.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    transcription.append(json.loads(recognizer.Result()))
            
            transcription.append(json.loads(recognizer.FinalResult()))

    return transcription
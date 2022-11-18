import torch
import librosa
import numpy as np
import soundfile as sf
import moviepy.editor as mp
from scipy.io import wavfile
from IPython.display import Audio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from translate import Translator



def toText(filename):
    transcription = "did you say somethin?" 
    translation = []
    UPLOAD_FOLDER = './uploads/'
    audioFile = UPLOAD_FOLDER + filename[:-4] + ".wav"

    tokenizer = Wav2Vec2Tokenizer.from_pretrained('./preTrainedWeithts' ) # use_auth_token=True
    model = Wav2Vec2ForCTC.from_pretrained("./preTrainedWeithts")

    print("\n\n", audioFile, "\n\n")

    data = wavfile.read(audioFile)
    framerate = data[0]
    sounddata = data[1]
    time = np.arange(0,len(sounddata))/framerate
    input_audio, _ = librosa.load(audioFile, sr=16000)
    input_values = tokenizer(input_audio, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    print(transcription)

    transcription = transcription.replace("<s>", "")
    print("\n", transcription)
    # transcription.replace("<", "&lt")
    # transcription.replace(">", "&gt")
    # transcription = "<pre>" + transcription + "<\pre><br><br>" + transcription

    try:
        translator= Translator(from_lang="hindi",to_lang="english")
        # translation = translator.translate(transcription)
        words = transcription.split()
        for word in words:
            translation.append(translator.translate(word)) 
        toReturn = transcription + "\n\n" + translation
    except:
        print("\n\ntranslation failed, words aren't recognized", translation)
        toReturn = transcription + """
        <br><div style="color: red;">TRANSLATION FAILED, WORDS AREN'T RECOGNIZED.</div> 
        <br><br>I think this might have been what you said and I know I am completely wrong:<br><b>
        """ + " ".join(x for x in translation)

    return toReturn


    # creating a EngtoHindi() object
    res = EngtoHindi(transcription)

    # displaying the translation
    print(res.convert)

    return transcription + "<br>" +  res
# toText("audio2.wav")
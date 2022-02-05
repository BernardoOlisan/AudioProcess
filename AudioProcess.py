'''
# Some wav files are stereo so we convert them to mono
from pydub import AudioSegment
import glob
import os

me = [f for f in glob.glob(os.path.abspath(r"Voiceclassification/DataCopia/otherCopia")+"/*", recursive=True) if not os.path.isdir(f)]

num = 0
for path in me:
	num += 1
	src = str(path)
	dst = str(path)
	sound = AudioSegment.from_wav(src)
	sound = sound.set_channels(1)
	sound.export(dst, format="wav")
	print(f"{num} done:)")
'''


# Audio processing for removing the silence and noise, prevent overfitting
from pydub import AudioSegment
from pydub.playback import play
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
import glob
import wave
import os

print("[INFO] Removing silence from wav files")
audiofiles = [f for f in glob.glob(os.path.abspath(r"Data/me")+"/*", recursive=True) if not os.path.isdir(f)]

num = 0

for audio in audiofiles:

	num += 1
	print(f"[INFO] wav file number {num}--------------------------------------------------------")

	# Chunk files
	print(f"[INFO] Creating Chunks for {audio} ")
	myaudio = AudioSegment.from_file(audio, "wav")
	from pydub.utils import make_chunks

	chunk_length_ms = 100 
	chunks = make_chunks(myaudio, chunk_length_ms) 

	for i, chunk in enumerate(chunks):
		chunk_name = os.path.abspath("Chunks/chunk{0}.wav".format(i))
		print("exporting", chunk_name)
		chunk.export(chunk_name, format="wav")


	# Get the amplitud 
	print("-----------------------------")
	print(f"[INFO] Deleting the chunks in silence")
	chunkfiles = [f for f in glob.glob(os.path.abspath(r"Chunks")+"/*", recursive=True) if not os.path.isdir(f)]

	for chunk in chunkfiles:

		samplerate, data = read(chunk)

		amplitud = max(data)
		print(amplitud)

		if amplitud < 1500:
			os.remove(chunk)
			print(f"{chunk} has been remove")


	print("-----------------------------")
	print(f"[INFO] Joining all the left chunks into the real audio")
	chunks = glob.glob(os.path.abspath("Chunks/*.wav"))

	infiles = [i for i in chunks]
	outfile = audio

	data= []
	for infile in infiles:
		w = wave.open(infile, 'rb')
		data.append( [w.getparams(), w.readframes(w.getnframes())] )
		w.close()
		
	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])
	for i in range(len(data)):
		output.writeframes(data[i][1])
	output.close()

	print(f"[INFO] Complete {audio}")
	print(f"[INFO] Done :)")




	''' PLOT all the audios

	samplerate, data = read(audio)
	print(f"rate: {samplerate}")

	duration = len(data)/samplerate
	time = np.arange(0, duration, 1/samplerate)

	plt.plot(time, data)
	plt.xlabel("Time [s]")
	plt.ylabel("Amplitud")
	plt.title(audio)
	plt.show()

	playaudio = AudioSegment.from_file(audio, format="wav")
	play(playaudio)

	plt.close()

	'''















import os
import pandas as pd
import json, asyncio
import nltk
from datetime import datetime
from dotenv import load_dotenv

from deepgram import Deepgram
from nltk.tokenize.treebank import TreebankWordDetokenizer

load_dotenv()

pathfile = str(input("Enter the pathfile to the audio here (ONLY MP3): \n"))
fileType = pathfile[-4:] # Gets .mp3
fileName = pathfile[:-5] # Gets the name of the file without the .mp3

if ((fileType.lower() != ".mp3")):
    print("Only MP3 files are allowed. Please enter a valid audio file and try again.")
    quit()

speaker_name = str(input("Enter the name of the speaker: \n"))
section = "Q_AND_A"

DEEPGRAM_API_KEY = 'ddabd865a664dcc14f0f5f7adf3822359044eba1' #os.getenv("DEEPGRAM_API_KEY")

try:
    FILE = pathfile
    MIMETYPE = 'audio/{}'.format(fileType) #mp3
except:
    FILE = str(input("Drag the audio file or enter its pathname: \n"))
    MIMETYPE = 'audio/{}'.format(fileType) #mp3


data = ""
async def main():
    try:
        global data
        # Initialize the Deepgram SDK
        deepgram = Deepgram(DEEPGRAM_API_KEY)

        options = { "punctuate": True, "model": "finance", "tier":"enhanced", "language": "en", "diarize":True }

        # Check whether requested file is local or remote, and prepare source
        if FILE.startswith('http'):
            # file is remote
            # Set the source
            source = {
            'url': FILE
            }
        else:
            # file is local
            # Open the audio file
            audio = open(FILE, 'rb')

            # Set the source
            source = {
            'buffer': audio,
            'mimetype': MIMETYPE
            }

        # Send the audio to Deepgram and get the response
        response = await asyncio.create_task(
            deepgram.transcription.prerecorded(
            source,options
            )
        )

        print(json.dumps(response['results']['channels'][0]['alternatives'][0]['words'], indent=4))

        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
        transcript = transcript.replace("...",".")
        transcript = transcript.replace("?",".")
        transcript = transcript.replace(",","")

        print(transcript)

        sentences = nltk.sent_tokenize(transcript)
        print(sentences)

        data = response['results']['channels'][0]['alternatives'][0]['words']

        speaker_list = []
        sentence_start_time = {}
        sentence_end_time = {}
        start_processed_words = set()
        end_processed_words = set()
        for sentence in sentences:
            sentence_words = sentence.split()
            if len(sentence_words) != 1:
                start_time = None
                end_time = None
                for word_data in data:
                    print(word_data['word'].upper()+ str(word_data["start"]))
                    if (word_data['word'].upper()+ str(word_data["start"])) in start_processed_words:
                        continue
                    start_processed_words.add(word_data['word'].upper() + str(word_data["start"]))
                    if word_data['word'].upper() == sentence_words[0].upper():
                        start_time = word_data["start"]
                        speaker_list.append(word_data['speaker'])
                        sentence_start_time[sentence] = (start_time)
                        break

                for word_data in data:
                    print(word_data['word'].upper() + str(word_data["end"]))
                    if (word_data['word'].upper() + str(word_data["end"])) in end_processed_words:
                        continue
                    end_processed_words.add(word_data['word'].upper() + str(word_data["end"]))
                    word = word_data['word'] + "."
                    print(word.upper())
                    print(sentence_words[-1].upper())
                    print('------------------')
                    if word.upper() == sentence_words[-1].upper():
                        end_time = word_data["end"]
                        if len(sentence) != 1:
                            sentence_end_time[sentence] = (end_time)
                            speaker_list.append(word_data['speaker'])
                        else:
                            pass
                        break
            else:
                pass

        df = pd.DataFrame([sentence_start_time, sentence_end_time])
        df = df.transpose()
        df = df.reset_index(inplace=False)
        column_list = ["statement","start", "stop"]
        df.columns = column_list


        df.insert(loc = 0,
            column = "speaker",
            value = [speaker_name] * len(df['statement'])
        )

        df.insert(loc = 1,
                column = "section",
                value = [section] * len(df['statement'])
                )

        df.insert(loc = 3,
                column = "type",
                value = [""] * len(df['statement'])
                )

        df = df.reset_index(inplace=False)

        data = df

        print(data)
        return data
    except Exception as e:
        print("An error with Deepgram's API was encountered. Please check your network or try again later")
        #print("Error: {}".format(str(e)))
        quit()

print(asyncio.run(main()))
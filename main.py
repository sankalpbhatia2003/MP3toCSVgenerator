import pandas as pd
import json, asyncio
import nltk
from datetime import datetime

from deepgram import Deepgram
from nltk.tokenize.treebank import TreebankWordDetokenizer

#section = str(input("What type of 'section' is the interview? Choose from: Q_AND_A or PREPARED_REMARKS: \n"))
section = 'Q_and_A'

DEEPGRAM_API_KEY = 'ddabd865a664dcc14f0f5f7adf3822359044eba1' # Add your Deepgram's API key here
try:
    FILE = ''  #Add your MP3 file here
    MIMETYPE = 'audio/mp3' #wav
except:
    FILE = str(input("Drag the audio file or enter its pathname: \n"))
    MIMETYPE = 'audio/mp3' #mp3

async def main():
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

    #print(response['results']['channels'][0]['alternatives'][0]['words'])

    print(json.dumps(response['results']['channels'][0]['alternatives'][0]['words'], indent=4))

    transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
    transcript = transcript.replace("...",".")
    transcript = transcript.replace("?",".")
    transcript = transcript.replace(",","")

    print(transcript)


    # Split the paragraph into sentences
    #def split_into_sentences(paragraph):
    sentences = nltk.sent_tokenize(transcript)
    print(sentences)

    # Map words to sentences and create new timestamps
    #def map_words_to_sentences(sentences, json_response):

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
                #print(word_data['word'])
                #print(sentence_words[0])
                #print(sentence_words[-1])
                if word_data['word'].upper() == sentence_words[0].upper():
                    #print(word_data['word'])
                    #print(word_data['start'])
                    #print('')
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
                    #print(word_data['word'])
                    #print(sentence_words[-1])
                    #print('')
                    end_time = word_data["end"]
                    if len(sentence) != 1:
                        sentence_end_time[sentence] = (end_time)
                        speaker_list.append(word_data['speaker'])
                    else:
                        pass
                    break
        else:
            pass

    print(sentence_start_time)
    print(sentence_end_time)
    print('')

    df = pd.DataFrame([sentence_start_time, sentence_end_time])
    df = df.transpose()
    df = df.reset_index(inplace=False)
    column_list = ['statement','start', 'stop']
    df.columns = column_list


    df.insert(loc = 0,
          column = 'speaker',
          value = [""] * len(df['statement'])
    )

    df.insert(loc = 1,
            column = 'section',
            value = [section] * len(df['statement'])
            )

    df.insert(loc = 3,
            column = 'type',
            value = [""] * len(df['statement'])
            )

    print(df)
    df.to_csv('example.csv') # Change the name of your CSV here

    json_data = df.to_json(orient='index')
    json_data = json.loads(json_data)

    print(json_data)



print(asyncio.run(main()))

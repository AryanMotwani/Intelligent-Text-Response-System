import nltk
import numpy as np
import tflearn
import tensorflow
import random
import pickle
import re
from nltk.stem.lancaster import LancasterStemmer
import classes_dict
import pyttsx3
import datetime
import speech_recognition as sr
import sys
import webbrowser
from googlesearch import search
from summarize import text_summarize
from text_generator import generate
import time
from learn_from_user import chat_bot   
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

def websearch(user_input):
    query = user_input.replace('google','')
    websites=[]

    time.sleep(2)

    for i in search(query, tld="com", num=3, stop=3, pause=2):
        websites.append(i)

    return webbrowser.open(websites[0])


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
       speak("Good Morning!")
    
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
   
    else:
        speak("Good Evening!")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        #print(e)
        print("Say that again please...")
        return "None"
    return query

stemmer = LancasterStemmer()

from classes_dict import *

my_words = []
my_classes = []
my_doc = []
ignore_words = ['?']

# pre-process text from classes_dict
for some_class in classes_dict:

    my_classes.append(some_class)

    for some_pattern in classes_dict[some_class]["pattern"]:

        temp_words = []

        raw_words = some_pattern
        word_tokens = nltk.word_tokenize(raw_words)

        for some_word in word_tokens:
            if some_word not in ignore_words:
                stemmed_word = stemmer.stem(some_word.lower())
                my_words.append(stemmed_word)
                temp_words.append(stemmed_word)

        my_doc.append((temp_words, some_class))

my_words = sorted(list(set(my_words)))  # remove duplicate words
my_classes = sorted(list(set(my_classes)))

training = []
output = []
output_empty = [0] * len(my_classes)

for some_doc in my_doc:

    bag = []
    pattern_words = some_doc[0]

    # create bag of words array
    for some_word in my_words:
        bag.append(1) if some_word in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[my_classes.index(some_doc[1])] = 1

    combined_row = bag + output_row  # Combine bag and output_row into a single list
    training.append(combined_row)

# shuffle training data and put into array
random.shuffle(training)
training = np.array(training)

# create train lists
train_x = list(training[:, :len(my_words)])
train_y = list(training[:, len(my_words):])

# build nn model
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

def tokenize_input(sentence):
    sentence_words = nltk.word_tokenize(sentence)  # tokenize pattern
    for some_word in sentence_words:
        sentence_words[sentence_words.index(some_word)] = stemmer.stem(some_word.lower())
    return sentence_words

def bag(user_input):
    input_words = tokenize_input(user_input)
    bag = [0] * len(my_words)
    for input_word in input_words:
        for i in range(0, len(my_words)):
            if input_word == my_words[i]:
                bag[i] = 1
    return np.array(bag)

def bot_response(user_input):
    matched_responses = ''

    for key, value in classes_dict.items():
        for pattern in value["pattern"]:
            if re.search(pattern, user_input):
                matched_responses += random.choice(value["response"])
                matched_responses+=' '
                #matched_responses.extend(value["response"])

    if matched_responses:
        print(matched_responses)
        # rand=random.choice(matched_responses)
        # print(rand)
        return speak(matched_responses)
        # return matched_responses
    else:
        # print("No Suggestion")
        # return speak("No Suggestion")
        return chat_bot(user_input)

def accuracy_predictor(): 
    nb_samples = 1000
    x, y = make_classification(n_samples=nb_samples, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1)
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(xtrain, ytrain)
    print("Accuracy: ", accuracy_score(ytest, model.predict(xtest)))
    speak("The accuracy of the program is: ")
    speak(accuracy_score(ytest, model.predict(xtest)))

def accuracy_predict(user_input):
    matched_responses = ''

    for key, value in classes_dict.items():
        for pattern in value["pattern"]:
            if re.search(pattern, user_input):
                matched_responses += random.choice(value["response"])
                matched_responses+=' '
                #matched_responses.extend(value["response"])

    return  matched_responses


error_threshold = 0.95

def response(user_input):
    if "google" in user_input:
        #summary = text_summarize(user_input)
        summary = generate(user_input)
        websearch(user_input)
        speak(summary)
        #webbrowser.open("https://google.com/search?q=" + user_input)
        #break
    elif "youtube" in user_input:
        webbrowser.open("https://youtube.com/search?q=" + user_input)
        #break
    
    elif "stop" in user_input:
        accuracy_predictor()
        sys.exit()
    else:
        if user_input != "none":
            bot_response(user_input)

def main():
    wishMe()
    print("Welcome to Intelligent Text Response System. How may I help you?")
    speak("Welcome to Intelligent Text Response System. How may I help you?")
    while True:
        user_input = takeCommand().lower()  # get input and convert to lowercase
        response(user_input)

if __name__ == "__main__":
    main()

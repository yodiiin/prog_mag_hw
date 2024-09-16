'''test texts:
1. Автоматическое распознавание речи (ASR) — это программное обеспечение, которое позволяет компьютерной системе преобразовывать человеческую речь в текст, используя несколько алгоритмов искусственного интеллекта и машинного обучения.
2. O eclipse solar de 8 de abril de 2024 foi um eclipse solar total, que foi visto em toda América do Norte é apelidado como o Grande Eclipse da América do Norte por alguns meios de comunicação.
'''

import speech_recognition as sr
from gtts import gTTS
import os
import random
from deep_translator import GoogleTranslator
from difflib import SequenceMatcher


# функция для воспроизведения речи
def speak(text, lang='pt-BR'):
    tts = gTTS(text=text, lang=lang)
    filename = 'assistant.mp3'
    tts.save(filename)
    os.system('start ' + filename) # проигрывает звуковой файл


# функция для прослушивания и обработки речи
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        text = ''
        try:
            text = r.recognize_google(audio, language='pt-BR')
        except sr.UnknownValueError:
            speak('Repita mais uma vez, por favor.')
            print('Repita mais uma vez, por favor...')
    return text


# функция для перевода
def translate(text):
    translator = GoogleTranslator(source='ru', target='pt')
    translation = translator.translate(text)
    return translation


# функция для сравнения произнесенного текста с правильным
def comparing_texts(text1, text2):
    matching = SequenceMatcher(None, text1, text2)
    similarity = matching.ratio()
    return similarity


# основная функция — взаимодействие с голосовым помощником
def assistant():
    while True:
        command = listen()
        if 'pare' in command: # стоп
            break
        elif 'traduza' in command: # переведи
            speak('Por favor, digite o texto que você deseja traduzir.')
            user_text = input('Digite o texto: ')
            translation = translate(user_text)
            print(f'Aqui está a tradução: {translation}')
            speak(translation)
        elif 'leia em voz alta' in command: # прочитай вслух
            speak('Por favor, digite o texto que você deseja que eu leia em voz alta.')
            user_text = input('Digite o texto em português: ')
            speak(user_text)
        elif 'praticar' in command: # практиковаться
            text = random.choice(texts)
            speak('Por favor, leia o seguinte texto em voz alta')
            print(f'Leia em voz alta: {text}')
            user_text = listen()
            similarity = comparing_texts(text, user_text)
            if similarity > 0.85:
                speak('Ótimo! Você leu o texto corretamente.')
                print('Ótimo!')
            else:
                speak('Há alguns erros. Continue praticando!')
                print('Tem erros :(')
        elif 'texto' in command:
            speak('Por favor, digite o texto que você deseja adicionar na base dos textos')
            text = input('Digite o texto para adicionar: ')
            texts.append(text)
            speak('Que bom! Vamos praticar!')
    print('Tchau!')
    speak('Está bem, até à próxima. Tenha um bom dia.')

texts = [
    'Olá, como está? Estou bem, e você?', 
    'Eu estou aprendendo português há cinco anos.', 
    'Tenho vinte e três anos.', 
    'Sou da Rússia.', 
    'Eu tenho muitos amigos.', 
    'Ultimamente eu tenho praticado programação em Python.'
    ]

assistant()
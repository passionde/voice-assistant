import random

import speech_recognition as sr
import pyttsx3

import commands


class Assistant:
    def __init__(self, commands: dict[str: tuple]):
        self.voice_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.__make_commands(commands)

    def speak(self, message: str):
        self.voice_engine.say(message)
        self.voice_engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            return text
        except sr.UnknownValueError:
            return "unknown"
        except sr.RequestError:
            return "error"

    def extract_command(self, text: str):
        # ToDo: Здесь можно подкрутить ИИ для определения команды или более совершенный алгоритм
        text = text.strip().lower()
        command = self.commands.get(text, None)
        if command:
            return command

        # Попытка найти перебором
        for k, v in self.commands.items():
            if k in text:
                return v

    def handle_command(self, command):
        if command is None:
            return

        if command == "hello":
            self.__hello_cmd()
        elif command == "error":
            self.__error_cmd()
        else:
            self.__unknown_cmd()

    def handle_one_command(self):
        text = self.listen()
        cmd = self.extract_command(text)
        self.handle_command(cmd)

    def run(self):
        while True:
            print("Слушаю команду...")

            text = self.listen()
            cmd = self.extract_command(text)

            print(f"Распознана команда /{cmd}")
            self.handle_command(cmd)

    def __make_commands(self, _commands: dict[str: tuple]):
        self.commands = {}
        for k, v_arr in _commands.items():
            k = k.lower()
            for v in v_arr:
                self.commands[v.lower()] = k

    def __hello_cmd(self):
        self.speak(random.choice([
            'и тебе привет', 'привет', 'приветсвую', 'снова здесь', 'рада видеть', 'давно не виделись',
            'не скучала,но привет', 'здравствуйте, сударыня', "новый рабочий день", 'привет от старых штиблет',
            'моя радость умирает от твоего прихода'
        ]))

    def __unknown_cmd(self):
        self.speak(random.choice([
            "я тебя не понимаю", "говори четче", "не расслышала"
        ]))

    def __error_cmd(self):
        self.speak(random.choice([
            "ууупс, кажется произошла ошибка", "видимо потеряно соединение с сервером"
        ]))


if __name__ == "__main__":
    assistant = Assistant(commands.commands)
    assistant.run()
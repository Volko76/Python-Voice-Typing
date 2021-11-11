import speech_recognition as sr
import random
import time
import pynput
import configparser
import os
import ast
from pynput.keyboard import Key, Controller
keyboard = Controller()
r = sr.Recognizer()
mic = sr.Microphone()
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# instantiate
config = ConfigParser()

# parse existing file
config.read('assignements.ini')

justWrite = ast.literal_eval(config.get("KEYWORDS", "just_words"))
print(justWrite[1])
defaults_actions = ast.literal_eval(config.get("KEYWORDS", "defaults_words"))
WORDS = []
WORDS.extend(list(justWrite))
for i in defaults_actions.keys():
    WORDS.append(str(i))
print("keywords = ", WORDS)
print("Specific ations can only be edit in the code (and also added to the just_words section)")
print("Please restart to apply changes")


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def ask():
    while 1:
        guess = recognize_speech_from_mic(sr.Recognizer(), sr.Microphone())
        if guess["transcription"]:
            print("Validated")

            break
        if not guess["success"]:
            break
        print("I didn't catch that. What did you say?\n")

    # if there was an error, stop the game
    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))

    # show the user the transcription
    print("You said: {}".format(guess["transcription"]))
    return guess


def actions(word):

    # for specific tasks
    if (word.lower() == "for" or word.lower() == "four"):
        print("select variable")
        i = str(ask()["transcription"])
        print("select range")
        range = str(ask()["transcription"])
        keyboard.type("for {} in range({})".format(i, range))
    elif (word.lower() == "create a variable"):
        print("select name of the variable")
        name = str(ask()["transcription"])
        print("select value")
        value = str(ask()["transcription"]).replace("\'", "\\'").replace("\"", "\\"")
        if (type(value) == "str"):
            value = "{}".format(value)
        elif (type(value) == ""):
            value = "{}".format(value)
        keyboard.type("{} = {}".format(name, value))
    elif (word.lower() == "launch browser"):
        os.startfile("C:\\Users\\volko\\AppData\\Local\\Programs\\Opera GX\\opera.exe")
    elif (word.lower() == "launch discord" or word.lower() == "launch discount"):
        os.startfile(
            "C:\\Users\\volko\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc\\Discord.lnk")
    else:
        for justword in justWrite:
            if justword == word:
                keyboard.type(justword)

        for defaults_words in defaults_actions:
            if defaults_words == word:
                keyboard.type(defaults_actions[defaults_words])


if __name__ == "__main__":

    time.sleep(1)

    while 1:
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        # for j in range(PROMPT_LIMIT):

        guess = ask()
        if guess["transcription"].lower() in WORDS:
            print("Finded in database")
            actions(guess["transcription"].lower())

        #
        # # determine if guess is correct and if any attempts remain
        # for word in WORDS:
        #     if (guess["transcription"].lower() == word.lower()):
        #         print("Finded in database")
        #         actions()
        #         break
        #

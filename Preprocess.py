
import re

file = open("resources/stop-words.txt", "r")
stop_words = file.read().split()


def remove_stop_words(words):
    return [word for word in words if word not in stop_words and re.sub("\s|\u200c", "", word).isalnum()]

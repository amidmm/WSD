
import re
from Utility import read_file

stop_words = read_file("resources/stop-words.txt").split()

'''and re.sub("\s|\u200c", "", word).isalnum()'''
def remove_stop_words(words):
    return [word for word in words if word not in stop_words]

from hazm import POSTagger, Normalizer, Stemmer

tagger = POSTagger(model='resources/postagger.model')
normalizer = Normalizer()
stemmer = Stemmer()


def read_file(path):
    """Reads content of the file in path"""
    file = open(path, "r")
    return file.read()


def write_file(path, content, append=False):
    """Writes content to the file in path"""
    f_file = open(path, '+w')
    f_file.writelines(content)
    f_file.close()



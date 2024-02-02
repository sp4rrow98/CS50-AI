import math
import string
import os
import sys
import nltk
nltk.download('stopwords')


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # Get path and filenames
    path_files = os.path.join(os.getcwd(), directory)
    filenames = os.listdir(path_files)

    # Create dictionary
    dictionary = {}

    # Add file's contents as a string
    for file in filenames:
        with open(os.path.join(path_files, file), 'r', encoding='utf-8') as f:
            content = f.read()
            dictionary[file] = content

    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Tokenize string in order and lowercased
    tokenised = nltk.word_tokenize(document.lower())

    # Filter out punctuation and stopwords
    for c in tokenised:
        if c in string.punctuation or c in nltk.corpus.stopwords.words("english") and not c.isdigit():
            tokenised.remove(c)

    # Return list
    return tokenised


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # V1 -----------------------
    # Get text from documents
    values = list(documents.values())
    text = ''
    for value in values:
        text += ' '.join(value)
    text = set(text.split())

    # Count in how many documents does the word appear
    words = {word: 0 for word in text}
    for document in documents.values():
        wordz = set(document)
        for word in wordz:
            if word in words:
                words[word] = words[word] + 1
                break

    # Calculate IDF
    for key, value in words.items():
        words[key] = math.log(len(documents) / words[key]
                              ) if words[key] != 0 else math.log(len(documents) / 1)

    # print(sorted(words.items(), key=lambda x: x[1], reverse=False))

    # Return dictionary
    return words


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # n can not be greater than the total number of files
    if n > len(files):
        raise ValueError("n is greater than the total number of files")

    # Initialise dictionary to map words inside each file
    tf_idf = {}

    # Count words in documents
    for file, text in files.items():
        words = {}
        for word in text:

            # Add idf value
            if word in query:
                words[word] = words.get(word, 0) + 1 * idfs[word]

        # Add dictionary
        tf_idf[file] = sum(words.values())

    # Rank dictionary
    tf_idf = list(sorted(tf_idf.keys(), key= lambda k: tf_idf[k], reverse=True))[0:n]
    # print(tf_idf)

    # Return list
    return tf_idf


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Sentences rank dictionary
    sentences_rank = {}
    
    # Add idf for each query
    for sentence in sentences:
        count_idf = 0
        count_words = 0
        for word in query:
            if not word in idfs:
                continue
            if word in sentence.lower():
                count_idf += idfs[word]
                count_words += 1
        
        count = [count_idf, count_words]

        
        # Add sentence count to dictionary
        sentences_rank[sentence] = count

    # Sort sentences
    sentences_rank = dict(sorted(sentences_rank.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True))

    # Return list
    sentences = list(sentences_rank.keys())
    return sentences[0:n]




    # for key in sentences
        



if __name__ == "__main__":
    main()

import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""


NONTERMINALS = """
S -> NP VP | S Conj S | VP Det NP | VP NP | 
NP -> N | P N | Det N | Det N VP | Det N NP 
NP -> NP AdvP NP | PP NP Adv | N NP | N V Adv | P Det Adj N 
NP -> NP AdvP
NP -> NP PP
VP -> V | V NP | V PP | V AP | V AdvP | V Det 
AP -> Det Adj NP | Adj NP | P Det Adj NP | Det Adj Adj Adj 
AP -> Det Adj Adj Adj NP 
AdvP -> Adv VP | Adv |
PP -> P Det Adj NP | P Det | Det NP | P Det NP Det NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
        # tree.draw()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Get the sentence in lowercased and without punctuation
    new_sentence = ""
    for letter in sentence.lower():

        if letter.isalpha() or letter == " ":
            new_sentence += letter

    # Perform tokenization
    nltk.download('punkt')
    s = nltk.word_tokenize(new_sentence)

    # Return new sentence
    return s

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Create list
    list = []

    # Loop in the subtrees
    for sub in tree.subtrees():

        # Check if subtree has another NP subtree
        label = sub.label()
        if label == "NP":

            # Check the subtrees of the subtree
            for t in sub.subtrees():
                if t.label() == "NP":
                    pass
                else:
                    list.append(sub)

    return list



if __name__ == "__main__":
    main()

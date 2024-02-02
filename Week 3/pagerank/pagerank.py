import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # For example, if the corpus were {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, the page was "1.html", and the damping_factor was 0.85, then the output of transition_model should be {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}

    values = {}  # Dict to return

    pages_in_page = corpus[page]  # Get the pages from the current one

    if not pages_in_page:  # If the page has no links
        for link in corpus.keys():
            # Spread the posibility evenly
            values[link] = 1 / len(corpus.keys())
    else:
        links = corpus[page]  # Get page links
        # Distribute the dumping_factor for links
        for link in links:
            # Add initial values for the pages in page
            values[link] = damping_factor / len(links)
        
        length = len(corpus.keys())
        rest = (1 - damping_factor) / length
        total = 0

        for link in corpus.keys():  # Update values for pages
            if link in values:
                values[link] = float(values[link] + rest)
            else:
                values[link] = rest
            total += values[link] # Keep track of total
            

        # Adjust the sum to exactly 1
        # rounding = 1 - total
        # if rounding != 0:
        #     left = rounding / len(corpus.keys())
        #     for link in corpus.keys():
        #         values[link] += left
    return (values)


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialise copy for corpus to track samples and set values to 0
    copy_corpus = corpus.copy()
    for page in copy_corpus:
        copy_corpus[page] = 0

    # Get samples
    for i in range(n):
        # Generate random first sample
        if i == 0:
            sample = random.choice(list(copy_corpus.keys()))

        # Generate Chances to pick a page from the page
        model = transition_model(corpus, sample, damping_factor)
        # Make a choice
        choice = random.choices(list(model.keys()), weights=(model.values()))
        # Add sample to values
        copy_corpus[sample] += 1
        # Go to the next sample
        sample = choice[0]

    # Generate chance
    for page in copy_corpus:
        copy_corpus[page] /= n

    return copy_corpus


def iterate_pagerank(corpus, damping_factor):
    N = len(corpus)
    values = {page: 1 / N for page in corpus}  # Initialize all PageRank values equally
    new_values = values.copy()

    converged = False
    while not converged: # Loop until we converge
        for page in corpus:
            contribution_sum = 0
            for link in corpus:
                if page in corpus[link]: # If page is a link in other pages
                    contribution_sum += values[link] / len(corpus[link])
            
            new_value = (1 - damping_factor) / N + damping_factor * contribution_sum # Formula
            new_values[page] = new_value

        # Check for convergence
        converged = True
        for page in corpus:
            if abs(new_values[page] - values[page]) > 0.001:
                converged = False
                break
        
        # Update values for the next iteration
        values = new_values.copy()

    # Normalize PageRank values
    total = sum(values.values())
    return {page: rank / total for page, rank in values.items()}


if __name__ == "__main__":
    main()

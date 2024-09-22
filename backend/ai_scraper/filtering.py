from bs4 import BeautifulSoup, Comment
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def prune_dom(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Remove comments
    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove attributes except 'class' and 'id'
    for tag in soup.recursiveChildGenerator():
        if hasattr(tag, "attrs"):
            tag.attrs = {
                key: value for key, value in tag.attrs.items() if key in ["class", "id"]
            }

    # Remove empty tags
    for element in soup(
        lambda tag: len(tag.get_text(strip=True)) == 0 and len(tag.find_all()) == 0
    ):
        element.decompose()

    return str(soup)


def clean_class_name(class_name):
    # Remove common prefixes/suffixes and split into words
    words = re.findall(r"[a-z]+", class_name.lower())
    return " ".join(words)


def extract_relevant_dom(html, context_query, performance):
    top_n = 3 + performance  # This will give a range of 4 to 7
    max_depth = 4 + performance  # This will give a range of 5 to 8

    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all()

    class_names = [clean_class_name(" ".join(elem.get("class", []))) for elem in tags]

    if len(class_names) < top_n:
        print(f"Warning: Not enough tags ({len(tags)}) to match requested performance. Adjusting top_n.")
        top_n = len(tags)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(class_names + [context_query])

    cosine_similarities = cosine_similarity(
        tfidf_matrix[-1], tfidf_matrix[:-1]
    ).flatten()

    top_indices = cosine_similarities.argsort()[-top_n:][::-1]

    relevant_dom_sections = []
    seen_structures = set()

    for idx in top_indices:
        element = tags[idx]
        html = str(element)

        # Create a simplified representation of the element structure
        structure = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()

        # If we've seen this structure before, skip it
        if structure in seen_structures:
            continue
        seen_structures.add(structure)

        element_soup = BeautifulSoup(html, "html.parser")
        limited_soup = limit_depth(element_soup, max_depth)

        relevant_dom_sections.append(
            {
                "similarity": cosine_similarities[idx],
                "class": " ".join(element.get("class", [])),
                "html": str(limited_soup),
            }
        )

    return relevant_dom_sections


def limit_depth(soup, max_depth):
    def recursive_limit(tag, current_depth):
        if current_depth >= max_depth:
            tag.clear()
        else:
            for child in tag.children:
                if child.name:
                    recursive_limit(child, current_depth + 1)

    for tag in soup.children:
        if tag.name:
            recursive_limit(tag, 0)
    return soup

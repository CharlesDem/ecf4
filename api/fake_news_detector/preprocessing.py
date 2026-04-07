import re
from typing import Optional

try:
    import nltk
    from nltk.corpus import stopwords
except Exception:
    nltk = None
    stopwords = None


CONTRACTIONS: dict[str, str] = {
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "can't": "cannot",
    "couldn't": "could not",
    "won't": "will not",
    "wouldn't": "would not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "had'nt": "had not",
    "i'm": "i am",
    "you're": "you are",
    "we're": "we are",
    "they're": "they are",
    "he's": "he is",
    "she's": "she is",
    "it's": "it is",
    "i've": "i have",
    "you've": "you have",
    "we've": "we have",
    "they've": "they have",
    "i'll": "i will",
    "you'll": "you will",
    "we'll": "we will",
    "they'll": "they will",
    "that's": "that is",
    "there's": "there is",
    "what's": "what is",
    "who's": "who is",
    "let's": "let us",
}

NEGATION_WORDS: set[str] = {"not", "no", "never", "neither"}
_EN_STOPWORDS: Optional[set[str]] = None


def _get_stopwords() -> set[str]:
    global _EN_STOPWORDS
    if _EN_STOPWORDS is not None:
        return _EN_STOPWORDS

    words: set[str] = set()
    if stopwords is not None:
        try:
            words = set(stopwords.words("english"))
        except LookupError:
            if nltk is not None:
                try:
                    nltk.download("stopwords", quiet=True)
                except Exception:
                    pass
            try:
                words = set(stopwords.words("english"))
            except Exception:
                words = set()
        except Exception:
            words = set()

    _EN_STOPWORDS = words - NEGATION_WORDS
    return _EN_STOPWORDS


def expand_contractions(text: str) -> str:
    value = text.replace("\u2019", "'")
    for short, long in CONTRACTIONS.items():
        value = value.replace(short, long)
    return value


def tokenize_text(text: str) -> list[str]:
    return str(text).split()


def clean_text(tokens: list[str]) -> list[str]:
    cleaned_tokens: list[str] = []
    for token in tokens:
        token = str(token).lower()
        token = re.sub(r"<[^>]+>|&[a-zA-Z]+;", "", token)
        if re.search(r"https?://\S+|www\.\S+", token):
            continue
        if token.startswith("@") or token.startswith("#"):
            continue
        token = re.sub(r"[^a-z]", "", token)
        if token:
            cleaned_tokens.append(token)
    return cleaned_tokens


def remove_stopwords_not_negation(tokens: list[str]) -> list[str]:
    stop_words = _get_stopwords()
    if not stop_words:
        return tokens
    return [token for token in tokens if token not in stop_words]


def remove_shorty(tokens: list[str]) -> list[str]:
    return [token for token in tokens if len(token) > 2]


def clean_for_tfidf(text: str) -> str:
    tokens = tokenize_text(expand_contractions(text))
    tokens = clean_text(tokens)
    tokens = remove_stopwords_not_negation(tokens)
    tokens = remove_shorty(tokens)
    return " ".join(tokens)

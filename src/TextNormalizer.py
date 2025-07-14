import re
from matplotlib import style
style.use('ggplot')
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

class TextNormalizer:

    @staticmethod
    def remove_noise(text: str) -> str:
        # Remove noise from text, such as urls, @, #, and punctuation
        text = text.lower()
        text = re.sub(r"https\S+|www\S+httpss\S+", '', text, flags=re.MULTILINE) # Remove Url
        text = re.sub(r"\@w+|\#", '', text) # remove @ and #
        text = re.sub(r"[^\w\s]", '', text) # remove punctuation
        tokens = text.split()
        filtered = [w for w in tokens if not w in stop_words] # remove stopwords

        return " ".join(filtered)

    @staticmethod
    def stem_words(text: str) -> str:
        # Abstract words to their word stem
        stemmer = PorterStemmer()
        words = text.split()
        return " ".join(stemmer.stem(word) for word in words)  # abstract to word stem

    @staticmethod
    def truncate_text(text: str, max_length: int = 512) -> str:
        # Return only first 512 tokens (for emotion analysis model)
        words = text.split()
        return " ".join(words[:max_length])
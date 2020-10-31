import nltk
from googletrans import Translator, constants
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

metin = "seni seviyorum ama sevmiyor gibiyim"

# init the Google API translator
translator = Translator()
# translate a spanish text to english text (by default)
translation = translator.translate(metin,src='tr',dest='en')
metin_eng=translation.text
print(translation.text)
print(sid.polarity_scores(metin_eng))
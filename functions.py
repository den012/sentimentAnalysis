from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from langdetect import detect
from urllib.parse import urlparse
import re
import praw
import os

model_dir = "model"
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

class COLORS:
    GREEN = '\033[92m'
    PURPLE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[96m'
    RESET = '\033[0m'

def clean_text(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text) # no emoji
    text = text.replace(',', '') # no coma

    # Remove URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    text = url_pattern.sub(r'', text)

    # Remove &#x200B;
    text = text.replace('&#x200B;', '')

    # Remove excess newlines
    text = re.sub('\n+', '\n', text)

    return text

def get_sentiment(text):
    # Create the pipeline
    sentiment_classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

    result = sentiment_classifier(text)

    label_mapping = {
        '1 star': 'very sad',
        '2 stars': 'sad',
        '3 stars': 'neutral',
        '4 stars': 'happy',
        '5 stars': 'very happy',
    }

    for item in result:
        item['label'] = label_mapping[item['label']]

    sentiment = result[0]['label']
    return sentiment

def get_language(text):
    language_code = detect(text)
    language_mapping = {
        'en': 'English',
        'ceb': 'Cebuano',
        'sv': 'Swedish',
        'de': 'German',
        'fr': 'French',
        'nl': 'Dutch',
        'ru': 'Russian',
        'it': 'Italian',
        'es': 'Spanish',
        'pl': 'Polish',
        'ro': 'Romanian',
    }
    language = language_mapping.get(language_code, 'Unknown')
    print ("Language detected:" + COLORS.PURPLE + f"{language}" + COLORS.RESET)

def print_logo():
    print("   ___")
    print("  /   \\    " + COLORS.YELLOW + "S" + COLORS.RESET + COLORS.PURPLE + "E" + COLORS.RESET + COLORS.GREEN + "N" + COLORS.RESET + COLORS.RED + "T" + COLORS.RESET + COLORS.PURPLE + "I" + COLORS.RESET + COLORS.YELLOW + "M" + COLORS.RESET + COLORS.GREEN + "E" + COLORS.RESET + COLORS.RED + "N" + COLORS.RESET + COLORS.PURPLE + "T" + COLORS.RESET + " " + COLORS.YELLOW + "A" + COLORS.RESET + COLORS.GREEN + "N" + COLORS.RESET + COLORS.RED + "A" + COLORS.RESET + COLORS.PURPLE + "L" + COLORS.RESET + COLORS.YELLOW + "Y" + COLORS.RESET + COLORS.GREEN + "S" + COLORS.RESET + COLORS.RED + "I" + COLORS.RESET + COLORS.PURPLE + "S" + COLORS.RESET)
    print(" | "+ COLORS.RED + "0 0" + COLORS.RESET + " |          " + COLORS.RED + "V" + COLORS.RESET  + COLORS.BLUE + "1.0" + COLORS.RESET)
    print(" \  ~  / ")
    print("  \___/")
    print("\n")

def get_platform(url):
    result = urlparse(url)
    if 'reddit' in result.netloc:
        return 'reddit'
    else:
        return 'unknown'
    
def get_reddit_post_text(url):
    reddit = praw.Reddit(
        client_id="RpWsV2a_HwBWx4cKb8fR2Q",
        client_secret="Ra1RLllLA0nhQlswqPaNipvZadX5gQ",
        user_agent="LargeFact1813",
    )

    submission = reddit.submission(url=url)

    return submission.title, submission.selftext

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask_repeat_analysis(prompt):
    repeat = input(prompt)
    while repeat not in ["y", "n"]:
        print("Invalid input")
        repeat = input(prompt)
    return repeat
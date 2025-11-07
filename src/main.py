import re
import json

def format_word(word: str, urls: int) -> str:
    if "http" in word or "https" in word or "www" in word:
        urls += 1  
        return word.replace("http://", "").replace("https://", "").replace("www.", "").split('/')[0]
    word = word.lower()
    word = word.strip('\'"')
    word = re.sub(r'[()\?\!\:\.\>\<\-\'\\d]', '', word)
    return word

def find_spam(message: str) -> int:
    score = None
    try:
        with open('bad.json') as f:
            bad_words = json.loads(f.read())
        with open('good.json') as f:
            good_words = json.loads(f.read())
        with open(message, 'r') as f:
            message = f.read()
        with open('spammers_domains.json', 'r') as f:
            spammers_domains = json.loads(f.read())

        urls = 0
        spamicities = []
        for word in message.split():
            try:
                word = format_word(word, urls)
                if word in spammers_domains:
                    return 1
                try:
                    bad_words_chances = bad_words.get(word, 0.01)
                    good_words_chances = good_words.get(word, 0.01)
                    spamicity = bad_words_chances / (good_words_chances + bad_words_chances)
                    spamicities.append(spamicity)
                except KeyError:
                    continue
                    
            except KeyError as e:
                print(f"KeyError: {e}")
                continue
        prd_spamicity_bad = 1
        prd_spamicity_good = 1
        for spamicity in spamicities:
            if spamicity == 0:
                continue
            elif spamicity < 0 or spamicity > 1:
                print(f"Invalid spamicity value: {spamicity}")
                continue
            elif spamicity == 1:
                prd_spamicity_bad *= 0.999
                prd_spamicity_good *= 0.001
            elif spamicity == 0:
                prd_spamicity_bad *= 0.001
                prd_spamicity_good *= 0.999
            else:
                prd_spamicity_good *= (1-spamicity)
                prd_spamicity_bad *= spamicity

        score = prd_spamicity_bad / (prd_spamicity_bad + prd_spamicity_good)

        if urls > 0:
            score += 0.1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return -1

    if score is None:
        return -1
    elif score > 0.9:
        return 1
    else:
        return 0
    





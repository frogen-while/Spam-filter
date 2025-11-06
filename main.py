import re
import json
import os
def formatting(word, urls):
    if "http" in word or "https" in word or "www" in word:
        urls[0] += 1  
        return word.replace("http://", "").replace("https://", "").replace("www.", "").split('/')[0]
    word = word.lower()
    word = word.strip('\'"')
    word = re.sub(r'[()\?\!\:\.\>\<\-\'\\d]', '', word)
    return word

def find_spam(massage):
    try:
        with open('bad.json') as f:
            bad_words = json.loads(f.read())
        with open('good.json') as f:
            good_words = json.loads(f.read())
        with open(massage, 'r') as f:
            massage = f.read()
        with open('spammers_domains.json', 'r') as f:
            spammers_domains = json.loads(f.read())

        urls = [0] 
        spamicities = []
        for word in massage.split():
            try:
                word = formatting(word, urls)
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

        if urls[0] > 0:
            score += 0.1
        return score

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

for i in range(1, len(os.listdir("massages")) + 1):

    score = find_spam(f"massages/msg{i}.txt")
    if score > 0.1005:
        print(score)
        print(f"The file msg{i}.txt is spam")
    else:
        print(score)
        print(f"The file msg{i}.txt is not spam")
    print("-------------------------------------------------\n")







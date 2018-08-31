from collections import defaultdict, deque
import sys

dictionary_file = 'dictionary.txt'
def get_words_and_word_relationships():
    try:
        with open(dictionary_file) as dictionary:
            lexicon = set()
            contextual_slots = defaultdict(list)
            for word in dictionary:
                word = word.rstrip()
                lexicon.add(word)
                for i in range(len(word)):
                    contextual_slots[word[: i], word[i + 1: ]].append(word)
            closest_words = defaultdict(set)
            for slot in contextual_slots:
                for i in range(len(contextual_slots[slot])):
                    for j in range(i + 1, len(contextual_slots[slot])):
                        closest_words[contextual_slots[slot][i]].add(contextual_slots[slot][j])
                        closest_words[contextual_slots[slot][j]].add(contextual_slots[slot][i])
            return lexicon, closest_words
    except FileNotFoundError:
        print(f'Could not open {dictionary_file}. Giving up...')
        sys.exit()

lexicon, closest_words = get_words_and_word_relationships()
print(list(lexicon)[0])
print(closest_words['COLD'])

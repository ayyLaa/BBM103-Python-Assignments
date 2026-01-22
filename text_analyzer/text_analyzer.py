from sys import argv
from collections import Counter
import locale
import re


locale.setlocale(locale.LC_ALL, "en_US")


def number_of_words(text):
    """Calculate number of words in given text. Whole text must be purified from the punctuations (except the ones
       that are in the word itself such as "well-known" "they’re" etc.) and white-spaces.

    Args:
        text (str): Input text to be analyzed.

    Returns:
        list: Words in given text.
    """
    # Remove standalone punctuations and those at the end, preserve ' and - between words
    tokenized_text = re.sub(r"(?<!\w)[^\w\s'-]+|[^\w\s'-]+(?!\w)|(?<=\w)'(?!\w)", "", text)
    words = tokenized_text.split()

    return words


def number_of_sentences(text):
    """Calculate number of sentences in given text. End of the sentence characters can be assumed as ".", "!", "?", or "...".

    Args:
        text (str): Input text to be analyzed.

    Returns:
        int: Number of sentences in given text.
    """
    tokenized_text = []
    # Split text into a list of sentences based on punctuation
    for sentence in re.split(r"(?<=\w|\))(?:\.\.\.|\?|!|\.)|(?<=\w|\))(?:\.\.\.|\?|!|\.)$", text):
        if sentence.strip():
           tokenized_text.append(sentence.strip())

    return len(tokenized_text)


def average_of_words_per_sentence(text):
    """Calculate average number of words per sentence in given text.

    Args:
        text (str): Input text to be analyzed.

    Returns:
        float: Average number of words per sentence in given text.
    """
    words = number_of_words(text)
    sentences = number_of_sentences(text)

    return len(words)/sentences


def number_of_all_characters(text):
    """Calculate number of all characters (including the punctuations
       and the white-space characters) in given text.

    Args:
       text (str): Input text to be analyzed.

    Returns:
       int: Number of all characters in given text.
    """
    i = 0

    for character in text:
        i += 1

    return i


def number_of_all_characters_just_words(text):
    """Calculate number of characters (excluding the punctuations
       and white-spaces) in given text.

    Args:
        text (str): Input text to be analyzed.

    Returns:
        int: Number of all characters excluding the punctuations and white-spaces in given text.
    """
    i = 0
    words=number_of_words(text)

    for word in words:
        for character in word:
            i += 1

    return i


def words_frequency(text):
    """Calculate the frequencies of all words in given text.

    Args:
        text (str): Input text to be analyzed.

    Returns:
        dict: Frequencies of all words in given text.
    """
    text = text.lower()
    words = number_of_words(text)

    # Calculate the number of occurrences of words
    dictionary_of_frequencies = Counter(words)
    for word, frequency in dictionary_of_frequencies.items():
        dictionary_of_frequencies[word] = frequency / len(words)

    return dictionary_of_frequencies


def shortest_word(text):
    """Calculate the shortest word(s) in given text.

    Args:
        text (str): Input text to be analyzed.

    Returns:
        list: Shortest word(s) in given text.
    """
    dictionary_of_frequencies = words_frequency(text)
    list_of_shortest_words = []
    shortest = None

    # Get the shortest word from dictionary
    for word in dictionary_of_frequencies:
        if shortest is None or len(word) < len(shortest):
           shortest = word

    # Check if there is any other word with the same length
    # and create list of the shortest lengths with frequencies
    for word, frequency in dictionary_of_frequencies.items():
        if len(word) == len(shortest):
           list_of_shortest_words.append((word,frequency))

    # Sort according to frequency in descending order,
    # if frequency is the same sort it according to the increasing alphabetical order
    return sorted(list_of_shortest_words, key=lambda x: (-x[1], x[0]))


def longest_word(text):
    """Calculate the longest word(s) in given text.

    Args:
        text (str): Input text to be analyzed.

    Returns:
        list: Longest word(s) in given text.
    """
    dictionary_of_frequencies = words_frequency(text)
    list_of_longest_words = []
    longest = None

    # Get the longest word from dictionary
    for word in dictionary_of_frequencies:
        if longest is None or len(word) > len(longest):
           longest = word

    # Check if there is any other word with the same length
    # and create a list of the longest words with frequencies
    for word, frequency in dictionary_of_frequencies.items():
        if len(word) == len(longest):
            list_of_longest_words.append((word, frequency))

    # Sort according to frequency in descending order,
    # if frequency is the same sort it according to the increasing alphabetical order
    return sorted(list_of_longest_words, key=lambda x: (-x[1], x[0]))


def main():
    if len(argv) != 3:
        print("It should be: python text_analyzer.py <input_file> <output_file>")
        return

    try:
        with open(argv[1], "r") as file_input:
            text = file_input.read()

            if not text:
                print("Input text is empty.")
                return

        with open(argv[2], "w") as file_output:
             file_output.write('Statistics about {:<7}:\n'.format(argv[1]))
             file_output.write(f'{"#Words":<24}: {len(number_of_words(text))}\n')
             file_output.write(f'{"#Sentences":<24}: {number_of_sentences(text)}\n')
             file_output.write(f'{"#Words/#Sentences":<24}: {average_of_words_per_sentence(text):.2f}\n')
             file_output.write(f'{"#Characters":<24}: {number_of_all_characters(text)}\n')
             file_output.write(f'{"#Characters (Just Words)":<24}: {number_of_all_characters_just_words(text)}\n')

             # Check if there is more than one shortest word and format output according to it
             if len(shortest_word(text)) > 1:
                file_output.write(f'{"The Shortest Words":<24}:\n')
             else:
                file_output.write(f'{"The Shortest Word":<24}: ')
             for word, frequency in shortest_word(text):
                file_output.write('{:<24} ({:.4f})\n'.format(word, frequency))

             # Check if there is more than one longest word and format output according to it
             if len(longest_word(text)) > 1:
                file_output.write(f'{"The Longest Words":<24}:\n')
             else:
                file_output.write(f'{"The Longest Word":<24}: ')
             for word, frequency in longest_word(text):
                file_output.write('{:<24} ({:.4f})\n'.format(word, frequency))

             # Sort according to frequency in descending order,
             # if frequency is the same sort it according to the increasing alphabetical order
             sorted_frequencies = sorted(words_frequency(text).items(), key=lambda x: (-x[1], x[0]))
             file_output.write(f'{"Words and Frequencies":<24}:')
             for word, frequency in sorted_frequencies:
                 file_output.write(f'\n{word:<24}: {frequency:.4f}')
    except FileNotFoundError:
        print("Input file does not exist.")
        return
    except PermissionError:
        print("Permission denied.")
        return


if __name__ == '__main__':
    main()
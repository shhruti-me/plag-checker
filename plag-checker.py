import math
import string

# Preprocessing

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split())
    return text


# Tokenization

def word_tokens(text):
    return text.split()

def char_ngrams(text, n=3):
    text = text.replace(" ", "_")  # preserve word boundaries
    return [text[i:i+n] for i in range(len(text) - n + 1)]


# Jaccard Similarity

def jaccard_similarity(tokens1, tokens2):
    set1 = set(tokens1)
    set2 = set(tokens2)

    if not set1 and not set2:
        return 1.0

    return len(set1 & set2) / len(set1 | set2)


# Cosine Similarity

def frequency(tokens):
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return freq

def cosine_similarity(tokens1, tokens2):
    f1 = frequency(tokens1)
    f2 = frequency(tokens2)

    all_tokens = set(f1) | set(f2)

    dot = sum(f1.get(t, 0) * f2.get(t, 0) for t in all_tokens)
    mag1 = math.sqrt(sum(v * v for v in f1.values()))
    mag2 = math.sqrt(sum(v * v for v in f2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return dot / (mag1 * mag2)


# Interpretation

def verdict(score):
    if score < 0.3:
        return "Low similarity"
    elif score < 0.6:
        return "Moderate similarity"
    elif score < 0.85:
        return "High similarity"
    else:
        return "Possible plagiarism"


# Main

def main():
    print("Enter first text:")
    text1 = input("\n> ")

    print("\nEnter second text:")
    text2 = input("\n> ")

    t1 = clean_text(text1)
    t2 = clean_text(text2)

    # 🔁 SWITCH HERE
    # tokens1 = word_tokens(t1)
    # tokens2 = word_tokens(t2)

    tokens1 = char_ngrams(t1, n=3)
    tokens2 = char_ngrams(t2, n=3)

    jaccard = jaccard_similarity(tokens1, tokens2)
    cosine = cosine_similarity(tokens1, tokens2)

    print("\n--- Similarity Results (Character 3-grams) ---")
    print(f"Jaccard Similarity : {jaccard * 100:.2f}% ({verdict(jaccard)})")
    print(f"Cosine Similarity  : {cosine * 100:.2f}% ({verdict(cosine)})")


if __name__ == "__main__":
    main()

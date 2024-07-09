import requests
import certifi

def fetch_words_from_category(category):
    try:
        response = requests.get(
            f"https://api.datamuse.com/words?ml={category}&max=1000",
            verify=certifi.where()
        )
        response.raise_for_status()  # Raise HTTPError for bad responses
        words = [word_info['word'] for word_info in response.json()]
        return words
    except requests.RequestException as e:
        print(f"Error fetching words for category '{category}': {e}")
        return []

# Example usage
category = "animals"
words = fetch_words_from_category(category)
print(words)

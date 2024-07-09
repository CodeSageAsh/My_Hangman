import random
import requests

# Define the URL for fetching words based on a category
API_URL = "https://api.datamuse.com/words?ml={category}&max=1000"

def fetch_words_from_category(category):
    #Fetch words from an online API based on a given category.
    try:
        response = requests.get(API_URL.format(category=category))
        response.raise_for_status()
        words = [word['word'] for word in response.json() if len(word['word']) > 1]
        return words
    except requests.RequestException as e:
        print(f"An error occurred while fetching words: {e}")
        return []

def choose_word(words):
    #Randomly select a word from the list of words.
    return random.choice(words)

def display_word(word, guesses):
    # Display the word with guesses revealed and underscores for unknown letters."""
    return ''.join([letter if letter in guesses else '_' for letter in word])

def print_hangman(attempts_left):
    # Print the current hangman stage based on the number of attempts left."""
    stages = [
        "_____\n|   |\n|\n|\n|\n|\n|_______",
        "_____\n|   |\n|   O\n|\n|\n|\n|_______",
        "_____\n|   |\n|   O\n|   |\n|\n|\n|_______",
        "_____\n|   |\n|   O\n|  /|\n|\n|\n|_______",
        "_____\n|   |\n|   O\n|  /|\\\n|\n|\n|_______",
        "_____\n|   |\n|   O\n|  /|\\\n|  /\n|\n|_______",
        "_____\n|   |\n|   O\n|  /|\\\n|  / \\\n|\n|_______",
    ]
    
    # Ensure attempts_left is within the valid range
    if attempts_left < 0:
        attempts_left = 0
    elif attempts_left > len(stages) - 1:
        attempts_left = len(stages) - 1

    return stages[len(stages) - 1 - attempts_left]  # Ensure correct stage is shown

def single_player_hangman():
    # Handle single-player hangman game."""
    category = input("Enter a category to fetch words (e.g., 'animals'): ").strip()
    words = fetch_words_from_category(category)
    
    if not words:
        print("No words found for the specified category. Exiting.")
        return

    word = choose_word(words)
    display = ['_' for _ in word]
    attempts = 7
    guesses = set()

    print("Welcome to hangman! You have 7 chances to guess the word. Let's begin!")

    while attempts > 0 and '_' in display:
        print("\n" + ' '.join(display))
        print(print_hangman(attempts))
        guess = input("Guess a letter: ").lower()

        if guess in guesses:
            print("You've already guessed that letter. Try again.")
            continue

        guesses.add(guess)

        if guess in word:
            for index, letter in enumerate(word):
                if guess == letter:
                    display[index] = guess
        else:
            print('Incorrect guess!')
            attempts -= 1

    if '_' not in display:
        print(f"Hooray! You guessed '{word}' right!")
    else:
        print("_____\n|   |\n|   O\n|  /|\\\n|  / \\\n|\n|_______")
        print(f"Womp Womp! You lost. The correct word was '{word}'.")

def multiplayer_hangman():
    # Handle multiplayer hangman game."""
    category = input("Enter a category to fetch words (e.g., 'animals'): ").strip()
    words = fetch_words_from_category(category)
    
    if len(words) < 2:
        print("Not enough words found for the specified category. Exiting.")
        return

    # Randomly select two words of the same length
    valid_words = [word for word in words if len(word) > 1]
    word1 = choose_word(valid_words)
    word2 = choose_word(valid_words)

    # Ensure both words are of the same length
    while len(word1) != len(word2):
        word2 = choose_word(valid_words)
    
    display1 = ['_' for _ in word1]
    display2 = ['_' for _ in word2]
    attempts1 = 7
    attempts2 = 7
    guesses1 = set()
    guesses2 = set()
    current_player = 1

    print("\n" * 50)  # Clear screen for a fresh start

    while (attempts1 > 0 and '_' in display1) or (attempts2 > 0 and '_' in display2):
        # Display both players' current state
        print(f"Player 1's word: {' '.join(display1)}\n")
        print(f"Player 2's word: {' '.join(display2)}\n")
        
        # Print both hangmans side by side with added spacing
        hangman1 = print_hangman(attempts1)
        hangman2 = print_hangman(attempts2)
        hangman1_lines = hangman1.split('\n')
        hangman2_lines = hangman2.split('\n')
        
        for line1, line2 in zip(hangman1_lines, hangman2_lines):
            print(f"{line1:<15}    {line2:<15}")
        
        print("\n" + "-" * 50 + "\n")
        
        if current_player == 1:
            print("Player 1's turn:")
            guess = input("Guess a letter: ").lower()

            if guess in guesses1:
                print("You've already guessed that letter. Try again.")
                continue

            guesses1.add(guess)

            if guess in word1:
                for index, letter in enumerate(word1):
                    if guess == letter:
                        display1[index] = guess
            else:
                print('Incorrect guess!')
                attempts1 -= 1

            if not attempts2==0:
                current_player = 2
        else:
            print("Player 2's turn:")
            guess = input("Guess a letter: ").lower()

            if guess in guesses2:
                print("You've already guessed that letter. Try again.")
                continue

            guesses2.add(guess)

            if guess in word2:
                for index, letter in enumerate(word2):
                    if guess == letter:
                        display2[index] = guess
            else:
                print('Incorrect guess!')
                attempts2 -= 1

            if not attempts1==0:
                current_player = 1

        # Check if any player has won
        if '_' not in display1:
            print("\nPlayer 1 wins!")
            print(f"Player 2's word was: {word2}")
            return
        elif '_' not in display2:
            print("\nPlayer 2 wins!")
            print(f"Player 1's word was: {word1}")
            return

    # End game if attempts run out
    print("Game over! both lose :( ")
    if '_' in display1:
        print(f"Player 1's word was: {word1}")
    if '_' in display2:
        print(f"Player 2's word was: {word2}")

def main():
    while True:
        mode = input("Choose mode: (1) Single Player (2) Multiplayer (q) Quit: ").strip().lower()
        if mode == '1':
            single_player_hangman()
        elif mode == '2':
            multiplayer_hangman()
        elif mode == 'q':
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
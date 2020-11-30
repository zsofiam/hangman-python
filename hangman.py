import random
import os


def choose_word(file, level):
    with open(file) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        wordlist_per_level = choose_list_per_level(level, content)
        word = random.choice(wordlist_per_level)
    f.close()
    return word


def choose_list_per_level(level, content):
    easy = []
    medium = []
    hard = []
    for word in content:
        if len(word) <= 5:
            hard.append(word)
        elif 6 <= len(word) <= 9:
            medium.append(word)
        else:
            easy.append(word)
    if int(level) == 1:
        return easy
    elif int(level) == 2:
        return medium
    else:
        return hard


def start_game(file):
    lives = None
    while True:
        level = input("Choose difficulty!\n1: easy\n2: medium\n3: hard\n")  
        if level.upper() == "QUIT":
            print("Goodbye!")
            exit()
        try:
            int(level)
        except (TypeError, ValueError):
            continue
        if int(level) == 1:
            lives = 10
            break
        elif int(level) == 2:
            lives = 7
            break
        elif int(level) == 3:
            lives = 5
            break
    word = choose_word(file, level)
    play(word, lives)


def play(word, lives):
    os.system("clear")
    letters = set(word.upper())
    revealed_letters = len(word) * '-'
    guesses = []
    guessed = False
    print("Let's play!")
    while (not guessed and lives > 0):
        guess = input('Make a guess!').upper()
        if guess == "QUIT":
            print("Goodbye!")
            exit()
        if len(guess) > 1 or not guess.isalpha():
            print("Wrong input.")
            continue
        elif guess in guesses:
            print("You've already guessed the letter")
        elif guess not in letters:
            print(guess, "is not in the word")
            guesses.append(guess)
            lives -= 1
        elif guess in letters:
            print(guess, "is in the word")
            guesses.append(guess)
            revealed_letters = add_guess_to_revealed_letters(revealed_letters, guess, word)
            guessed = check_if_guessed(revealed_letters, guessed)
        print('you have', lives, 'lives')
        print(display_hangman(lives))
        print(revealed_letters + "\n")
    if guessed:
        print("Congratulations! You guessed the word!")
    else:
        print("You died. The word was", word)
        
# word: Germany
# guess: e
def add_guess_to_revealed_letters(revealed_letters, guess, word):
    revealed_letters_list = list(revealed_letters)
    indices = [i for i, letter in enumerate(word) if letter == guess]
    for index in indices:
        revealed_letters_list[index] = guess
    for i in range(0, len(word)):
        if word[i] == guess.lower():
            revealed_letters_list[i] = word[i]
    revealed_letters = "".join(revealed_letters_list)
    return revealed_letters


def check_if_guessed(revealed_letters, guessed):
    if "-" not in revealed_letters:
        guessed = True
    return guessed


def display_hangman(lives):
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """,
                """
                   --------
                   |      
                   |      
                   |    
                   |      
                   |     
                   -
                """,
                """
                
                   |      
                   |      
                   |    
                   |      
                   |     
                   -
                """,
                """
                """,
                """
                """
    ]
    return stages[lives]


# in case we want to repeat the game
def main():
    start_game("countries_and_capitals.txt")
    while True:
        answer = input("Do you want to play again? Y/N\n").upper()
        if answer == "Y":
            start_game("countries_and_capitals.txt")
            answer = input("Do you want to play again? Y/N\n").upper()
        elif answer == "N" or answer == "QUIT":
            print("Goodbye!")
            exit()
        else:
            print("Please choose!")


if __name__ == '__main__':
    main()
    # start_game("countries_and_capitals.txt")

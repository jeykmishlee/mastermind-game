import random as r
import sys

# initialize to store how many guess decrease will be done based on lifeline used, default 0
decrease_num = 0

def length_randomizer():
    # the codemaker should define the length to guess by the codebreaker (4 to 8)
    c_maker_no_length = r.randint(4,8)
    
    return c_maker_no_length

def restart_game():
    # restarts the game, sets variables to its default value before continuing

    global decrease_num
    response = input("Do you wish to play again? Y / N: ")
    
    if response.upper() == 'Y':
        # generate new length randomizer for new game
        new_c_maker_no_length = length_randomizer()
        # reset decrease guesses to start fresh when the game restarts
        decrease_num = 0
        game_proper(new_c_maker_no_length)

    else:
        sys.exit()

def guess_validation(code_breaker_guess, c_maker_pattern):
    # where validation happens, checks if there are correct number and exact position hence red or correct number but not exact position hence white.  

    # initalization, starts at 0
    red = 0
    white = 0

    # create a copy of list for removal purposes when a guess has already been seen in the pattern
    glist = code_breaker_guess[:]
    plist = c_maker_pattern[:]

    # check if number and position exists and is correct then add 1 from red and remove it from the list (this new list will be used for iteration of white checker)
    for x in range(len(code_breaker_guess)):

        if code_breaker_guess[x] == c_maker_pattern[x]:
            red+=1
            glist.remove(code_breaker_guess[x])
            plist.remove(code_breaker_guess[x])

    # check if number exists but not in exact position then add 1 from white.
    for num in glist:
        if num in plist:
            white+=1
            plist.remove(num)

    print(f"{red}R - {white}W \n")

def call_lifeline(current_guess_num, llnum, c_maker_pattern):
    # implements lifeline1 and lifline2, allows to check if the number that will be decreased from the user's available guess is 1 or 2.

    global decrease_num

    if f'lifeline#{llnum}' == 'lifeline#1':    
        # check first if the current number of guess is < 10 (lifeline#1 is applicable til 9th guess), else lifeline must not be permitted because there will be no guesses left when guess decrease happen.
        if current_guess_num < 10:
            # pick random number from the pattern as a hint
            llresult = r.choice(c_maker_pattern)
            print(f"Hidden code contains digit {llresult}.")
            print("Note: Total number of guesses is reduced by 1 \n")
            # Call number of guesses reduce to 1 
            decrease_num = 1
        else:
            print("You cannot use this lifeline on this guess since you dont have any guess left \n")
            # reset because lifeline is not permitted.
            decrease_num = 0
            return guess(current_guess_num, c_maker_pattern)

    elif f'lifeline#{llnum}' == 'lifeline#2':
        # check first if the current number of guess is < 9 (lifeline#2 is applicable til 8th guess), else lifeline must not be permitted because there will be no guesses left when guess decrease happen.
        if current_guess_num < 9:
            # pick random number from the pattern as a hint
            llresult = r.choice(c_maker_pattern)

            # if the hint number has a repeating occurence in codemaker's pattern, we should also pick from all of their available indices as its postition (randomized).
            # example: pattern is '11212', if number 1 was picked as a hint, its postition that can be returned is: 1, 2 or 3
            duplicates = {x for x in c_maker_pattern if c_maker_pattern.count(x) > 1}
            if llresult in duplicates:
                indices = [i for i, x in enumerate(c_maker_pattern) if x == llresult]
                llresult_position = r.choice(indices)
            else:
                llresult_position = c_maker_pattern.index(llresult)

            print(f"Hidden code contains digit {llresult} at position {llresult_position+1}.")
            print("Note: Total number of guesses is reduced by 2 \n")
            # Call number of guesses reduce to 2
            decrease_num = 2
        else:
            print("You cannot use this lifeline on this guess since you dont have any guess left \n")
            # reset because lifeline is not permitted.
            decrease_num = 0
            return guess(current_guess_num, c_maker_pattern)

def guess(current_guess_num, c_maker_pattern):
    # asks the player/codebreaker to guess the number pattern

    global decrease_num

    if decrease_num in (1,2):
        print(f"Guess #{current_guess_num-1}:")
    else:
        print(f"Guess #{current_guess_num}:")
    code_breaker_guess = input("Enter guess> ")

    if not code_breaker_guess.isnumeric() and 'lifeline#' not in code_breaker_guess:
        print("Invalid Guess. \nInput must contain numbers 0-9 or lifeline#1 or lifeline#2 \n")
        return guess(current_guess_num, c_maker_pattern)

    elif 'lifeline#' in code_breaker_guess:
        llnum = code_breaker_guess.split("#")[1]
        # First is to check whether the inputted lifeline is either 1 or 2
        if llnum in ('1','2'):
            # Check if the user haven't use the lifeline to permit usage.
            if decrease_num == 0:
                decrease_num = int(llnum)
                return call_lifeline(current_guess_num, int(llnum),c_maker_pattern)

            else:
                print("You already used up your lifeline earlier, you can only use this ONCE. \n")
                return guess(current_guess_num, c_maker_pattern)
        else:
            print("Please choose from lifeline#1 or lifeline#2 only \n")
            return guess(current_guess_num, c_maker_pattern)

    elif not len(code_breaker_guess) == len(c_maker_pattern):
        print(f"Invalid Guess. Code is of length {len(c_maker_pattern)}. \n")
        return guess(current_guess_num, c_maker_pattern)

    else:
        # convert code_breaker_guess from string to list for comparison
        code_breaker_guess = list(map(int,code_breaker_guess))

        if code_breaker_guess == c_maker_pattern:
            print("YOU WIN!! \n")
            return "WIN"

        else:
            guess_validation(code_breaker_guess, c_maker_pattern)

def game_proper(c_maker_no_length):
    print(f"Hidden code is of length {c_maker_no_length}.")
    print(f"Total number of Guesses: 10 \n")

    # there are 2 ways to generate random number [r.choices(allows duplicates) and r.sample(doesn't allow duplicate)]
    c_maker_pattern = r.choices((0,1,2,3,4,5,6,7,8,9), k=c_maker_no_length)

    # execute guess
    for x in range(1,11):
        # we initialize the default value of decrease_num as 0 earlier. When lifeline is called, it will be modified depending on which lifeline number has been used (equivalent to 1 or 2).
        if decrease_num == 0:
            result = guess(x, c_maker_pattern)

        # if decrease_num has been modified because the user calls for a lifeline, we need to limit the number of guesses that he will play.
        else:
            # if lifeline used is 1, then guess must not exceed by 9 guesses
            if decrease_num == 1:
                result = guess(x, c_maker_pattern)
            # if lifeline used is 2, then guess must not exceed by 8 guesses
            elif decrease_num == 2:
                if x <= 9:
                    result = guess(x, c_maker_pattern)
                else: 
                    result = "LOSE"
                    print(f"The Pattern we are looking for is: {''.join(map(str,c_maker_pattern))}")

        if result == "WIN" or result == "LOSE":
            restart_game()

    else:
        print(f"The Pattern we are looking for is: {''.join(map(str,c_maker_pattern))}")
        restart_game()



c_maker_no_length = length_randomizer()

game_proper(c_maker_no_length)

import random
import tkinter as tk
from tkinter import *
vals = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
        10: 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 1}


def main():
    money = 100
    while True:
        money = play_round(money)
        if money == 0:
            print("You have no more money, you lost")
            break
        if ask_again(money) == False:
            print(f"Thanks for playing, you ended with ${money}")
            break

    """window = Tk()  # Starts a window
    # Place window on computer screen, listen for events
    window.geometry("1600x1600")
    window.title("BlackJack Game")
    window.config(background="#330a11")

    # Labels
    img = PhotoImage(
        file='/Users/carloslage/Downloads/new_image.png')
    label = Label(window,
                  text="Welcome to BlackJack",
                  font=('Arial', 20, 'bold'),
                  fg='#f5e4e7',
                  bg='black',
                  relief=RAISED,
                  bd=30,
                  padx=10,
                  pady=10)
    textbox = tk.Text(window, height=3, font=('Arial', 16))  # Inputs textbox
    textbox.pack()

    button = tk.Button(window, text="Start Blackjack", font=('Arial', 16))
    button.pack(padx=10, pady=10)

    buttonframe = tk.Frame(window)
    buttonframe.columnconfigure(0, weight=1)
    buttonframe.columnconfigure(1, weight=1)
    buttonframe.columnconfigure(2, weight=1)

    btn1 = tk.Button(buttonframe, text="1", font=('Arial', 16))
    btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

    btn2 = tk.Button(buttonframe, text="2", font=('Arial', 16))
    btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

    btn3 = tk.Button(buttonframe, text="3", font=('Arial', 16))
    btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

    btn4 = tk.Button(buttonframe, text="4", font=('Arial', 16))
    btn4.grid(row=1, column=0, sticky=tk.W+tk.E)

    btn5 = tk.Button(buttonframe, text="5", font=('Arial', 16))
    btn5.grid(row=1, column=1, sticky=tk.W+tk.E)

    btn6 = tk.Button(buttonframe, text="6", font=('Arial', 16))
    btn6.grid(row=1, column=2, sticky=tk.W+tk.E)

    buttonframe.pack(fill='x')

    anotherbtn = tk.Button(window, text = "Test")
    anotherbtn.place(x=200,y=200,height=100,width=100)"""  # Places btn in specific place
    class MyGUI:
        def __intit__(self):

            self.root = tk.Tk()

            self.label = tk.Label(self.root, text="Your message")
            self.label.pack(padx=10, pady=10)

            self.textbox = tk.Text(self.root, height=5, font=('Arial', 18))
            self.textbook.pack(padx=10, pady=10)

            self.check_state = tk.IntVar()

            self.check = tk.Checkbutton(self.root, text="Show message", font=(
                'Arial', 16), variable=self.check_state)
            self.check.pack(padx=10, pady=10)

            self.button = tk.Button(
                self.root, text="Show Message", font=('Arial', 18))
            self.button(padx=10, pady=10)

            self.root.mainloop()

    """label.pack()

    window.mainloop()"""  # Place window on computer screen, listen for events


def play_round(m: int) -> int:
    """
    Function:
        + print how much money one has + get bet
        + pass out cards
        + insurance
        + check for blackjack(s)
        + player decisions
        + reveal dealer + dealer hits
        + see who wins + give out money accordingly

    """
    bet, m = get_bet(m)
    p_hand, d_hand = get_hands()
    pass_out_cards(p_hand, d_hand)

    d_bj = False
    if d_hand[0] == "Ace":
        insurance_taken, insurance_amnt = insurance(bet, m)
        m -= insurance_amnt
        if insurance_taken == True:
            d_bj, m = insurance_check(d_hand[1], insurance_amnt, m)
        if d_bj:
            return m

    bjs = check(p_hand, d_hand, m, bet)
    if bjs != None:
        return bjs

    under_21, choice, p_hand = player_decisions(p_hand, bet, m)

    if choice == "double" or choice == "split":
        m -= bet
        bet += bet

    if under_21 == False:
        return m

    hand_bets = []

    if choice == "split":
        p_hand_1, p_hand_2 = p_hand[0], p_hand[1]
        print("")
        under_21_1, bet_1, m = split_check(p_hand_1, bet//2, m)
        if under_21_1 == False:
            print("Hand 1 busted\n")
        else:
            hand_bets.append((p_hand_1, bet_1))
        under_21_2, bet_2, m = split_check(p_hand_2, bet//2, m)
        if under_21_2 == False:
            print("Hand 2 busted")
        else:
            hand_bets.append((p_hand_1, bet_2))
        if under_21_1 == False and under_21_2 == False:
            return m
    else:
        hand_bets = [(p_hand, bet)]

    print(f"Dealer's hand: {d_hand}")
    d_hand, d_bust = dealer_hit(d_hand, bet)
    if d_bust == True:
        for _, h_bet in hand_bets:
            m += (bet * 2)
        return m

    for hand, h_bet in hand_bets:
        outcome = win_loss(hand, d_hand)
        if outcome == True:
            print(f"YOU WINN ${h_bet}!!!!")
            m += (h_bet * 2)
        elif outcome == False:
            print("You lost :(")
        else:
            print("It's a push")
            m += h_bet
    return m


def ask_again(m: int) -> bool:
    """
    Function:
        - ask if wanna play again
    """
    while True:
        print(f"Your current balance: ${m}")
        ask = input("Do you want to play again?(yes/no) ").strip().lower()
        if ask == "yes":
            return True
        elif ask == "no":
            return False
        else:
            print("Invalid input")
            continue


def get_bet(m: int) -> tuple[int, int]:
    print("")
    print(f"You have ${m}")
    try:
        bet = int(input("What is your bet?: ").strip())
    except ValueError:
        print("Bet must be an integer, try again")
        return get_bet(m)
    if bet > m:
        print("You don't have that much money, try again")
        return get_bet(m)
    elif bet <= 0:
        print("Bet must be greater than 0, try again")
        return get_bet(m)
    m -= int(bet)
    print("")
    return bet, m


def get_hands() -> tuple[list, list]:
    return [random.choice(list(vals.keys())), random.choice(list(vals.keys()))], [random.choice(list(vals.keys())), random.choice(list(vals.keys()))]


def pass_out_cards(p: list, d: list):
    print(f"Your hand: {p}")
    print(f"Dealer's card: {d[0]}")


def calc_val(s: list) -> int:
    total = 0
    is_ace = False
    for j in s:
        if j == "Ace":
            is_ace = True
        total += vals[j]
    if is_ace:
        if total <= 11:
            total += 10
    return total


def check(p: list, d: list, m: int, b: int) -> int:
    p = calc_val(p)
    d = calc_val(d)
    if p == 21 and d == 21:
        print("It's a push, both you and dealer have blackjack")
        m += b
        return m
    elif p == 21:
        print(f"You got blackjack!!, you win {b * 3/2}")
        m += (b * 5/2)
        m = int(m)
        return m
    elif d == 21:
        print("You lost, dealer had blackjack")
        return m
    return


def insurance(bet: int, money: int) -> tuple[bool, int]:
    """
    This function:
        - asks for insurance
    Inputs:
        - bet(int)
        - money balance(int)
    Returns:
        - if taken bet (bool)
        - how much insurance bet (int)
    """
    while True:
        print("")
        print(f"Reminder, you bet {bet} and you have {money}")
        choice = input(
            "Do you want to take insurance? (yes/no) ").lower().strip()
        if choice == "yes":
            try:
                insurance_bet = int(
                    input("How much do you want to bet on insurance? ").strip())
                if insurance_bet <= 0:
                    print("Bet must be greater than 0, try again")
                    continue
                elif insurance_bet > money:
                    print("You don't have that much money, try again")
                    continue
                elif insurance_bet > bet / 2:
                    print(
                        "Insurance bet cannot be more than half of your original bet, try again")
                    continue
            except ValueError:
                print("Bet must be an integer, try again")
                continue
            print("You took insurance, you will get paid 2:1 if the dealer has blackjack")
            return True, insurance_bet
        elif choice == "no":
            print("You did not take insurance")
            print("")
            return False, 0
        else:
            print("Invalid choice, try again")
            print("")


def insurance_check(d_second_card: int, insurance_amnt: int, m: int) -> tuple[bool, int]:
    """
    Function:
        - checks if dealer has blackjack
    Returns:
        - if dealer has blackjack(bool)
        - money supply (int)
    """
    if vals[d_second_card] != 10:
        print("Dealer does not have blackjack, play on")
        return False, m
    print("Dealer did have blackjack, you win insurance")
    m += (insurance_amnt * 2)
    return True, m


def player_decisions(p: list, b: int, m: int, s=True) -> tuple[bool, str, list]:
    doub_open = True
    split_open = s
    if p[0] != p[1]:
        split_open = False
    while True:
        if b > m:
            doub_open = False
            split_open = False
        if doub_open == True and split_open == True:
            choice = input(
                "What do you want to do (hit/stand/double/split) ").lower().strip()
        elif doub_open == True:
            choice = input("What do you want to do? (hit/stand/double) ")
        else:
            choice = input(
                "What do you want to do (hit/stand) ").lower().strip()
        if choice == "hit":
            print("")
            doub_open = False
            split_open = False
            p = add_card(p)
            print(f"Your hand: {p}")
            total = calc_val(p)
            if total > 21:
                print("You busted, you lost")
                return False, choice, p
        elif choice == "double" and doub_open == True:
            print("")
            b += b
            p = add_card(p)
            print(f"Your hand: {p}")
            total = calc_val(p)
            if total > 21:
                print("You busted, you lost")
                return False, choice, p
            return True, choice, p
        elif choice == "stand":
            print("")
            return True, choice, p
        elif choice == "split" and split_open == True:
            print("")
            p = [[p[0], random.choice(list(vals.keys()))], [
                p[1], random.choice(list(vals.keys()))]]
            print(f"Your hands: {p}")
            return True, choice, p
        else:
            print("Invalid choice, try again")
            print("")


def add_card(p: list) -> list:
    p.append(random.choice(list(vals.keys())))
    return p


def dealer_hit(d: list, b: int) -> tuple[list, bool]:
    while calc_val(d) <= 16:
        d = add_card(d)
        print(f"Dealer's hand: {d}")
    print("")
    if calc_val(d) > 21:
        print(f"Dealer busted, you win ${b}!!!")
        return d, True
    return d, False


def win_loss(p: list, d: list) -> bool:
    p = calc_val(p)
    d = calc_val(d)
    if p < d:
        return False
    elif p > d:
        return True
    return


def split_check(p: list, b: int, m: int) -> tuple[bool, int, int]:
    print(f"Your hand: {p}")
    under_21, choice, p_hand = player_decisions(p, b, m, s=False)
    if choice == "double":
        m -= b
        b += b
        return True, b, m
    if under_21 == False:
        return False, b, m
    return True, b, m


if __name__ == "__main__":
    main()

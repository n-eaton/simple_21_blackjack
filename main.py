'''
For this project you will make a Blackjack game using Python.
Familiarize yourself with the the rules of the game.
You won't be implementing every rule "down to the letter" with the game, but we will doing a simpler version of the game.
This assignment will be given to further test your knowledge on object-oriented programming concepts.
'''


import random
import time
import itertools


class Deck:
    suits = ["♠", "♣️", "♥️", "♦"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def fill_deck(self):
        for i in range(0, 6):
            for suit, value in itertools.product(self.suits, self.values):
                self.cards.append(Card(suit, value))

    def clear_deck(self):
        self.cards = []

    def shuffle(self):
        random.shuffle(self.cards)


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value}{self.suit}"

    @property
    def cards_value(self):
        if self.value in ["J", "Q", "K"]:
            return 10
        if self.value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            return int(self.value)
        if self.value == "A":
            return 1


class Player:
    def __init__(self):
        self.hand = []

    def show_hand(self):
        print("\nPlayer's hand:")
        for i, card in enumerate(self.hand):
            print(str(self.hand[i]))
        print()

    def reset(self):
        self.hand = []

    @property
    def ace(self):
        return len([i for i in self.hand if i.value == "A"])

    @property
    def score(self):
        return sum([i.cards_value for i in self.hand])

    @property
    def ace_score(self):
        for ace in range(self.ace):
            if self.score < 12:
                self.score += 10
        return self.score

    @property
    def is_busted(self):
        if self.ace_score > 21:
            return True


class Human(Player):
    def __init__(self, chips):
        super().__init__()
        self.chips = chips

    def place_bet(self):
        bet = input(f"\nYou have {self.chips} chips. \nHow much would you like to bet?: ")
        try:
            if int(bet) > self.chips:
                print("You don't have enough to bet!")
                self.place_bet()
            else:
                self.chips -= int(bet)
                return int(bet)
        except ValueError:
            print("That is not a valid entry.")
            self.place_bet()


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.hand = []

    def show_hand(self, show_all=False):
        """Prints out the dealers hand, pass show_all=True to show all cards else only shows 1st card"""
        print("\nDealer's Hand:")
        if show_all:
            for n, card in enumerate(self.hand):
                print(str(self.hand[n]))
        else:
            print(str(self.hand[0]))
            print("???")


class Game:
    def __init__(self):
        self.players = []
        self.deck = []
        self.player_bet = 0
        self.players_turn = True

    def deal(self):
        print(f"{len(self.deck)} cards in Deck")
        if len(self.deck) < 104:  # When stack gets to total of 2 card decks remaining, reshuffle 6 decks
            print("Reshuffling decks...")
            self.deck.clear_deck()
            self.deck.fill_deck()
            self.deck.shuffle()
            time.sleep(4)
        for i in range(2):
            for player in self.players:
                card = self.deck.cards.pop()
                player.hand.append(card)

    def hit(self, player):
        card = self.deck.cards.pop()
        player.hand.append(card)
        if isinstance(player, Dealer):
            player.show_hand(True)
        else:
            player.show_hand()
        self.check_bust(player)
        print(f"player score is {player.ace_score}")

    def player_choice(self, player):
        answer = input("---Hit--- or ---Stick?--- h/s: ")
        if answer == "h":
            self.hit(player)
        if answer == "s":
            print(f"Player sticks with {str(player.ace_score)}\n")
            self.players_turn = False

    def check_bust(self, player):
        if player.is_busted:
            if isinstance(player, Human):
                print("Player Busts!")
                self.players_turn = False
                self.player_lose()
            if isinstance(player, Dealer):
                print("\nDealer Busts!")

    def player_win(self, player):
        print(f"You win! \n{str(2 * self.player_bet)} chips added to your total.")
        player.chips += 2 * self.player_bet
        self.player_bet = 0

    def player_lose(self):
        print(f"You lose!")

    def draw(self, player):
        print(f"Its a draw, you get your bet of {self.player_bet} back.")
        player.chips += self.player_bet

    def compare_scores(self, player, dealer):
        if player.ace_score > dealer.ace_score:
            self.player_win(player)
        if player.ace_score == dealer.ace_score:
            self.draw(player)
        if player.ace_score < dealer.ace_score:
            self.player_lose()

    def reset_players(self):
        for player in self.players:
            player.reset()
        self.player_bet = 0

    def play_again(self, player):
        again = None
        while again != "y" or again != "n":
            again = input("\nWould you like to play again? y/n: ")
            if again == "y":
                return True
            if again == "n":
                print(f"\nOk, thanks for playing. You walk away with {player.chips} chips.")
                input("Press any key to exit: ")
                return False
            else:
                print("That was not a valid input")

    def play(self):
        print("\n------------------------------------------\n")
        print("\n---------- Welcome to Blackjack ----------\n")
        print("\n------------------------------------------\n")
        self.deck = Deck()
        player = Human(1000)
        dealer = Dealer()
        self.players = [player, dealer]
        self.deck.fill_deck()
        self.deck.shuffle()
        running = True
        while running:
            if self.players[0].chips == 0:
                print("It's time to leave the table.")
                input("Press any key.")
                break
            self.player_bet = player.place_bet()
            self.deal()
            dealer.show_hand()
            player.show_hand()
            while self.players_turn:
                self.player_choice(player)
            if not player.is_busted:
                dealer.show_hand(True)
                while not self.players_turn:
                    if dealer.ace_score < 17:
                        time.sleep(1)
                        print("\nDealer Hits")
                        self.hit(dealer)
                        time.sleep(1)
                    if dealer.ace_score >= 17 and not dealer.is_busted:
                        print(f"\nDealer Sticks with hand of {str(dealer.ace_score)}\n")
                        break
                    if dealer.is_busted:
                        self.player_win(player)
                        break
                if not dealer.is_busted:
                    self.compare_scores(player, dealer)
            again = self.play_again(player)
            if not again:
                running = False
            self.players_turn = True
            self.reset_players()


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
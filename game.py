import random

class Background:
    # This class deals with creating the deck and printing the board.
    def __init__(self):
        self.deck = self.create_deck()
        self.health = 20
        self.cards_shown = 4  # Track the number of cards shown

    def create_deck(self):
        suits = ["♠", "♣", "♥", "♦"]
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def print_cards(self):
        # Show only 4 cards at a time
        for card in self.deck[:self.cards_shown]:
            print(card)

    def print_health(self):
        print(f"Your health is {self.health}.")

    def print_cards_left(self):
        print(f"Cards left in deck: {len(self.deck)}.")

    def update_cards(self):
        # Show the next set of cards once 3 cards are used
        if self.cards_shown < 2:
            self.deck = self.deck[3:]
            self.cards_shown = 4

class Cards:
    # This class handles the aftermath of choosing a card.
    def __init__(self):
        self.weapon_value = 0
        self.stack_value = 0

    def black_cards(self, health, card):
        # Subtract the weapon value from the damage dealt by black cards
        damage = self.card_value(card) - self.weapon_value
        return health - damage

    def hearts(self, health, card):
        # For hearts: add the card value to health.
        return health + self.card_value(card)

    def set_weapon(self, card):
        # For diamonds: set the weapon value based on the card.
        self.weapon_value = self.card_value(card)
        print("Weapon value", self.weapon_value)
        return self.weapon_value

    def stack(self, card):
        # Stack of diamonds under the weapon.
        card_val = self.card_value(card)
        if self.stack_value is None or card_val < self.stack_value:
            self.stack_value = card_val
        return self.stack_value

    def card_value(self, card):
        # Returns the numerical value of a card.
        rank = card[:-1]  # Remove the suit symbol.
        if rank == "A":
            return 14
        elif rank == "K":
            return 13
        elif rank == "Q":
            return 12
        elif rank == "J":
            return 11
        elif rank == "10":
            return 10
        else:
            return int(rank)

class Turn:
    # This class handles the player's turn.
    def __init__(self, background, cards):
        self.background = background
        self.cards = cards
        self.chosen_card = None

    def choose_card(self):
        self.background.print_cards()
        try:
            card_index = int(input("Choose a card position to play (1-4): ")) - 1

            if 0 <= card_index < 4:
                self.background.cards_shown -= 1
                self.chosen_card = self.background.deck.pop(card_index)
                print("You played", self.chosen_card)
                suit = self.chosen_card[-1]
                if suit in "♠♣":
                    self.background.health = self.cards.black_cards(self.background.health, self.chosen_card)
                elif suit == "♥":
                    self.background.health = self.cards.hearts(self.background.health, self.chosen_card)
                elif suit == "♦":
                    self.cards.set_weapon(self.chosen_card)
                else:
                    print("Invalid card suit")
                
                self.background.update_cards()  # Update the deck after a card is used
            else:
                print("Invalid choice: Number must be between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")

class Game:
    # This class compiles the other parts.
    def __init__(self):
        self.background = Background()
        self.cards = Cards()
        self.turn = Turn(self.background, self.cards)

    def play(self):
        while self.background.health > 0 and len(self.background.deck) > 0:
            self.turn.choose_card()
            self.background.print_cards_left()
            self.background.print_health()

# Start the game
if __name__ == "__main__":
    game_instance = Game()
    game_instance.play()

import random

class Background:
    # This class deals with creating the deck and printing the board.
    def __init__(self):
        try:
            self.deck = self.create_deck()
            self.health = 20
        except Exception as e:
            print("Error in Background.__init__:", e)
            raise

    def create_deck(self):
        try:
            suits = ["♠", "♣", "♥", "♦"]
            ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
            deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
            random.shuffle(deck)
            return deck
        except Exception as e:
            print("Error in Background.create_deck:", e)
            raise

    def print_cards(self):
        try:
            for card in self.deck[:4]:
                print(card)
        except Exception as e:
            print("Error in Background.print_cards:", e)
            raise

    def print_health(self):
        try:
            print(f"Your health is {self.health}.")
        except Exception as e:
            print("Error in Background.print_health:", e)
            raise

    def print_cards_left(self):
        try:
            print(f"Cards left in deck: {len(self.deck)}.")
        except Exception as e:
            print("Error in Background.print_cards_left:", e)
            raise
   
class Cards:
    # This class handles the aftermath of choosing a card.
    def __init__(self):
        try:
            self.weapon_value = 0
            self.stack_value = None
        except Exception as e:
            print("Error in Cards.__init__:", e)
            raise

    def black_cards(self, health, card):
        try:
            # For spades and clubs: subtract the card value from health.
            return health - self.card_value(card)
        except Exception as e:
            print("Error in Cards.black_cards:", e)
            raise

    def hearts(self, health, card):
        try:
            # For hearts: add the card value to health.
            return health + self.card_value(card)
        except Exception as e:
            print("Error in Cards.hearts:", e)
            raise

    def set_weapon(self, card):
        try:
            # For diamonds: set the weapon value based on the card.
            self.weapon_value = self.card_value(card)
            print("Weapon value" , self.weapon_value)
            return self.weapon_value
        except Exception as e:
            print("Error in Cards.set_weapon:", e)
            raise

    def stack(self, card):
        try:
            # Stack of diamonds under the weapon.
            card_val = self.card_value(card)
            if self.stack_value is None or card_val < self.stack_value:
                self.stack_value = card_val
            return self.stack_value
        except Exception as e:
            print("Error in Cards.stack:", e)
            raise

    def card_value(self, card):
        try:
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
        except Exception as e:
            print("Error in Cards.card_value:", e)
            raise

class Turn:
    # This class handles the player's turn.
    def __init__(self, background, cards):
        try:
            self.background = background
            self.cards = cards
            self.chosen_card = None
        except Exception as e:
            print("Error in Turn.__init__:", e)
            raise

    def choose_card(self):
        try:
            self.background.print_cards()
            try:
                card_index = int(input("Choose a card position to play (1-4): ")) - 1
            except ValueError as ve:
                print("Invalid input in Turn.choose_card:", ve)
                return

            if 0 <= card_index < 4:
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
            else:
                print("Invalid choice: Number must be between 1 and 4.")
        except Exception as e:
            print("Error in Turn.choose_card:", e)
            raise

class Game:
    # This class compiles the other parts.
    def __init__(self):
        try:
            self.background = Background()
            self.cards = Cards()
            self.turn = Turn(self.background, self.cards)
        except Exception as e:
            print("Error in Game.__init__:", e)
            raise

    def play(self):
        try:
            self.turn.choose_card()
            self.background.print_cards_left()
            self.background.print_health()
        
        except Exception as e:
            print("Error in Game.play:", e)
            raise

# Start the game
if __name__ == "__main__":
    try:
        game_instance = Game()
        game_instance.play()
    except Exception as e:
        print("Error in main game loop:", e)
        raise

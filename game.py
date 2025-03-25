import random

class Background:
    def __init__(self):
        self.deck = self.create_deck() 
        self.health = 20

    def create_deck(self):
        suits = ["♠", "♣", "♥", "♦"]
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"] 
        deck = [f"{rank}{suit}" for rank in ranks for suit in suits]  
        random.shuffle(deck)  
        return deck 

    def print_cards(self):
        for card in self.deck[:4]:  
            print(card)
    
    def print_health(self):
        print(f"Your health is {self.health}.")

    def print_cards_left(self):
        print(f"Cards left in deck: {len(self.deck)}.")

class Cards:
    def __init__(self):
        self.stack_value = None  

    def black_cards(self, health, card, weapon):
        if self.card_value(card) < self.stack_value:
            if self.card_value(card) < weapon:
                return health
            else:
                return health + self.diamonds(card) - self.card_value(card)

    def hearts(self, health, card):
        return health + self.card_value(card)
    
    def diamonds(self, card):
        return self.card_value(card)

    def stack(self, card):
        if card[-1] in "♠♣":  
            card_val = self.card_value(card)
            if self.stack_value is None or card_val < self.stack_value:
                self.stack_value = card_val
        return self.stack_value

    def card_value(self, card):
        rank = card[:-1]  
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
    def __init__(self, background):
        self.background = background  

    def choose_card(self):

        self.background.print_cards()
        print("Choose a card position to play (1-4):")

        try:
            card_index = int(input()) - 1
            if 0 <= card_index < 4:
                chosen_card = self.background.deck.pop(card_index)
                print("You played", chosen_card)
            else:
                print("Invalid choice, out of range.")
        except ValueError:
            print("Invalid input, please enter a number.")

class Game:
    def __init__(self):
        self.background = Background()
        self.cards = Cards()
        self.turn = Turn(self.background)

    def play(self, health):
        while health > 0:
            self.turn.choose_card()
            self.background.print_cards_left()
            self.background.print_health()
            self.background.print_cards()
            

game_instance = Game()
game_instance.play(game_instance.background.health)

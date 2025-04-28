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
        for card in deck:
            if card[-1] == "♦" and card[0] in "JQKA":
                deck.remove(card)
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
            if len(self.deck) > 4:
                self.cards_shown = 4 
            else: 
                self.cards_shown = len(self.deck)

class Cards:
    # This class handles the aftermath of choosing a card.
    def __init__(self):
        self.weapon_value = 0
        self.weapon_str = " " # to give the weapon a visual 
        self.stack_value = 0

    def black_cards(self, health, card):
        # weapon behavior is a bit complicated
        #   - a new weapon ("top" card is diamond) can be used for any black card 
        #   - a used weapon can only be used for black cards equal to or less than the current value
        #   - you can always fight with fists and have 0 defense. This keeps your weapon as is
        
        value = self.card_value(card) 
        if value > self.weapon_value and self.weapon_str[-1] != "♦":
            return health - value
        choice = input("Fight with (W)eapon or (F)ists: ").upper().strip()
        if choice == "F":
            return health - value
        elif choice == "W":
            pass
        else:
            print("Invalid choice. Defaulting to fists.")
            return health - value

        # weapon fighting was selected
        #if self.weapon_str[-1] == "♦": # new weapon
        damage = max(0, value - self.weapon_value) # make sure there is no negative damage
        self.weapon_value = value
        self.weapon_str += "->" + card
        return health - damage

    def hearts(self, health, card):
        # For hearts: add the card value to health.
        return min(20, health + self.card_value(card)) 

    def set_weapon(self, card):
        # For diamonds: set the weapon value based on the card.
        self.weapon_value = self.card_value(card)
        self.weapon_str = card
        print("Weapon value", self.weapon_value)
        return self.weapon_value

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
        self.new_room = True
        self.canrun = True

    def choose_card(self):
        print("\n\n")
        self.background.print_cards()
        print("Weapon: " + self.cards.weapon_str)
        print("Health:", self.background.health, "\n")

        try:
            if self.new_room: 
                run= input("Run from room? Y/N: ").strip().upper()
                while run != "Y" and run != "N":
                    print("Invalid input.")
                    run = input("Run from room? Y/N: ").strip().upper()
                if run == "Y":
                    print("")
                    current_room = self.background.deck[0:4]
                    self.background.deck = self.background.deck[4:]
                    self.background.deck.extend(current_room)
                    self.background.print_cards()
                    print("Weapon: " + self.cards.weapon_str)
                    print("Health:", self.background.health, "\n")
                    self.new_room = False

            card_index = int(input("Choose a card position to play (1-" + str(self.background.cards_shown) + "): ")) - 1
            if 0 <= card_index < self.background.cards_shown: #figures out which suit your card is to determine further steps
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
                
                if self.background.cards_shown < 2: 
                    self.new_room = True
                else: 
                    self.new_room = False
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

        if self.background.health > 0:
            print("\
▄██   ▄    ▄██████▄  ███    █▄        ▄█     █▄   ▄█  ███▄▄▄▄   \n\
███   ██▄ ███    ███ ███    ███      ███     ███ ███  ███▀▀▀██▄ \n\
███▄▄▄███ ███    ███ ███    ███      ███     ███ ███▌ ███   ███ \n\
▀▀▀▀▀▀███ ███    ███ ███    ███      ███     ███ ███▌ ███   ███ \n\
▄██   ███ ███    ███ ███    ███      ███     ███ ███▌ ███   ███ \n\
███   ███ ███    ███ ███    ███      ███     ███ ███  ███   ███ \n\
███   ███ ███    ███ ███    ███      ███ ▄█▄ ███ ███  ███   ███ \n\
 ▀█████▀   ▀██████▀  ████████▀        ▀███▀███▀  █▀    ▀█   █▀  \n\
")                                                                

        else: 
            print("No Health You lose :(") 
            print("⠀    ⣀⣠⠤⠶⠶⣖⡛⠛⠿⠿⠯⠭⠍⠉⣉⠛⠚⠛⠲⣄⠀⠀⠀⠀⠀")
            print("⠀⠀⢀⡴⠋⠁⠀⡉⠁⢐⣒⠒⠈⠁⠀⠀⠀⠈⠁⢂⢅⡂⠀⠀⠘⣧⠀⠀⠀⠀")
            print("⠀⠀⣼⠀⠀⠀⠁⠀⠀⠀⠂⠀⠀⠀⠀⢀⣀⣤⣤⣄⡈⠈⠀⠀⠀⠘⣇⠀⠀⠀")
            print("⢠⡾⠡⠄⠀⠀⠾⠿⠿⣷⣦⣤⠀⠀⣾⣋⡤⠿⠿⠿⠿⠆⠠⢀⣀⡒⠼⢷⣄⠀")
            print("⣿⠊⠊⠶⠶⢦⣄⡄⠀⢀⣿⠀⠀⠀⠈⠁⠀⠀⠙⠳⠦⠶⠞⢋⣍⠉⢳⡄⠈⣧")
            print("⢹⣆⡂⢀⣿⠀⠀⡀⢴⣟⠁⠀⢀⣠⣘⢳⡖⠀⠀⣀⣠⡴⠞⠋⣽⠷⢠⠇⠀⣼")
            print("⠀⢻⡀⢸⣿⣷⢦⣄⣀⣈⣳⣆⣀⣀⣤⣭⣴⠚⠛⠉⣹⣧⡴⣾⠋⠀⠀⣘⡼⠃")
            print("⠀⢸⡇⢸⣷⣿⣤⣏⣉⣙⣏⣉⣹⣁⣀⣠⣼⣶⡾⠟⢻⣇⡼⠁⠀⠀⣰⠋⠀⠀")
            print("⠀⢸⡇⠸⣿⡿⣿⢿⡿⢿⣿⠿⠿⣿⠛⠉⠉⢧⠀⣠⡴⠋⠀⠀⠀⣠⠇⠀⠀⠀")
            print("⠀⢸⠀⠀⠹⢯⣽⣆⣷⣀⣻⣀⣀⣿⣄⣤⣴⠾⢛⡉⢄⡢⢔⣠⠞⠁⠀⠀⠀⠀")
            print("⠀⢸⠀⠀⠀⠢⣀⠀⠈⠉⠉⠉⠉⣉⣀⠠⣐⠦⠑⣊⡥⠞⠋⠀⠀⠀⠀⠀⠀⠀")
            print("⠀⢸⡀⠀⠁⠂⠀⠀⠀⠀⠀⠀⠒⠈⠁⣀⡤⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
            print("⠀⠀⠙⠶⢤⣤⣤⣤⣤⡤⠴⠖⠚⠛⠉")


# Start the game
if __name__ == "__main__":
    game_instance = Game()
    playing = True
    
    while playing:
        print("\n" * 40)  

        print("Welcome to...\n")
        print(r"""
    ▄████████  ▄████████  ▄██████▄  ███    █▄  ███▄▄▄▄   ████████▄     ▄████████    ▄████████  ▄█      
  ███    ███ ███    ███ ███    ███ ███    ███ ███▀▀▀██▄ ███   ▀███   ███    ███   ███    ███ ███       
  ███    █▀  ███    █▀  ███    ███ ███    ███ ███   ███ ███    ███   ███    ███   ███    █▀  ███       
  ███        ███        ███    ███ ███    ███ ███   ███ ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄     ███       
▀███████████ ███        ███    ███ ███    ███ ███   ███ ███    ███ ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ███       
         ███ ███    █▄  ███    ███ ███    ███ ███   ███ ███    ███ ▀███████████   ███    █▄  ███       
   ▄█    ███ ███    ███ ███    ███ ███    ███ ███   ███ ███   ▄███   ███    ███   ███    ███ ███▌    ▄ 
 ▄████████▀  ████████▀   ▀██████▀  ████████▀   ▀█   █▀  ████████▀    ███    ███   ██████████ █████▄▄██ 
                                                                     ███    ███              ▀        
""")
        instructions = ""
        while instructions not in ("Y", "N"):
            instructions = input("Need instructions? Y/N\n\n").strip().upper()
            if instructions == "Y":
                print("\nInstructions:")
                print("You get a Room from the deck consisting of 4 cards.")
                print("To move to the next room, you can either face the room (pick 3 cards) or run (shuffle and get 4 new cards),")
                print("but you can't run from two rooms in a row.")
                print("Hearts will heal you for the face value.(max 20)")
                print("Black cards (Clubs and Spades) damage you for the face value.")
                print("Diamonds are weapons that protect you from damage for the face value.")
                print("Be careful, using your weapon on an enemy makes it duller, and it can only kill an enemy")
                print("with a lower face value than the previous one.(resets after a new weapon)") 
                print("If you have no weapon, you can use your fists to block damage.(0 value)")
                print("The goal is to get through the deck without dying.")
                print("If you run out of cards, you win.")
                print("If you run out of health, you lose.")
                print("Good luck!")   
                print("\n")

        start = ""
        while start not in ("Y", "N"):
            start = input("\nStart New Run? Y/N\n\n").strip().upper()

        if start == "Y":
            game_instance = Game()
            game_instance.play()
            input("\nPress ENTER to continue...")
        else:
            playing = False

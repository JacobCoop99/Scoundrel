# Scoundrel
Final Project: Scoundrel (a card based rougelike game) Members: Luca Sheridan and Jacob Coopersmith

Based directly on this game: http://www.stfj.net/art/2011/Scoundrel.pdf

## Description

Scoundrel is a one player game based on a standard deck of cards.
It involves drawing four cards to create a "room" of a dungeon and the goal of the game is to progress through all the rooms and finish the dungeon.
Each suit of card represents a different thing. Spades and clubs are monster cards; diamonds are weapon cards used to fight monsters; and hearts heal the player.
In order to progress to the next room, there must be only one card remaining in the room and then the new room is entered by drawing cards to fill the three empty slots
Weapons are equipped by drawing them from a room. Drawing a weapon replaces your previous one.
Only one heart card can be used to heal per room. The second card forward is just discarded.
The player can fight monsters in two ways: barehanded or with a weapon.
When fighting barehanded you take damage based on the rank of the card (2-Ace where ace is 14).
You can equip a weapon by taking it from the room. When you fight a monster with it you subtract the weapon value from the monster value and take the leftover damage. After using the weapon to kill a monster, the monster card remains on top of the weapon card and it can now only be used to kill monsters with a smaller value. The next monster you kill with it is placed on top in the same way.
Your weapon and its status remains with you between rooms
Before interacting with a room you can run from it and the four cards are placed on the bottom of the deck. You cannot run from two rooms in a row.
The project will be built in python

## What our game needs

Fully implement all the rules and mechanics
Random number generator to shuffle the cards
Using classes to represent each card, the deck of cards, and the weapons.
We currently don’t plan to use any other technologies or languages

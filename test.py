import pygame
import random

# Card values and suits
card_values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Create a shuffled deck of cards
def create_deck():
    deck = [(value, suit) for suit in suits for value in card_values]
    random.shuffle(deck)
    return deck

# Deal a card
def deal_card(deck):
    return deck.pop()

# Calculate hand score
def calculate_score(hand):
    score = 0
    num_aces = sum(1 for card in hand if card[0] == 'A')  # Count Aces correctly
    for card in hand:
        score += card_values[card[0]]
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

# Start the game
def start_game():
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    return deck, player_hand, dealer_hand

# Handle player's hit
def hit(deck, hand):
    hand.append(deal_card(deck))

# Handle player's stand
def stand(deck, player_hand, dealer_hand):
    while calculate_score(dealer_hand) < 17:
        hit(deck, dealer_hand)

# Determine the winner
def determine_winner(player_hand, dealer_hand):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    if player_score > 21:
        return "Dealer Wins!"
    elif dealer_score > 21:
        return "Player Wins!"
    elif player_score > dealer_score:
        return "Player Wins!"
    elif dealer_score > player_score:
        return "Dealer Wins!"
    else:
        return "Tie!"

# Game loop
def game_loop():
    deck, player_hand, dealer_hand = start_game()
    while True:
        print("\nPlayer Hand:", player_hand)
        print("Player Score:", calculate_score(player_hand))
        print("Dealer's Up Card:", dealer_hand[0])
        
        action = input("Hit (h) or Stand (s)? ").strip().lower()
        if action == 'h':
            hit(deck, player_hand)
            if calculate_score(player_hand) > 21:
                print("Player Busts! Dealer Wins!")
                return
        elif action == 's':
            stand(deck, player_hand, dealer_hand)
            break
        else:
            print("Invalid input. Please enter 'h' or 's'.")

    print("\nDealer Hand:", dealer_hand)
    print("Dealer Score:", calculate_score(dealer_hand))
    print(determine_winner(player_hand, dealer_hand))

# Start the game
game_loop()


import pygame
import random

# Init pygame
pygame.init()

# Scherminstellingen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# Kleuren
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)

# Kaartwaarden en suits
card_values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Laad lettertype
font = pygame.font.Font(None, 36)

def create_deck():
    """Maakt een geschud deck van kaarten."""
    deck = [(value, suit) for suit in suits for value in card_values]
    random.shuffle(deck)
    return deck

def deal_card(deck):
    """Geeft een kaart uit het deck."""
    return deck.pop()

def calculate_score(hand):
    """Bereken de score van een hand."""
    score = 0
    num_aces = sum(1 for card in hand if card[0] == 'A')
    for card in hand:
        score += card_values[card[0]]
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

def stand(deck, dealer_hand):
    """Laat de dealer spelen totdat de score minimaal 17 is."""
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))

def determine_winner(player_hand, dealer_hand):
    """Bepaalt de winnaar van de ronde."""
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    if player_score > 21:
        return "Dealer Wins!"
    elif dealer_score > 21 or player_score > dealer_score:
        return "Player Wins!"
    elif dealer_score > player_score:
        return "Dealer Wins!"
    else:
        return "Tie!"

def reset_game():
    """Herstart het spel en geeft nieuwe handen."""
    global deck, player_hand, dealer_hand, game_over, winner
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    game_over = False
    winner = ""

# Start een nieuw spel
reset_game()

# Game loop
running = True
while running:
    screen.fill(GREEN)  # Achtergrondkleur

    # Scoreberekening
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand) if game_over else "?"
    
    # Tekst tonen
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    dealer_text = font.render(f"Dealer: {dealer_score}", True, WHITE)
    
    screen.blit(player_text, (50, 400))
    screen.blit(dealer_text, (50, 100))

    # Kaarten tekenen
    for i, card in enumerate(player_hand):
        pygame.draw.rect(screen, WHITE, (50 + i * 80, 450, 70, 100))
        text = font.render(card[0], True, BLACK)
        screen.blit(text, (70 + i * 80, 490))

    for i, card in enumerate(dealer_hand):
        pygame.draw.rect(screen, WHITE, (50 + i * 80, 150, 70, 100))
        if game_over or i == 0:
            text = font.render(card[0], True, BLACK)
            screen.blit(text, (70 + i * 80, 190))
        else:
            pygame.draw.rect(screen, BLACK, (50 + i * 80, 150, 70, 100))  # Verberg dealerkaart

    # Knoppen tekenen
    hit_button = pygame.draw.rect(screen, WHITE, (300, 500, 100, 50))
    stand_button = pygame.draw.rect(screen, WHITE, (450, 500, 100, 50))
    
    hit_text = font.render("HIT", True, BLACK)
    stand_text = font.render("STAND", True, BLACK)
    screen.blit(hit_text, (330, 515))
    screen.blit(stand_text, (460, 515))

    # Winnaar tonen en 'New Game'-knop toevoegen als het spel voorbij is
    if game_over:
        result_text = font.render(winner, True, WHITE)
        screen.blit(result_text, (WIDTH // 2 - 100, HEIGHT // 2))

        new_game_button = pygame.draw.rect(screen, WHITE, (320, 350, 160, 50))
        new_game_text = font.render("NEW GAME", True, BLACK)
        screen.blit(new_game_text, (340, 365))

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not game_over:
                if hit_button.collidepoint(x, y):
                    player_hand.append(deal_card(deck))
                    if calculate_score(player_hand) > 21:
                        game_over = True
                        winner = "Dealer Wins!"
                elif stand_button.collidepoint(x, y):
                    stand(deck, dealer_hand)
                    game_over = True
                    winner = determine_winner(player_hand, dealer_hand)
            else:
                if new_game_button.collidepoint(x, y):
                    reset_game()  # Start een nieuw spel

pygame.quit()

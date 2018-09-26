import random
import os

# Global variable, to avoid having to pass the deck around
deck = [i for i in xrange(2, 15)] * 4

# Macro to encode face-cards
switch = {
	11: "J",
	12: "Q",
	13: "K",
	14: "A"
}

# Draw a card from deck
def pickCard():
	random.shuffle(deck)
	card = deck.pop()
	if card in switch: 
		card = switch[card]
	return card

# Draw two cards and return two hands
def dealHand():
	hand = []
	hand.append(pickCard())
	hand.append(pickCard())
	return hand

# Return the value of a hand of cards
def handValue(hand):
	total = 0
	face_cards = ["J", "Q", "K"]
	for card in hand:
		if card in face_cards:
			total += 10
		elif card == "A":
			if total >= 11:
				total += 1
			else:
				total += 11
		else:
			total += card
	return total

# Reset the screen and game variables
def resetGame():
	query_player = raw_input("Do you want to play again (y/n)? : ").lower()
	if query_player == "n":
		print "Thanks for playing. Bye!"
		exit()
	else:
		dealer_hand = []
		player_hand = []
		deck = [i for i in xrange(2, 15)] * 4
		main()

# Print hands and values for both players
def printGame(player_hand, dealer_hand):
	cleanScreen()
	print "The dealer has a ", str(dealer_hand), "which is worth ", str(handValue(dealer_hand))
	print "You have a ", str(player_hand), "which is worth ", str(handValue(player_hand))

# End conditions
def checkBlackjack(player_hand, dealer_hand):
	player_hand_value = handValue(player_hand)
	dealer_hand_value = handValue(dealer_hand)
	if player_hand_value == 21:
		printGame(player_hand, dealer_hand)
		print "You have blackjack! You win!"
		resetGame()
	elif dealer_hand_value == 21:
		printGame(player_hand, dealer_hand)
		print "The dealer has balckjack! Sorry, you lose."
		resetGame()
	elif player_hand_value > 21:
		printGame(player_hand, dealer_hand)
		print "You have over 21! You've busted. Dealer wins!"
		resetGame()
	elif dealer_hand_value > 21:
		printGame(player_hand, dealer_hand)
		print "The dealer has over 21! Dealer has busted. You win!"
		resetGame()

# Dealer builds a hand with the heuristic of staying at values 17 and above
def makeFinalDealerHand(dealer_hand):
	while handValue(dealer_hand) < 17:
		dealer_hand.append(pickCard())
	return dealer_hand

# Compare scores and print results
def compareScores(player_hand, dealer_hand):
	player_hand_value = handValue(player_hand)
	dealer_hand_value = handValue(dealer_hand)
	if player_hand_value > dealer_hand_value:
		printGame(player_hand, dealer_hand)
		print "Your hand is worth more than the dealer's hand. You win!"
	else:
		printGame(player_hand, dealer_hand)
		print "Your hand is not worth more than the dealer's hand. The dealer wins!"

# Avoid cluttering of a screen
def cleanScreen():
	if os.name == "nt":
		os.system("CLS")
	elif os.name == "posix":
		os.system("clear")

# Hosts the game
def main():
	cleanScreen()
	print "Let's play some Blackjack!"

	# set up the game
	dealer_hand = dealHand()
	player_hand = dealHand()
	player_hand_value = handValue(player_hand)

	print "The dealer is showing a", str(dealer_hand[0])
	print "You have ", str(player_hand), " which is worth ", player_hand_value
	checkBlackjack(player_hand, dealer_hand)
	user_choice = raw_input("Do you want a hit (h), to stay (s), or quit (q)? : ").lower()
	cleanScreen()
	while user_choice != "q":
		if user_choice == "h":
			# keep hitting
			while user_choice != "n":
				new_card = pickCard()
				player_hand.append(new_card)
				player_hand_value = handValue(player_hand)
				print "You were dealt a ", str(new_card)
				print "You now have ", str(player_hand), " which is worth ", player_hand_value
				if player_hand_value > 21:
					printGame(player_hand, dealer_hand)
					print "You have over 21! You've busted. Dealer wins!"
					resetGame()
				user_choice = raw_input("Do you want another hit? (y/n) : ").lower()
				checkBlackjack(player_hand, dealer_hand)
			dealer_hand = makeFinalDealerHand(dealer_hand)
			if handValue(dealer_hand) > 21:
				printGame(player_hand, dealer_hand)
				print "The dealer has busted. You win!"
			compareScores(player_hand, dealer_hand)
		elif user_choice == "q":
			print "Thanks for playing. Bye!"
			exit()
		elif user_choice != "s":
			print "Invalid input entered: ", user_choice
			resetGame()			
		else:
			dealer_hand = makeFinalDealerHand(dealer_hand)
			compareScores(player_hand, dealer_hand)
		resetGame()

if __name__ == '__main__':
	main()
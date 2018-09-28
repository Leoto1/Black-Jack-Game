import random
import os


class Player:
    def __init__(self, name, points):
        self.name = name
        self.points = points
        self.card = []
        self.card_stack = []
        self.sum = 0

    def show_points(self):
        return self.points

    def points_inc(self):
        self.points += 100

    def points_dec(self):
        self.points -= 100

    def drawn_card(self, card):
        self.card = card
        self.stack(self.card)
        self.total(self.card[0])

    def stack(self, card):
        self.card_stack.append(card)

    def show_stack(self):
        return self.card_stack

    def reset(self):
        self.card_stack = []
        self.sum = 0

    def total(self, card_value):
        if card_value > 10:
            card_value = 10
        self.sum = self.sum + card_value

    def show_total(self):
        return self.sum

    def ask(self):
        ans = input('\nDO you want to HIT or STAND ')
        if ans.upper() == 'HIT':
            return True
        else:
            return False

    def compute(self):
        if self.sum <= 12:
            return True
        else:
            return False

    def ace_manager(self):
        flag = 0
        for card in self.card_stack:
            if(card[0] == 1):
                flag = 1
        if flag:
            ace = self.sum + 10
            if(ace <= 21):
                self.sum += 10

    def check(self):
        if self.sum > 21:
            print(self.name + " got BUSTED")
            self.points_dec()
            return True
        else:
            return False


class Deck:
    global human, computer, res1, res2, bust1, bust2

    def __init__(self):
        self.count = 0
        self.cards = []
        self.suit = ['\u2660', '\u2666', '\u2663', '\u2665']
        for i in self.suit:
            for j in range(13):
                temp = [j + 1, i]
                self.cards.append(temp)

    def shuffle(self):
        return random.shuffle(self.cards)

    def distribute(self):
        if res1 and res2:
            computer.drawn_card(self.cards[self.count])
            self.count += 1
            human.drawn_card(self.cards[self.count])
            self.count += 1
        elif res1 == True and res2 == False:
            human.drawn_card(self.cards[self.count])
            self.count += 1
        elif res1 == False and res2 == True:
            computer.drawn_card(self.cards[self.count])
            self.count += 1

    def compare(self):
        if bust1 or bust2:
            if bust1:
                return 0
            else:
                return 1
        elif human.show_total() > computer.show_total():
            human.points_inc()
            computer.points_dec()
            return 1
        elif human.show_total() < computer.show_total():
            human.points_dec()
            computer.points_inc()
            return 0
        else:
            return 2

    def display(self):
        os.system('cls')
        real = [' A', ' 2', ' 3', ' 4', ' 5', ' 6',
                ' 7', ' 8', ' 9', '10', ' J', ' Q', ' K']
        print('Your cards are \n')
        stack = human.show_stack()
        points = human.show_points()
        for card in stack:
            print('|---------|')
            print('|         |')
            print('|   %s %s  |' % (real[card[0] - 1], card[1]))
            print('|         |')
            print('|---------|')

        print("\nYour Points : ", points)

    def display_result(self, result):
        os.system('cls')
        human.check()
        computer.check()
        real = [' A', ' 2', ' 3', ' 4', ' 5', ' 6',
                ' 7', ' 8', ' 9', '10', ' J', ' Q', ' K']
        print('Your cards are \n')
        stack = human.show_stack()
        for card in stack:
            print('|---------|')
            print('|         |')
            print('|   %s %s  |' % (real[card[0] - 1], card[1]))
            print('|         |')
            print('|---------|')
        print('Computers cards are \n')
        stack = computer.show_stack()
        for card in stack:
            print('|---------|')
            print('|         |')
            print('|   %s %s  |' % (real[card[0] - 1], card[1]))
            print('|         |')
            print('|---------|')

        if result == 0:
            print('Computer won')
        elif result == 1:
            print('You won!')
        points = human.show_points()
        print('Your Current Points :', points)

    def reset(self):
        self.count = 0


def get_highscore():
    f = open('score.txt', 'r+')
    highscore = f.read()
    f.close()
    f = open('scorer.txt', 'r+')
    player = f.read()
    f.close()
    return highscore, player


def set_highscore(name, points):
    f = open('score.txt', 'r+')
    highscore = int(f.read())
    f.close()
    if(highscore < points):
        f = open('score.txt', 'w+')
        f.write(str(points))
        f.close()
        f = open('scorer.txt', 'w+')
        f.write(name)
        f.close()


os.system(" cls ")
print('+------------------------------------------------------+')
print('+                WELCOME TO BLACKJACK                  +')
print('+------------------------------------------------------+')
highscore, player = get_highscore()
print('\nCURRENT HIGHSCORE : ')
print('%s - %s' % (player, highscore))
input('\nPress any key to Start')
name = input('\nEnter Your Name ')
os.system(" cls ")
human = Player(name, 1000)
computer = Player('Computer', 10000000)
deck = Deck()
while 1:
    human.reset()
    computer.reset()
    deck.reset()
    if human.show_points() <= 0:
        print('Sorry Your Points are insufficient to play game start again ')
        break
    print('Shuffling cards.....')
    deck.shuffle()
    res1, res2, bust1, bust2 = True, True, False, False
    deck.distribute()
    deck.display()
    while 1:
        if(res1 == True):
            res1 = human.ask()
        res2 = computer.compute()
        deck.distribute()
        if(res1 == True):
            deck.display()
        bust1 = human.check()
        bust2 = computer.check()
        if bust1 or bust2:
            break
        if not res1 and not res2:
            break
    human.ace_manager()
    computer.ace_manager()
    result = deck.compare()
    deck.display_result(result)
    reply = input('DO YOU WANT TO PLAY AGAIN Y/N ')
    if reply.upper() == 'N':
        break
set_highscore(name, human.show_points())
print('Thanks for Playing')

#import関連
from math import inf, floor
import random
from time import sleep


class Card():
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __repr__(self):
        return f'{self.suit} {self.number}'


class Deck():

    def __init__(self):
        suits = ['♠', '♥', '♣', '♦']
        numbers = [
            {'key': 'A', 'value': 11},
            {'key': '2', 'value': 2},
            {'key': '3', 'value': 3},
            {'key': '4', 'value': 4},
            {'key': '5', 'value': 5},
            {'key': '6', 'value': 6},
            {'key': '7', 'value': 7},
            {'key': '8', 'value': 8},
            {'key': '9', 'value': 9},
            {'key': '10', 'value': 10},
            {'key': 'J', 'value': 10},
            {'key': 'Q', 'value': 10},
            {'key': 'K', 'value': 10},
        ]

        self.cards = []

        for i in range(6):
            for suit in suits:
                for number in numbers:
                    self.cards.append(Card(suit, number))

    def deal(self):
        return self.cards.pop(0)

    def shuffle(self):
        random.shuffle(self.cards)



class Hand():

    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.total = 0

    def add_card(self, card):
        self.cards.append(card)

    def calc_value(self):
        self.value = 0
        ace = False
        for card in self.cards:
            self.value += int(card.number['value'])
            if card.number['key'] == 'A':
                ace = True

        if ace and self.value > 21:
            self.value -= 10

        return self.value

    def is_blackjack(self):
        return self.calc_value() == 21

    def show(self, show_two_cards=False):
        print(f"{'Dealer' if self.dealer else 'Your'} hand:")

        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_two_cards and not self.is_blackjack():
                pass
            else:
                print(f"{card.suit} {card.number['key']}")
        if not self.dealer:
            print('Total:', self.calc_value())
        print()


#Gameエンジンメイン部分
class Game():
    Zs =''
    def check_winner(self, player_hand, dealer_hand, player_cards, dealer_cards, game_over=False):
        global Zs
        if not game_over: #ブラックジャックの判定
            if player_hand.calc_value() > 21:
                print('あなたは21を超えました. Dealer wins!')
                Zs = 'Mlose'
                return True
            elif dealer_hand.calc_value() > 21:
                print('ディーラーは21を超えました. You win!')
                Zs = 'Mwin'
                return True
            elif player_hand.is_blackjack() and dealer_hand.is_blackjack() and (player_cards == 2) and (dealer_cards == 2):
                print('ふたりともブラックジャックです. Draw!')
                Zs = 'Mdraw'
                return True
            elif player_hand.is_blackjack() and (player_cards == 2):
                print('あなたはブラックジャックです! You win!')
                Zs = 'BR'
                return True
            elif dealer_hand.is_blackjack() and (dealer_cards == 2):
                print('ディーラーはブラックジャックです! Dealer wins!')
                Zs = 'Mlose'
                return True
        else: #勝者判定
            if player_hand.calc_value() > dealer_hand.calc_value():
                print('あなたの勝ちです!')
                Zs = 'Mwin'
            elif player_hand.calc_value() == dealer_hand.calc_value():
                print('引き分けです!')
                Zs = 'Mdraw'
            else:
                print('残念、ディーラーの勝ちです‥')
                Zs = 'Mlose'
            return True
        return False

    def play(self):
        game_to_play = 0
        game_number = 0
        kane = 10000
        kane_hen=0

        while game_to_play <= 0: #プレー回数の選択
            try:
                game_to_play_kai = input('何回ゲームをプレーしますか？(未定ならばinf)> ')
                if game_to_play_kai == 'inf':
                    game_to_play = inf
                else:
                    game_to_play = int(game_to_play_kai)
            except ValueError:
                print('数字で入力してください(未定ならばinf)> ')
        
        while not(not(game_number < game_to_play) or not(kane != 0)): #n回プレイする
            #プレイ回数カウント
            game_number += 1
            
            #デッキの初期化
            deck = Deck()
            deck.shuffle()

            #カードを配る
            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            #BRバグ防止
            player_cards = 2
            dealer_cards = 2

            for i in range(2):
                player_hand.add_card(deck.deal())
                dealer_hand.add_card(deck.deal())

            print()
            sleep(1.5)
            print(f'ゲームの回数 {game_number}/{game_to_play}')
            sleep(1)
            print()

            print('所持金:' + str(kane)) #賭け金設定
            kane_hen = -1
            while ((kane_hen < 0) or ((kane - kane_hen) < 0)):
                try:
                    kane_hen = int(input('賭け金を入力してください> '))
                except ValueError:
                    print('数字で入力してください')
            kane = kane - kane_hen
            
            #カード表示
            player_hand.show()
            dealer_hand.show()

            #ブラックジャック判定
            if self.check_winner(player_hand, dealer_hand, player_cards, dealer_cards):
                if Zs == 'Mwin':
                    kane = kane + kane_hen*2
                elif Zs == 'BR':
                    kane = kane + floor(kane_hen*2.5)
                elif Zs == 'Mdraw':
                    kane = kane + kane_hen
                continue

            #プレイヤーのターン
            choice = ''
            while choice not in ['s', 'stand'] and player_hand.calc_value() < 21:
                choice = input('Hit または Stand をしてください (h/s)> ').lower()
                print()
                player_cards += 1
                while choice not in ['h', 's', 'hit', 'stand']:
                    choice = input('hit or stand (h/s) を入力してください> ').lower()
                    print()
                if choice in ['hit', 'h']:
                    player_hand.add_card(deck.deal())
                    player_hand.show()

            if self.check_winner(player_hand, dealer_hand, player_cards, dealer_cards):
                if Zs == 'Mwin':
                    kane = kane + kane_hen*2
                elif Zs == 'BR':
                    kane = kane + floor(kane_hen*2.5)
                elif Zs == 'Mdraw':
                    kane = kane + kane_hen
                
                continue

            #ディーラーのターン
            while dealer_hand.calc_value() < 17:
                dealer_cards += 1
                dealer_hand.add_card(deck.deal())
                dealer_hand.calc_value()
                dealer_hand.show(show_two_cards=True)
            
            #結果出力
            if self.check_winner(player_hand, dealer_hand, player_cards, dealer_cards):
                if Zs == 'Mwin':
                    kane = kane + kane_hen*2
                elif Zs == 'BR':
                    kane = kane + floor(kane_hen*2.5)
                elif Zs == 'Mdraw':
                    kane = kane + kane_hen
                continue

            print('結果発表')
            print('Your hand:', player_hand.calc_value())
            print('Dealer hand:', dealer_hand.calc_value())
            self.check_winner(player_hand, dealer_hand, player_cards, dealer_cards, game_over=True)
            if Zs == 'Mwin':
                kane = kane + kane_hen*2
            elif Zs == 'BR':
                kane = kane + floor(kane_hen*2.5)
            elif Zs == 'Mdraw':
                kane = kane + kane_hen
        
        #破産判定
        if kane <= 0:
            print()
            print('所持金が0になってしまいました')
            

#Gameトリガー
print('～ブラックジャック～')
print(' Version: 1.2')
print()
game = Game()
game.play()


#exe用
for i in range(2):
    print()
input('終了するにはEnterキーを押してください> ')
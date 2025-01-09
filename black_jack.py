import sys
import random

#  Задаем значение констант.

HEARTS = chr(9829)  # Символ 9829 — '♥'.
DIAMONDS = chr(9830)  # Символ 9830 — '♦'.
SPADES = chr(9824)  # Символ 9824 — '♠'.
CLUBS = chr(9827)  # Символ 9827 — '♣'.
BACKSIDE = 'backside'


def main():
    print("""
    Правила:
1. Постарайтесь набрать как можно больше очков до 21-го, не превышая его.
2. Короли, дамы и валеты стоят 10 очков.
3. Тузы по желанию игрока считаются за 11 очков или за 1 очко.
4. Карты со 2 по 10 имеют номинальную стоимость.
5. Необходимо набрать карты с суммой очков, по возможности близкой к 21. 21 — это максимум, 
   перебор сразу же приводит к поражению.
6. Перед началом игры, игрок делает ставку.
7. Дилер останавливает игру при 17 набранных очках.
    """)

    money = 5000

    # Основной цикл игры.
    while True:
        if money <= 0:
            print('Вы на мели!')
            print('Хорошо что Вы играли не на настоящие деньги.')
            print('Спасибо за игру.')
            sys.exit()
    # Даём возможность игроку сделать ставку на раунд.
        print(f"Денег на счету: {money}$")
        bet = get_bet(money)

    # Сдаем дилеру и игроку по две карты из колоды.
        deck = get_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]

    # Обработка действий игрока.
        print(f'Ставка: {bet}')
        while True:  # Выполняем действие до тех пор, пока игрок не скажет "хватит" или у него не будет перебор.
            display_hands(player_hand, dealer_hand, False)
            print()
    # Проверка на перебор у игрока.
            if get_hand_value(player_hand) > 21:
                # Перебор у игрока.
                break
    # Получаем ход игрока: H, S или D.
            move = get_move(player_hand, money - bet)
    # Обработка действий игрока.
            if move == 'У':
                # Игрок удваивает, он может увеличить ставку.
                additional_bet = get_bet(min(bet, (money - bet)))
                bet += additional_bet
                print(f'Ставка увеличена до {bet}$')
                print(f'Ставка: {bet}')
            if move in ('Е', 'У'):  # Еще или 'удваиваю'. Игрок берет еще одну карту.
                new_card = deck.pop()
                rank, suit = new_card
                print(f'Ваша карта: {rank} {suit}')
                player_hand.append(new_card)

                if get_hand_value(player_hand) > 21:
                    continue

            if move in ('Х', 'У'):  # 'Хватит' или 'Удваиваю': переход хода к другому игроку.
                break

    # Обработка действий дилера.
        if get_hand_value(player_hand) < 21:
            while get_hand_value(dealer_hand) < 21:  # Дилер берет еще карту.
                print('Дилер делает ход...')
                dealer_hand.append(deck.pop())
                display_hands(player_hand, dealer_hand, False)

                if get_hand_value(dealer_hand) > 21:
                    # Перебор у дилера.
                    break
                input('Нажмите клавишу Enter что бы продолжить')
                print('\n\n')

    # Отображает игровые карты на руках.
        display_hands(player_hand, dealer_hand, True)
        player_value = get_hand_value(player_hand)
        dealer_value = get_hand_value(dealer_hand)
    # Проверяем: Игрок выиграл, проиграл или сыграл вничью.

        if dealer_value > 21:
            print(f'Дилер проиграл! Вы выиграли {bet}$')
            money += bet
        elif player_value > 21 or player_value < dealer_value:
            print(f'Вы проиграли!')
            money -= bet
        elif player_value > dealer_value:
            print(f'Вы выиграли {bet}$')
            money += bet
        elif player_value == dealer_value:
            print('Ничья! Ставка возвращается Вам')

        input('Нажмите клавишу Enter что бы продолжить')
        print('\n\n')


def get_bet(max_bet):
    """Спрашиваем у игрока, сколько он ставит на этот раунд."""
    while True:
        print(f'Сколько Вы готовы поставить? (1-{max_bet} или q - QUIT)')
        bet = input('>...').upper().strip()
        if bet == 'q':
            print('Спасибо за игру!')
            sys.exit()

    # Если игрок ничего не поставил, спрашиваем заново.
        if not bet.isdecimal():
            continue

    # Проверяем допустимое значение ставки.
        bet = int(bet)
        if 1 < bet <= max_bet:
            return bet


def get_deck():
    """Возвращаем список кортежей (номинал, масть) для всех 52 карт."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def display_hands(player_hand, dealer_hand, show_dealer_hand):
    """
    Отображаем карты игрока и дилера. Скрываем первую карту дилера,
    если showDealerHand равно False.
    """
    print()
    if show_dealer_hand:
        print(f'ДИЛЕР: {get_hand_value(dealer_hand)}')
        display_cards(dealer_hand)
    else:
        print('ДИЛЕР: ???')
    # Скрываем первую карту дилера.
        display_cards([BACKSIDE] + dealer_hand[1:])

    # Отображаем карту игрока.
    print(f'ИГРОК: {get_hand_value(player_hand)}')
    display_cards(player_hand)


def get_hand_value(cards):
    """
    Возвращаем стоимость карт. Фигурные карты стоят 10, тузы — 11
    или 1 очко (эта функция выбирает подходящую стоимость карты).
    """
    value = 0
    number_of_aces = 0

    # Добавляем стоимость карты - не туза.
    for card in cards:
        rank = card[0]  # карта представляет собой кортеж (номинал, масть)
        if rank == 'A':
            number_of_aces += 1
        elif rank in ('J', 'Q', 'K'):  # Фигурные карты стоят 10 очков.
            value += 10
        else:
            value += int(rank)  # Стоимость числовых карт равна их номиналу.

    # Добавляем стоимость номиналов для тузов.
    value += number_of_aces  # Добавляем 1 для каждого туза.
    for i in range(number_of_aces):
        # Если можно добавить еще 10 с перебором, добавляем:
        if value + 10 <= 21:
            value += 10
    return value


def display_cards(cards):
    """Отображаем все карты из списка карт."""
    rows = ['', '', '', '', '']  # Отображаемый в каждой строке текст.

    for i, card in enumerate(cards):
        rows[0] += ' ___ '  # Выводим верхнюю строку карты.
        if card == BACKSIDE:  # Выводим рубашку карты:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:  # Выводим лицевую сторону карты:
            rank, suit = card  # Карта — структура данных типа кортеж.
            rows[1] += f'|{rank}  |'
            rows[2] += f'| {suit} |'
            rows[3] += f'|  {rank}|'
        # Выводим все строки на экран:
        for row in rows:
            print(row)


def get_move(player_hand, money):
    """
    Спрашиваем, какой ход хочет сделать игрок, и возвращаем 'H', если он
    хочет взять еще карту, 'S', если ему хватит, и 'D', если он удваивает.
    """
    while True:  # Продолжаем итерации, пока игрок не сделает допустимый ход.
        moves = ['(Е)щё', '(Х)ватит']
        # Игрок может удвоить при первом ходе, это ясно из того, что у игрока ровно две карты:
        if len(player_hand) == 2 and money > 0:
            moves.append('(У)двоить')

        move_promt = ', '.join(moves) + '> '
        move = input(move_promt).upper()
        if move in ('Е', 'Х'):
            return move
        if move == 'У' and '(У)двоить' in moves:
            return move


if __name__ == '__main__':
    main()

import random


CARD_NUMBERS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["하트", "다이아", "스페이드", "클로버"]
JOKER = "도둑"


def make_deck():
    deck = []

    for number in CARD_NUMBERS:
        for suit in CARD_SUITS:
            deck.append(f"{suit} {number}")

    deck.append(JOKER)
    random.shuffle(deck)
    return deck


def card_number(card):
    if card == JOKER:
        return JOKER
    return card.split()[-1]


def remove_pairs(hand):
    counts = {}
    result = []

    for card in hand:
        number = card_number(card)
        counts[number] = counts.get(number, 0) + 1

    removed_numbers = set()
    for number, count in counts.items():
        if number != JOKER and count >= 2:
            removed_numbers.add(number)

    for card in hand:
        if card_number(card) not in removed_numbers:
            result.append(card)

    return result


def show_hand(hand):
    print()
    print("내 카드")
    for index, card in enumerate(hand, start=1):
        print(f"{index}. {card}")


def draw_card(drawer, target, target_name):
    if len(target) == 0:
        return

    print()
    print(f"{target_name}의 카드 중 하나를 뽑습니다.")

    while True:
        try:
            choice = int(input(f"몇 번째 카드를 뽑을까요? (1~{len(target)}): "))
            if 1 <= choice <= len(target):
                break
            print("범위 안의 숫자를 입력하세요.")
        except ValueError:
            print("숫자로 입력하세요.")

    picked_card = target.pop(choice - 1)
    drawer.append(picked_card)
    print(f"뽑은 카드: {picked_card}")


def computer_draw(drawer, target):
    if len(target) == 0:
        return

    index = random.randrange(len(target))
    picked_card = target.pop(index)
    drawer.append(picked_card)
    print()
    print("컴퓨터가 내 카드 중 하나를 뽑았습니다.")


def play_game():
    deck = make_deck()
    user_hand = deck[: len(deck) // 2]
    computer_hand = deck[len(deck) // 2 :]

    user_hand = remove_pairs(user_hand)
    computer_hand = remove_pairs(computer_hand)

    print()
    print("도둑잡기 게임을 시작합니다.")
    print("같은 숫자 카드는 자동으로 버립니다.")

    turn = "user"

    while user_hand and computer_hand:
        if turn == "user":
            show_hand(user_hand)
            print(f"컴퓨터 카드 수: {len(computer_hand)}")
            draw_card(user_hand, computer_hand, "컴퓨터")
            user_hand = remove_pairs(user_hand)
            turn = "computer"
        else:
            computer_draw(computer_hand, user_hand)
            computer_hand = remove_pairs(computer_hand)
            turn = "user"

    print()
    if len(user_hand) == 0:
        print("승리! 내 카드가 먼저 없어졌습니다.")
        return "win"

    print("패배! 마지막까지 도둑 카드를 가지고 있습니다.")
    return "lose"


def start_game(player_info):
    print()
    print(f"[도둑잡기] {player_info['name']}님, 게임을 시작합니다!")

    while True:
        result = play_game()

        if result == "win":
            player_info["chips"] += 20
            print("보상으로 칩 20개를 얻었습니다.")
        else:
            player_info["chips"] = max(0, player_info["chips"] - 10)
            print("칩 10개를 잃었습니다.")

        print(f"현재 칩: {player_info['chips']}개")

        again = input("도둑잡기를 다시 하시겠습니까? (y/n): ").strip().lower()
        if again != "y":
            print("도둑잡기를 종료하고 로비로 돌아갑니다.")
            return player_info


def start_thief_card(player_info):
    return start_game(player_info)


if __name__ == "__main__":
    test_player = {"name": "Player 1", "chips": 100}
    start_game(test_player)

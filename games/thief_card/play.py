import random

 feature/old-maid
from core.card import Deck


class ThiefCard:
    rank = "THIEF"

    def __str__(self):
        return "도둑"


def make_old_maid_deck():
    deck = Deck()
    cards = [deck.draw() for _ in range(len(deck))]
    cards.append(ThiefCard())
    random.shuffle(cards)
    return cards


def card_rank(card):
    return card.rank


def remove_pairs(hand):
    rank_groups = {}
    remaining_hand = []
    removed_count = 0

    for card in hand:
        rank_groups.setdefault(card_rank(card), []).append(card)

    for rank, cards in rank_groups.items():
        if rank == "THIEF":
            remaining_hand.extend(cards)
            continue

        pair_count = len(cards) // 2
        removed_count += pair_count * 2
        remaining_hand.extend(cards[pair_count * 2 :])

    random.shuffle(remaining_hand)
    return remaining_hand, removed_count


def create_players():
    return [
        {"name": "나", "hand": [], "is_human": True, "out": False},
        {"name": "컴퓨터1", "hand": [], "is_human": False, "out": False},
        {"name": "컴퓨터2", "hand": [], "is_human": False, "out": False},
        {"name": "컴퓨터3", "hand": [], "is_human": False, "out": False},
    ]


def deal_cards(cards, players):
    for index, card in enumerate(cards):
        players[index % len(players)]["hand"].append(card)


def remove_starting_pairs(players):
    for player in players:
        player["hand"], removed_count = remove_pairs(player["hand"])
        print(f"{player['name']} 시작 짝 제거: {removed_count}장")
        if len(player["hand"]) == 0:
            player["out"] = True
            print(f"{player['name']}은(는) 시작하자마자 모든 카드를 버렸습니다.")


def display_status(players):
    print("\n--- 현재 카드 수 ---")
    for player in players:
        status = "탈출" if player["out"] else f"{len(player['hand'])}장"
        print(f"{player['name']}: {status}")
    print("-------------------")


def display_player_hand(hand):
    print("\n--- 나의 카드 ---")
    for index, card in enumerate(hand, start=1):
        print(f"{index}. {card}")
    print("----------------")


def active_players(players):
    return [player for player in players if not player["out"]]


def next_active_index(players, current_index):
    for offset in range(1, len(players) + 1):
        candidate_index = (current_index + offset) % len(players)
        if not players[candidate_index]["out"]:
            return candidate_index
    return None


def ask_human_card_index(target):
    while True:
        choice = input(
            f"{target['name']}의 카드 중 몇 번째를 뽑을까요? "
            f"(1~{len(target['hand'])}, q: 중단): "
        ).strip().lower()

        if choice == "q":
            return None

        try:
            card_index = int(choice) - 1
            if 0 <= card_index < len(target["hand"]):
                return card_index
            print("범위 안의 숫자를 입력해 주세요.")
        except ValueError:
            print("숫자 또는 q를 입력해 주세요.")


def draw_card(current_player, target_player):
    if current_player["is_human"]:
        display_player_hand(current_player["hand"])
        print(f"\n이번에는 {target_player['name']}의 카드를 뽑습니다.")
        card_index = ask_human_card_index(target_player)
        if card_index is None:
            return "quit"
    else:
        card_index = random.randrange(len(target_player["hand"]))
        print(f"\n{current_player['name']}이(가) {target_player['name']}의 카드 한 장을 뽑았습니다.")

    picked_card = target_player["hand"].pop(card_index)
    current_player["hand"].append(picked_card)

    if current_player["is_human"]:
        print(f"뽑은 카드: {picked_card}")

    return "continue"


def settle_player_after_turn(player):
    player["hand"], removed_count = remove_pairs(player["hand"])

    if removed_count:
        print(f"{player['name']}이(가) 같은 숫자 카드 {removed_count}장을 버렸습니다.")

    if len(player["hand"]) == 0:
        player["out"] = True
        print(f"{player['name']} 탈출! 손에 남은 카드가 없습니다.")


def play_round():
    players = create_players()
    cards = make_old_maid_deck()
    deal_cards(cards, players)

    print("\n♣ 4인 도둑잡기 게임을 시작합니다! ♣")
    print("참가자: 나, 컴퓨터1, 컴퓨터2, 컴퓨터3")
    print("공용 카드 덱(core.card.Deck) 52장에 도둑 카드 1장을 추가했습니다.")
    remove_starting_pairs(players)

    current_index = 0

    while len(active_players(players)) > 1:
        current_player = players[current_index]

        if current_player["out"]:
            next_index = next_active_index(players, current_index)
            if next_index is None:
                break
            current_index = next_index
            continue

        target_index = next_active_index(players, current_index)
        if target_index is None:
            break

        target_player = players[target_index]
        display_status(players)
        print(f"\n현재 차례: {current_player['name']}")

        draw_result = draw_card(current_player, target_player)
        if draw_result == "quit":
            return "quit"

        if len(target_player["hand"]) == 0:
            target_player["out"] = True
            print(f"{target_player['name']} 탈출! 손에 남은 카드가 없습니다.")

        settle_player_after_turn(current_player)
        current_index = next_active_index(players, current_index) or current_index

    remaining_players = active_players(players)
    if not remaining_players:
        return "draw"

    loser = remaining_players[0]
    print(f"\n마지막까지 남은 사람: {loser['name']}")
    return "lose" if loser["is_human"] else "win"


def get_bet(player_info):
    if player_info["chips"] <= 0:
        print("칩이 부족합니다! 로비에서 다시 시작해 주세요.")
        return None

    while True:
        try:
            bet = int(input(f"배팅할 칩을 입력하세요 (보유: {player_info['chips']}): "))
            if 0 < bet <= player_info["chips"]:
                return bet
            print("보유한 칩 범위 안에서 1개 이상 입력해 주세요.")
        except ValueError:
            print("숫자만 입력 가능합니다.")


def start_game(player_info):
    print(f"\n{player_info['name']}님, 4인 도둑잡기 게임을 시작합니다.")

    bet = get_bet(player_info)
    if bet is None:
        return player_info

    result = play_round()
    chip_change = 0

    if result == "quit":
        print("\n게임을 중단했습니다. 칩은 변동되지 않습니다.")
    elif result == "win":
        print("\n승리! 나는 도둑 카드에서 살아남았습니다.")
        chip_change = bet
        player_info["chips"] += bet
    elif result == "lose":
        print("\n패배! 내가 마지막까지 도둑 카드를 가지고 있습니다.")
        chip_change = -bet
        player_info["chips"] -= bet
    else:
        print("\n무승부입니다. 칩은 변동되지 않습니다.")

    print("\n--- 정산 결과 ---")
    print(f"배팅 칩: {bet}개")
    print(f"이번 판 결과: {chip_change:+}개")
    print(f"최종 보유 칩: {player_info['chips']}개")
    print("----------------")
    input("\n[Enter]를 누르면 메인 로비로 돌아갑니다...")
    return player_info


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
 main


if __name__ == "__main__":
    test_player = {"name": "Player 1", "chips": 100}
    start_game(test_player)

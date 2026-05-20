import random
import time

class ThiefCard:
    rank = "THIEF"

    def __str__(self):
        return "🃏도둑"

def make_old_maid_deck():
    from core.card import Deck
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
    print("\n[게임 시작 전] 모두 손패에서 짝이 맞는 카드를 버립니다...")
    time.sleep(1.5)
    for player in players:
        player["hand"], removed_count = remove_pairs(player["hand"])
        print(f"✨ {player['name']}: {removed_count}장 폐기 완료 (남은 카드: {len(player['hand'])}장)")
        time.sleep(0.5)
        if len(player["hand"]) == 0:
            player["out"] = True
            print(f"🎉 {player['name']}은(는) 시작하자마자 프리패스 탈출!")

def display_status(players):
    print("\n================ 테이블 현황 ================")
    status_list = []
    for player in players:
        status = "👑 탈출" if player["out"] else f"[{len(player['hand'])}장]"
        status_list.append(f"{player['name']}: {status}")
    print(" | ".join(status_list))
    print("=============================================")

def display_player_hand(hand):
    print("\n🔮 [나의 현재 손패]")
    for index, card in enumerate(hand, start=1):
        print(f"  {index}. {card}")
    print("---------------------------------------------")

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
            f"👉 {target['name']}의 카드 중 몇 번째 카드를 뽑을까요? "
            f"(1~{len(target['hand'])}, q: 중단): "
        ).strip().lower()

        if choice == "q":
            return None

        try:
            card_index = int(choice) - 1
            if 0 <= card_index < len(target["hand"]):
                return card_index
            print("❌ 올바른 카드 번호를 선택해 주세요.")
        except ValueError:
            print("❌ 숫자 또는 q를 입력해 주세요.")

def draw_card(current_player, target_player):
    if current_player["is_human"]:
        display_player_hand(current_player["hand"])
        print(f"⚔️  내 차례입니다! {target_player['name']}의 카드를 뺏어옵니다.")
        card_index = ask_human_card_index(target_player)
        if card_index is None:
            return "quit"
    else:
        print(f"🎲 {current_player['name']}이(가) 신중하게 {target_player['name']}의 카드를 고르는 중...")
        time.sleep(2.0)
        card_index = random.randrange(len(target_player["hand"]))

    picked_card = target_player["hand"].pop(card_index)
    current_player["hand"].append(picked_card)

    if current_player["is_human"]:
        print(f"\n🔥 [결과] {target_player['name']}에게서 [{picked_card}] 카드를 뽑아왔습니다!")
    else:
        print(f"\n🔥 [결과] {current_player['name']}(이)가 {target_player['name']}의 {card_index + 1}번째 카드를 뺏어갔습니다!")
    
    time.sleep(1.5)
    return "continue"

def settle_player_after_turn(player):
    player["hand"], removed_count = remove_pairs(player["hand"])

    if removed_count:
        print(f"✨ {player['name']}이(가) 같은 숫자 짝 [{removed_count}장]을 바닥에 버렸습니다!")
        time.sleep(1.5)

    if len(player["hand"]) == 0:
        player["out"] = True
        print(f"🎉 👑 {player['name']} 탈출 성공! 손에 남은 카드가 없습니다!")
        time.sleep(1.5)

def play_round():
    players = create_players()
    cards = make_old_maid_deck()
    deal_cards(cards, players)

    print("\n♣ 4인 도둑잡기 게임을 시작합니다! ♣")
    print("참가자: 나, 컴퓨터1, 컴퓨터2, 컴퓨터3")
    print("52장 덱에 '도둑(🃏)' 카드 1장이 추가되었습니다.")
    
    remove_starting_pairs(players)
    input("\n[Enter]를 누르면 본격적인 라운드를 시작합니다!")

    current_index = 0

    while len(active_players(players)) > 1:
        current_player = players[current_index]

        if current_player["out"]:
            current_index = next_active_index(players, current_index)
            continue

        target_index = next_active_index(players, current_index)
        if target_index is None:
            break

        target_player = players[target_index]
        
        display_status(players)
        print(f"\n📢 현재 턴: {current_player['name']} -> 대상: {target_player['name']}")
        print("-" * 45)

        draw_result = draw_card(current_player, target_player)
        if draw_result == "quit":
            return "quit"

        if len(target_player["hand"]) == 0:
            target_player["out"] = True
            print(f"🎉 👑 카드를 빼앗긴 {target_player['name']}이(가) 강제 탈출 성공!")
            time.sleep(1.5)

        settle_player_after_turn(current_player)
        
        if not current_player["is_human"]:
            input("\n[Enter] 다음 턴 보기...")
            
        current_index = next_active_index(players, current_index) or current_index

    remaining_players = active_players(players)
    if not remaining_players:
        return "draw"

    loser = remaining_players[0]
    print("\n=============================================")
    print(f"💀 게임 종료! 마지막까지 도둑을 쥐고 있는 패배자: {loser['name']}")
    print("=============================================")
    return "lose" if loser["is_human"] else "win"

def start_game(player_info):
    print(f"\n{player_info['name']}님, 4인 도둑잡기 게임 룸에 입장하셨습니다.")

    result = play_round()

    if result == "quit":
        print("\n게임을 중단했습니다. 칩은 유지됩니다.")
    elif result == "win":
        print("\n🏆 승리! 도둑을 다른 컴퓨터에게 무사히 떠넘기고 살아남았습니다!")
        player_info["chips"] += 20
        print("💰 보상으로 칩 20개를 획득했습니다.")
    elif result == "lose":
        print("\n😭 패배! 마지막까지 도둑 카드를 들고 파멸했습니다.")
        player_info["chips"] = max(0, player_info["chips"] - 10)
        print("💸 칩 10개를 잃었습니다.")
    else:
        print("\n🤝 무승부입니다. 칩 변동이 없습니다.")

    print(f"🏦 보유 칩 현황: {player_info['chips']}개")
    input("\n[Enter]를 누르면 메인 로비로 돌아갑니다...")
    return player_info

# 로비(main.py) 진입용 함수
def start_thief_card(player_info):
    return start_game(player_info)
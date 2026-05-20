# games/blackjack/play.py
import time  # 딜러가 카드를 한 장씩 뽑는 연출을 위한 시간 딜레이 추가
from core.card import Deck

def calculate_score(hand):
    """보유한 카드의 블랙잭 점수를 계산하는 함수"""
    score = 0
    aces = 0
    
    for card in hand:
        if card.rank in ['J', 'Q', 'K']:
            score += 10
        elif card.rank == 'A':
            score += 11
            aces += 1
        else:
            score += int(card.rank)
            
    # 에이스(A) 조정: 총점이 21을 넘으면 A를 1점짜리로 취급
    while score > 21 and aces:
        score -= 10
        aces -= 1
        
    return score

def display_hands(player_hand, dealer_hand, hide_dealer=True):
    """현재 플레이어와 딜러의 카드를 출력"""
    print("\n--- 현재 카드 상황 ---")
    if hide_dealer:
        print(f"딜러의 카드: [{dealer_hand[0]}], [ ? ]")
    else:
        print(f"딜러의 카드: {', '.join(str(c) for c in dealer_hand)} (점수: {calculate_score(dealer_hand)})")
        
    print(f"나의 카드  : {', '.join(str(c) for c in player_hand)} (점수: {calculate_score(player_hand)})")
    print("----------------------")

def start_blackjack(player_info):
    """메인 로비에서 호출할 블랙잭 메인 함수"""
    print("\n♠ 블랙잭 게임을 시작합니다! ♠")
    
    if player_info['chips'] <= 0:
        print("칩이 부족합니다! 로비에서 충전(재시작)이 필요합니다.")
        return player_info

    # 1. 배팅 단계
    while True:
        try:
            bet = int(input(f"배팅할 칩을 입력하세요 (보유: {player_info['chips']}): "))
            if 0 < bet <= player_info['chips']:
                break
            print("보유한 칩 범위 내에서 올바르게 입력해 주세요.")
        except ValueError:
            print("숫자만 입력 가능합니다.")

    # 2. 게임 초기화 및 첫 카드 분배
    deck = Deck()
    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]
    
    # 3. 플레이어 턴 (Hit or Stand)
    player_burst = False
    while True:
        display_hands(player_hand, dealer_hand, hide_dealer=True)
        player_score = calculate_score(player_hand)
        
        if player_score == 21:
            print("블랙잭! (또는 21점 달성)")
            break
        elif player_score > 21:
            print("버스트(Bust)! 21점을 초과했습니다.")
            player_burst = True
            break
            
        action = input("카드를 더 받으시겠습니까? (1: Hit / 2: Stand): ").strip()
        if action == '1':
            player_hand.append(deck.draw())
        elif action == '2':
            break
        else:
            print("잘못된 입력입니다.")

    # 이번 판의 정산 결과를 저장할 변수
    net_result = 0 

    # 4. 딜러 턴 및 결과 판정
    if not player_burst:
        player_score = calculate_score(player_hand)
        print("\n--- 딜러의 턴 ---")
        time.sleep(1)
        
        # 딜러의 숨겨진 카드를 먼저 오픈하며 시작합니다.
        print("딜러가 카드를 공개합니다...")
        display_hands(player_hand, dealer_hand, hide_dealer=False)
        time.sleep(1.5)
        
        # 딜러는 점수가 17점 이상이 될 때까지 '한 장씩' 받으며 상황을 계속 보여줍니다.
        while calculate_score(dealer_hand) < 17:
            print("\n딜러의 점수가 17점 미만입니다. 카드를 한 장 더 받습니다... 🎴")
            time.sleep(1.5)  # 1.5초 멈춰서 긴장감 조성
            
            new_card = deck.draw()
            dealer_hand.append(new_card)
            print(f"-> 딜러가 뽑은 카드: [{new_card}]")
            
            # 카드를 뽑을 때마다 현재 딜러의 전체 카드 상황 업데이트 출력
            display_hands(player_hand, dealer_hand, hide_dealer=False)
            time.sleep(1.5)
            
        dealer_score = calculate_score(dealer_hand)
        print("\n--- 최종 결과 판정 ---")
        
        if dealer_score > 21:
            print("딜러 버스트! 당신이 승리했습니다! 🎉")
            player_info['chips'] += bet
            net_result = bet
        elif player_score > dealer_score:
            print("당신이 더 높은 점수로 승리했습니다! 🎉")
            player_info['chips'] += bet
            net_result = bet
        elif player_score < dealer_score:
            print("딜러가 승리했습니다. 😢")
            player_info['chips'] -= bet
            net_result = -bet
        else:
            print("비겼습니다! (Push) 칩이 반환됩니다.")
            net_result = 0
    else:
        # 플레이어 버스트 시 즉시 패배
        display_hands(player_hand, dealer_hand, hide_dealer=False)
        print("당신이 패배했습니다. 😢")
        player_info['chips'] -= bet
        net_result = -bet

    # 💰 딴 칩/잃은 칩 전용 정산 화면 출력 구역
    print("\n==============================")
    if net_result > 0:
        print(f"💰 이번 판 결과: +{net_result} 칩을 획득했습니다! 🎉")
    elif net_result < 0:
        print(f"💸 이번 판 결과: {net_result} 칩을 잃었습니다. 😢")
    else:
        print("🤝 이번 판 결과: 칩 변동이 없습니다. (무승부)")
    
    print(f"🏦 최종 보유 칩: {player_info['chips']} 칩")
    print("==============================")
    
    # 다시 로비로 돌아갈 때 갱신된 플레이어 정보를 반환함
    input("\n[Enter]를 누르면 메인 로비로 돌아갑니다...")
    return player_info
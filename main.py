import os
from datetime import datetime

# 각 게임 모듈 임포트
from games.blackjack.play import start_blackjack
from games.thief_card.play import start_thief_card

HOF_FILE = "hall_of_fame.txt"

def load_hall_of_fame():
    """명예의 전당 목록을 불러오는 함수"""
    if not os.path.exists(HOF_FILE):
        return []
    with open(HOF_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_to_hall_of_fame(player_name):
    """명예의 전당에 플레이어 이름을 기록하는 함수"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(HOF_FILE, "a", encoding="utf-8") as f:
        f.write(f"👑 {player_name} - 200 칩 달성! ({current_time})\n")

def display_hall_of_fame():
    """명예의 전당 출력 화면"""
    print("\n================ 🏆 명예의 전당 🏆 ================")
    records = load_hall_of_fame()
    if not records:
        print("  아직 명예의 전당에 등록된 전설이 없습니다.")
        print("  첫 번째 주인공이 되어보세요!")
    else:
        for idx, record in enumerate(records, start=1):
            print(f" {idx}. {record}")
    print("==================================================")
    input("\n[Enter]를 누르면 메인 메뉴로 돌아갑니다...")

def check_victory_condition(player_info):
    """게임 종료 후 200칩 달성 여부를 체크하는 핵심 로직"""
    if player_info["chips"] >= 200:  # 🎯 목표치 200으로 전격 하향 조정!
        print("\n🎉🎉🎉 축하합니다! 🎉🎉🎉")
        print(f"목표치인 200 칩을 달성하셨습니다! (현재 보유: {player_info['chips']} 칩)")
        print("카지노를 정복한 전설로 인정받아 '명예의 전당'에 이름을 올릴 수 있습니다.")
        
        # 이름 입력 받기
        while True:
            name = input("✍️ 명예의 전당에 새길 이름을 입력하세요: ").strip()
            if name:
                break
            print("이름은 최소 한 글자 이상 입력해 주세요.")
        
        save_to_hall_of_fame(name)
        print(f"\n✨ [{name}] 님의 이름이 명예의 전당에 영원히 기록되었습니다!")
        
        print("🏆 목표를 달성했으므로 기념으로 칩이 100개로 재설정됩니다.")
        player_info["chips"] = 100
        input("\n[Enter]를 누르면 메인 메뉴로 이동합니다...")
    return player_info

def main():
    # 플레이어 초기 정보 세팅 (기본 100칩 시작)
    player_info = {"name": "Player", "chips": 100}

    while True:
        print("\n================ 🎰 카드 게임 트리플 패키지 🎰 ================")
        print(f"  현재 보유 칩: 💰 {player_info['chips']} 개  |  🎯 목표: 🏆 200 칩 달성")
        print("------------------------------------------------------------")
        print("  1. ♠ 블랙잭 (Blackjack)")
        print("  2. 🃏 4인 도둑잡기 (Old Maid)")
        print("  3. 🏦 칩 충전소 (재시작시 100칩 지급)")
        print("  4. 🏆 명예의 전당 보기")
        print("  Q. 게임 완전히 종료하기")
        print("================================================------------")
        
        choice = input("👉 원하시는 메뉴 번호를 입력하세요: ").strip().lower()

        if choice == "1":
            player_info = start_blackjack(player_info)
            player_info = check_victory_condition(player_info)

        elif choice == "2":
            player_info = start_thief_card(player_info)
            player_info = check_victory_condition(player_info)

        elif choice == "3":
            if player_info["chips"] <= 0:
                player_info["chips"] = 100
                print("\n🔋 칩 충전 완료! 다시 100 칩으로 도전을 시작합니다.")
            else:
                print(f"\n⚠️ 아직 칩이 남아있습니다! (현재: {player_info['chips']}개)")
                print("칩을 모두 잃었을 때만 충전소를 이용하실 수 있습니다.")
            input("\n[Enter] 계속...")

        elif choice == "4":
            display_hall_of_fame()

        elif choice == "q":
            print("\n👋 게임 패키지를 종료합니다. 방문해 주셔서 감사합니다!")
            break
        else:
            print("\n❌ 잘못된 입력입니다. 메뉴에 있는 번호나 Q를 입력해 주세요.")

if __name__ == "__main__":
    main()
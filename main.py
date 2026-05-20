import os
from datetime import datetime

from games.blackjack.play import start_blackjack
from games.thief_card.play import start_game as start_thief_card
from games.stock_fake_news.play import start_game as start_stock_fake_news
from games.indian_poker.indian_poker import IndianPoker


HOF_FILE = "hall_of_fame.txt"
TARGET_CHIPS = 200
STARTING_CHIPS = 100


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
        f.write(f"👑 {player_name} - {TARGET_CHIPS} 칩 달성! ({current_time})\n")


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
    """게임 종료 후 목표 칩 달성 여부를 체크하는 로직"""
    if player_info["chips"] < TARGET_CHIPS:
        return player_info

    print("\n🎉🎉🎉 축하합니다! 🎉🎉🎉")
    print(f"목표치인 {TARGET_CHIPS} 칩을 달성하셨습니다! (현재 보유: {player_info['chips']} 칩)")
    print("카지노를 정복한 전설로 인정받아 '명예의 전당'에 이름을 올릴 수 있습니다.")

    while True:
        name = input("✍️ 명예의 전당에 새길 이름을 입력하세요: ").strip()
        if name:
            break
        print("이름은 최소 한 글자 이상 입력해 주세요.")

    save_to_hall_of_fame(name)
    print(f"\n✨ [{name}] 님의 이름이 명예의 전당에 영원히 기록되었습니다!")
    print(f"🏆 목표를 달성했으므로 기념으로 칩이 {STARTING_CHIPS}개로 재설정됩니다.")
    player_info["chips"] = STARTING_CHIPS
    input("\n[Enter]를 누르면 메인 메뉴로 이동합니다...")
    return player_info


def main():
    print("=" * 40)
    print("      ♠◆♥♣ 파이썬 카드 게임 미니 로비 ♣♥◆♠")
    print("=" * 40)

    user_name = input("플레이어 이름을 입력하세요: ").strip()
    if not user_name:
        user_name = "Player 1"

    player_info = {"name": user_name, "chips": STARTING_CHIPS}
    print(f"\n환영합니다, {player_info['name']}님! 초기 칩 {STARTING_CHIPS}개가 지급되었습니다.")

    while True:
        print("\n" + "-" * 40)
        print(f"[ 현재 자산: {player_info['chips']} 칩 | 목표: {TARGET_CHIPS} 칩 ]")
        print("1. 블랙잭")
        print("2. 인디언 포커")
        print("3. 도둑잡기")
        print("4. 주식 가짜 뉴스 판별게임")
        print("5. 칩 충전소")
        print("6. 명예의 전당 보기")
        print("0. 게임 종료")
        print("-" * 40)

        choice = input("플레이할 게임 번호를 선택하세요: ").strip()

        if choice == "1":
            player_info = start_blackjack(player_info)
            player_info = check_victory_condition(player_info)
        elif choice == "2":
            game = IndianPoker()
            player_info = game.play(player_info)
            player_info = check_victory_condition(player_info)
        elif choice == "3":
            player_info = start_thief_card(player_info)
            player_info = check_victory_condition(player_info)
        elif choice == "4":
            player_info = start_stock_fake_news(player_info)
            player_info = check_victory_condition(player_info)
        elif choice == "5":
            if player_info["chips"] <= 0:
                player_info["chips"] = STARTING_CHIPS
                print(f"\n🔋 칩 충전 완료! 다시 {STARTING_CHIPS} 칩으로 도전을 시작합니다.")
            else:
                print(f"\n⚠️ 아직 칩이 남아있습니다! (현재: {player_info['chips']}개)")
                print("칩을 모두 잃었을 때만 충전소를 이용하실 수 있습니다.")
            input("\n[Enter] 계속...")
        elif choice == "6":
            display_hall_of_fame()
        elif choice == "0":
            print("\n게임을 종료합니다. 방문해 주셔서 감사합니다!")
            break
        else:
            print("\n[오류] 잘못된 선택입니다. 다시 선택해 주세요.")


if __name__ == "__main__":
    main()

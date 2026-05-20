# main.py
import sys
# 팀원들의 게임 폴더 연결 (추후 팀원들이 완성하면 import 가능)
from games.blackjack.play import start_blackjack
from games.thief_card.play import start_game as start_thief_card
from games.stock_fake_news.play import start_game as start_stock_fake_news
from games.indian_poker.indian_poker import IndianPoker
def main():
    print("=" * 40)
    print("      ♠◆♥♣ 파이썬 카드 게임 미니 로비 ♣♥◆♠")
    print("=" * 40)
    
    # 간단한 플레이어 정보 세팅 (연결성을 위해)
    user_name = input("플레이어 이름을 입력하세요: ").strip()
    if not user_name:
        user_name = "Player 1"
        
    player_info = {"name": user_name, "chips": 100}
    print(f"\n환영합니다, {player_info['name']}님! 초기 칩 100개가 지급되었습니다.")

    while True:
        print("\n" + "-" * 30)
        print(f"[ 현재 자산: {player_info['chips']} 칩 ]")
        print("1. 블랙잭")
        print("2. 인디언 포커")
        print("3. 도둑잡기")
        print("4. 주식 가짜 뉴스 판별게임")
        print("0. 게임 종료")
        print("-" * 30)
        
        choice = input("플레이할 게임 번호를 선택하세요: ").strip()
        
        if choice == '1':
            # 블랙잭 실행 (플레이어 정보를 넘겨주어 칩이 연동되도록 함)
            player_info = start_blackjack(player_info)
        elif choice == '2':

            game = IndianPoker()

            player_info = game.play(
                player_info
            )
        elif choice == '3':
            player_info = start_thief_card(player_info)
        elif choice == '4':
            player_info = start_stock_fake_news(player_info)
        elif choice == '0':
            print("\n게임을 종료합니다. 방문해 주셔서 감사합니다!")
            sys.exit()
        else:
            print("\n[오류] 잘못된 선택입니다. 다시 선택해 주세요.")

if __name__ == "__main__":
    main()
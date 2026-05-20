from core.card import Deck


class IndianPoker:

    def __init__(self):

        self.deck = Deck()

    def card_value(self, rank):

        if rank == "A":
            return 1

        elif rank == "J":
            return 11

        elif rank == "Q":
            return 12

        elif rank == "K":
            return 13

        else:
            return int(rank)

    def play(self, player_info):

        print("\n♣ 인디언 포커를 시작합니다! ♣")

        # 1. 칩 보유 체크
        if player_info['chips'] <= 0:

            print(
                "칩이 부족합니다!"
            )

            return player_info

        # 2. 배팅 입력
        while True:

            try:

                bet = int(
                    input(
                        f"배팅할 칩 입력 "
                        f"(보유: "
                        f"{player_info['chips']}): "
                    )
                )

                if (
                    0 < bet <=
                    player_info[
                        'chips'
                    ]
                ):

                    break

                print(
                    "보유 칩 범위 "
                    "내 입력"
                )

            except ValueError:

                print(
                    "숫자만 "
                    "입력 가능"
                )

        # 카드 뽑기
        player = self.deck.draw()

        computer = self.deck.draw()

        print(
            "\n상대 카드"
        )

        print(computer)

        action = input(
            "\n1 체크\n"
            "2 레이즈\n"
            "3 폴드\n"
            "입력 : "
        )

        # 폴드
        if action == "3":

            result = "lose"

        else:

            print(
                "\n내 카드"
            )

            print(player)

            print(
                "\n컴퓨터 카드"
            )

            print(computer)

            player_score = (
                self.card_value(
                    player.rank
                )
            )

            computer_score = (
                self.card_value(
                    computer.rank
                )
            )

            if (
                player_score >
                computer_score
            ):

                result = "win"

            elif (
                player_score <
                computer_score
            ):

                result = "lose"

            else:

                result = "draw"

        # 4. 칩 정산
        print(
            "\n=========="
            "=========="
        )

        if result == "win":

            player_info[
                'chips'
            ] += bet

            print(
                f"💰 결과 "
                f"+{bet}"
            )

        elif result == "lose":

            player_info[
                'chips'
            ] -= bet

            print(
                f"💸 결과 "
                f"-{bet}"
            )

        else:

            print(
                "🤝 무승부"
            )

        print(
            f"🏦 최종 칩 : "
            f"{player_info['chips']}"
        )

        print(
            "=========="
            "=========="
        )

        return player_info
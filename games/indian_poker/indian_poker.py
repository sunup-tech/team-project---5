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

    def play(self):

        print("=== 인디언 포커 ===")

        player = self.deck.draw()

        computer = self.deck.draw()

        print("\n상대 카드")

        print(computer)

        action = input(
            "\n1 체크\n"
            "2 레이즈\n"
            "3 폴드\n"
            "입력 : "
        )

        if action == "3":

            print("패배")

            return

        print("\n내 카드")

        print(player)

        print("\n컴퓨터 카드")

        print(computer)

        player_score = self.card_value(
            player.rank
        )

        computer_score = self.card_value(
            computer.rank
        )

        if player_score > computer_score:

            print("승리")

        elif player_score < computer_score:

            print("패배")

        else:

            print("무승부")
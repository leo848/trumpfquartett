import json
import random
import time
from sys import exit

import colors
from card import Card


class Game:
    card_stack: list[Card]
    player_names: list[str]
    player_stacks: list[list[Card]]
    amount: int

    def ask_for_names(self):
        self.color_codes = (99 + random.randrange(0, 10), 37)
        self.player_names = []
        self.amount = int(input("Wie viele Spieler wollen spielen? "))
        if self.amount < 2:
            print(
                "Zu wenige Spieler (du kannst auch 2 auswählen und gegen dich selbst spielen)"
            )
            exit(1)
        for i in range(self.amount):
            self.player_names.append(
                input(
                    f"Gib den Namen von {colors.color(self.color_codes[0]+i*self.color_codes[1])}Spieler {i+1}{colors.END} ein: "
                )
            )

    def create_stack(self):
        self.card_stack = list()

        with open("data.json") as f:
            game_cards = json.load(f)

        for card in game_cards:
            self.card_stack.append(
                Card(
                    title=card["title"],
                    height=card["height"],
                    weight=card["weight"],
                    age=card["age"],
                )
            )

    def shuffle_stack(self):
        random.shuffle(self.card_stack)

    def distribute_cards(self):
        while self.card_stack.__len__() % self.amount:
            self.card_stack.pop()
        self.player_stacks = [[] for _ in range(self.amount)]
        for i, card in enumerate(self.card_stack):
            self.player_stacks[i % self.amount].append(card)

    def player_str(self, idx):
        sequence = (
            colors.BOLD
            + colors.color(
                colors.color(self.color_codes[0] + idx * self.color_codes[1])
            )[:-1]
            + self.player_names[idx]
            + colors.END
        )
        return sequence

    def play(self):
        self.ask_for_names()
        self.create_stack()
        self.shuffle_stack()
        self.distribute_cards()

        current_player = random.randrange(0, self.amount)

        while self.amount > 1:
            player_name = self.player_names[current_player]
            player_card = self.player_stacks[current_player][-1]

            print()
            # print(
            #     colors.color(242)
            #     + " - ".join(
            #         [card.title for card in self.player_stacks[current_player][-4:-2]][ ::-1 ]
            #     )
            #     + colors.END
            # )
            print(
                f"{self.player_str(current_player)}, du bist dran. Du hast die folgende Karte (von {self.player_stacks[current_player].__len__()}):"
            )
            print(player_card)
            attr = {"a": "height", "b": "weight", "c": "age"}[
                input(f"Wähle eines der Attribute mithilfe des Buchstabens: ")
            ]
            values = [(current_player, getattr(player_card, attr))]

            print("\n" * 2)

            for player in range(self.amount):
                if player == current_player:
                    continue
                card = self.player_stacks[player][-1]
                value = getattr(card, attr)
                values.append((player, value))

                time.sleep(0.2)
                print(
                    f"{self.player_str(player)} hat: {card.title} - {card.attr_str(attr)}"
                )
            print()

            winning = sorted(values, key=lambda t: t[1], reverse=True)
            if winning[0][1] == winning[1][1]:
                print(
                    f"Es gibt aktuell ein {colors.color(8)}Unentschieden{colors.END}. Weil kein Stich einprogrammiert ist, werden beide Karten zurückgelegt."
                )
                for stack in self.player_stacks:
                    stack.insert(0, stack.pop())
                continue
            elif winning[0][0] == current_player:
                print(
                    f"Du hast {colors.GREEN}{colors.BOLD}gewonnen{colors.END} und bist nun noch einmal dran."
                )
            else:
                print(
                    f"Du hast {colors.RED}{colors.BOLD}verloren{colors.END}, {self.player_str(winning[0][0])} hat diese Runde gewonnen."
                )
                input(
                    f"Bitte gib das Gerät nun an {self.player_str(winning[0][0])}, drücke <Enter>, um fortzufahren..."
                )
                print("\n" * 28)
            time.sleep(0.6)

            returned = [
                self.player_stacks[player].pop() for player in range(self.amount)
            ]
            self.player_stacks[winning[0][0]] = (
                returned + self.player_stacks[winning[0][0]]
            )

            current_player = winning[0][0]

            if not all([len(stack) for stack in self.player_stacks]):
                losing_player = min(enumerate(self.player_stacks), key=lambda s: s[1])[
                    0
                ]
                print()
                print(
                    f"{self.player_names[losing_player]}, du hast keine Karten mehr und bist ausgeschieden."
                )

                self.player_stacks.remove(losing_player)
                self.player_names.remove(losing_player)
                self.amount -= 1

        print(f"{'n'*3}{self.player_str(0)} hat das Spiel gewonnen!")

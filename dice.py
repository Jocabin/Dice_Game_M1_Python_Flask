import random as r


class Dice:
    def __init__(self, faces=1):
        self.faces = faces

    def __str__(self):
        return f"Je suis un dé de {self.faces} faces"

    def roll(self):
        return r.randint(1, self.faces)

    def get_dice_faces(self):
        return self.faces


class RiggedDice(Dice):
    def roll(self, rigged=False):
        return self.faces if rigged else super().roll()


dice = RiggedDice(faces=100)
dice.roll(rigged=False)

print(dice)
print(dice.roll(rigged=True))

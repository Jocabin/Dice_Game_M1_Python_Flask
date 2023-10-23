from flask import Flask, request, render_template

from dice import Dice
from character import Character, Mage, Warrior, Thief

app = Flask(__name__)

class_mapping = {
    'mage': Mage,
    'warrior': Warrior,
    'thief': Thief,
    'character': Character,
}


# Helpers
def SaveCharaToFile(char: Character, type):
    save_file = open("game_data.csv", "r+")
    lines = save_file.readlines()

    if len(lines) > 0:
        for line in lines:
            if char.get_name() == line.split(";")[0]:
                return False

    saved_data = f"{char.get_name()};{char.get_max_health()};{char.get_attack_value()};{char.get_defense_value()};{char.get_dice().get_dice_faces()};{type}\n"
    save_file.write(saved_data)
    save_file.close()
    return True


def DeleteCharaFromFile(name):
    with open("game_data.csv", "r") as f:
        lines = f.readlines()

    with open("game_data.csv", "w") as f:
        for line in lines:
            file_chara_name = line.strip('\n').split(";")[0]
            if name != file_chara_name:
                f.write(line)


def RecreateChara(line):
    chara_infos = line.split(";")
    char_class = class_mapping[chara_infos[-1].replace('\n', '')]
    return char_class(chara_infos[0], chara_infos[1], chara_infos[2], chara_infos[3], Dice(chara_infos[4]))


def GetAllCharasTypes():
    return class_mapping


def GetAllCharas():
    save_file = open("game_data.csv", "r")
    lines = save_file.readlines()
    all_charas = []

    for line in lines:
        chara = RecreateChara(line)
        all_charas.append(chara)

    return all_charas


def GetSpecifiChara(name):
    save_file = open("game_data.csv", "r")
    lines = save_file.readlines()
    chara = None

    for line in lines:
        if line.split(";")[0].replace(' ', '_') == name:
            chara = RecreateChara(line)
            break

    return chara


# Routes handling
@app.route('/api/create-char', methods=['POST'])
def ReturnCreateCharPage():
    type = request.form['type']
    char_class = class_mapping[type]

    char_name = request.form['name']
    max_health = request.form['max_health']
    atk = request.form['atk']
    defense = request.form['defense']
    dice_faces = request.form['dice_faces']

    chara = char_class(char_name, max_health, atk, defense, Dice(dice_faces))
    is_chara_saved = SaveCharaToFile(chara, type)

    if not is_chara_saved:
        return '<h1>Ce personnage existe déjà</h1><a href="/">Retourner à la page d\'accueil</a>'
    else:
        return '<h1>Personnage crée</h1><a href="/">Retourner à la page d\'accueil</a>'


@app.route('/api/delete-chara', methods=['POST'])
def ReturnDeleteCharaPage():
    char_name = request.form['name']
    DeleteCharaFromFile(char_name)
    return f'<h1>Personnage supprimé</h1><a href="/">Retourner à la page d\'accueil</a>'


@app.route('/', methods=['GET'])
def RenderHomePage():
    all_charas = GetAllCharas()
    return render_template('index.html', all_charas=all_charas)


@app.route('/create-char', methods=['GET'])
def RenderCreateCharPage():
    types = GetAllCharasTypes()
    return render_template('createChar.html', types=types)


@app.route('/character/<name>', methods=['GET'])
def RenderShowCharaStats(name):
    chara = GetSpecifiChara(name)
    return render_template('charaStats.html', chara=chara)


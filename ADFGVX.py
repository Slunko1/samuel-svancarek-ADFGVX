import random

abeceda_ADFGX_CZ = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
abeceda_ADFGX_EN = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
abeceda_ADFGVX = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

wild_cards = {
    "1": "XIEDENX",
    "2": "XDVAX",
    "3": "XTRIX",
    "4": "XSTYRIX",
    "5": "XPETX",
    "6": "XSESTX",
    "7": "XSEDEMX",
    "8": "XOSEMX",
    "9": "XDEVETX",
    "0": "XNULAX",
    " ": "XMEDZERAX"
}

def najdi_znak(tabulka, znak):
    for i in range(len(tabulka)):
        for j in range(len(tabulka[i])):
            if tabulka[i][j] == znak:
                return i, j

    return None

def vymen_znaky(text, zdrojova_abeceda):
    if "W" not in zdrojova_abeceda:
        text = text.replace("W", "V")
    if "J" not in zdrojova_abeceda:
        text = text.replace("J", "I")
    return text

def odstran_diakritiku(text):
    text = text.replace("Á", "A")
    text = text.replace("Ä", "A")
    text = text.replace("Č", "C")
    text = text.replace("Ď", "D")
    text = text.replace("É", "E")
    text = text.replace("Í", "I")
    text = text.replace("Ĺ", "L")
    text = text.replace("Ľ", "L")
    text = text.replace("Ň", "N")
    text = text.replace("Ó", "O")
    text = text.replace("Ô", "O")
    text = text.replace("Ŕ", "R")
    text = text.replace("Š", "S")
    text = text.replace("Ť", "T")
    text = text.replace("Ú", "U")
    text = text.replace("Ý", "Y")
    text = text.replace("Ž", "Z")
    text = text.replace("Ě", "E")
    text = text.replace("Ů", "U")
    text = text.replace("Ř", "R")

    return text

def vytvor_tabulku(abeceda, n, seed):
    abeceda = list(abeceda)
    rng = random.Random(seed)
    rng.shuffle(abeceda)

    tabulka = []
    i = 0

    # naplnenie tabulky
    for column in range(n):
        tabulka.append([])

        for row in range(n):
            tabulka[column].append(abeceda[i])
            i += 1

    return tabulka

def osetri_vstup(text, n):
    text = text.upper()
    text = odstran_diakritiku(text)

    if n == 5:
        abeceda = abeceda_ADFGX_CZ
        text = vymen_znaky(text, abeceda)
    elif n == 55:
        abeceda = abeceda_ADFGX_EN
        text = vymen_znaky(text, abeceda)
    else:
        abeceda = abeceda_ADFGVX

    novy_text = ""
    for znak in text:
        if znak in wild_cards and znak not in abeceda:
            novy_text += wild_cards[znak]
        elif znak in abeceda:
            novy_text += znak

    return novy_text

def zasifruj(filtrovany_text, n, tabulka):
    if n == 5:
        t = "ADFGX"
    else:
        t = "ADFGVX"

    zasifrovany_text = ""
    for znak in filtrovany_text:
        suradnice = najdi_znak(tabulka, znak)

        if suradnice is None:
            continue

        x, y = suradnice

        zasifrovany_text += t[x]
        zasifrovany_text += t[y]
        zasifrovany_text += " "

    return zasifrovany_text

def transformuj_maticu(zasifrovany_text, key):
    text = zasifrovany_text.replace(" ", "")
    key = osetri_kluc(key)

    if not key:
        raise ValueError("Key must be longer than 0 characters")

    pocet_stlpcov = len(key)

    matica = []
    i = 0

    while i < len(text):
        riadok = []

        for j in range(pocet_stlpcov):
            if i < len(text):
                riadok.append(text[i])
                i += 1

        matica.append(riadok)

    return vypis_maticu_po_stlpcoch(matica, pocet_stlpcov, key)

def vypis_maticu_po_stlpcoch(matica, pocet_stlpcov, key):
    zasifrovany_text = ""

    #triedenie podla indexu
    poradie = sorted(
        range(len(key)),
        key=lambda i: (key[i], i)
    )

    for i in poradie:
        for j in range(len(matica)):
            if i < len(matica[j]):
                zasifrovany_text += matica[j][i]

    return zasifrovany_text

def osetri_kluc(key):
    key = key.upper()
    key = odstran_diakritiku(key)

    filtered_key = ""
    for znak in key:
        if znak in abeceda_ADFGX_CZ or znak in ("W"):
            filtered_key += znak

    return filtered_key

def desifruj(filtrovany_text, n, tabulka):
    if n in (5, 55):
        t = "ADFGX"
    else:
        t = "ADFGVX"

    dvojice = []
    for i in range(0, len(filtrovany_text), 2):
        dvojice.append(filtrovany_text[i:i + 2])

    novy_text = ""
    for dvojica in dvojice:
        x = dvojica[0]
        y = dvojica[1]

        x = t.index(x)
        y = t.index(y)

        novy_text += tabulka[x][y]



    return novy_text

def napln_maticu(filtrovany_text, key):
    pocet_stlpcov = len(key)
    poradie = sorted(range(len(key)),key=lambda i: (key[i], i))

    pocet_riadkov = (len(filtrovany_text) + pocet_stlpcov - 1) // pocet_stlpcov
    zvysok = len(filtrovany_text) % pocet_stlpcov

    matica = []
    for _ in range(pocet_riadkov):
        matica.append([""] * pocet_stlpcov)

    index = 0

    for stlpec in poradie:
        if zvysok > stlpec or zvysok == 0:
            dlzka = pocet_riadkov
        else:
            dlzka = pocet_riadkov - 1

        for riadok in range(dlzka):
            matica[riadok][stlpec] = filtrovany_text[index]
            index += 1

    novy_text = ""
    for riadok in matica:
        for znak in riadok:
            novy_text += znak

    return novy_text

def osetri_vstup_pre_desifrovanie(zasifrovany_text, n):
    zasifrovany_text = zasifrovany_text.replace(" ", "")

    if len(zasifrovany_text) % 2 != 0:
        return False

    for znak in zasifrovany_text:
        if znak not in "ADFGVX" and n == 6:
            return False
        elif znak not in "ADFGX" and n == 5:
            return False

    return zasifrovany_text
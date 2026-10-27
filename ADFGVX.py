import random

abeceda_ADFGX_CZ = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
abeceda_ADFGX_EN = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
abeceda_ADFGVX = "ABCDEFGHIJKLMNOPQRSTUVXYZ01234567890"


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


def vytvor_tabulku(abeceda, n):
    abeceda = list(abeceda)
    random.shuffle(abeceda)

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
        if znak in wild_cards:
            novy_text += wild_cards[znak]
        elif znak in abeceda:
            novy_text += znak

    return novy_text

def zasifruj(text, n, tabulka):
    if n == 5:
        t = "ADFGX"
    else:
        t = "ADFGVX"

    novy_text = ""
    for znak in text:
        suradnice = najdi_znak(tabulka, znak)

        if suradnice is None:
            continue

        x, y = suradnice

        novy_text += t[x]
        novy_text += t[y]

    return novy_text


print(zasifruj("UTOKXMEDZERAXNAXMEDZERAXCENKAXMEDZERAXVXMEDZERAXXDEVETXXNULAXXNULAX", 5, [['P', 'Q', 'J', 'D', 'E'], ['K', 'H', 'T', 'M', 'V'], ['X', 'U', 'O', 'Z', 'Y'], ['F', 'C', 'A', 'B', 'L'], ['G', 'S', 'N', 'I', 'R']]))

#print(osetri_vstup("Útok na čenka v 9_00", 5))

#print(vytvor_tabulku("ABCDEFGHIJKLMNOPQRSTUVXYZ01234567890", 6))
#print(vytvor_tabulku("ABCDEFGHIJKLMNOPQRSTUVXYZ", 5))



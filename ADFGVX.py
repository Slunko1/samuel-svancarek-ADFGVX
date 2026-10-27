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
    print(matica)
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

seed = "42"
n = 5
text = "Útok na čenka v 9:00"
key = "zidia"

tabulka = vytvor_tabulku(abeceda_ADFGX_CZ, n, seed)
print("Tabulka: ", tabulka)
text = osetri_vstup(text, n)
print("Filtrovany text: ", text)
zasifrovany_text = zasifruj(text, n, tabulka)
print("Zasifrovany text: ", zasifrovany_text)

print(transformuj_maticu(zasifrovany_text, key))

#print(transformuj_maticu("FD DF FF DA FA DG AX AG FG AX XX GF FA XF GF FA DG AX AG FG AX XX GF FA GD AX XF DA GF FA DG AX AG FG AX XX GF FA DX FA DG AX AG FG AX XX GF FA FA AG AX DX AX DF FA FA XF FD GX GF FA FA XF FD GX GF FA", "BAČA"))
#print(osetri_kluc("AB13"))



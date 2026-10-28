import sys

from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt

from pathlib import Path

import ADFGVX

SCRIPT_DIR = Path(__file__).resolve().parent
UI_PATH = SCRIPT_DIR / ("ADFGVX_GUI.ui")
FONT_PATH = SCRIPT_DIR / "ARCADECLASSIC.ttf"

class UiScreen(QDialog):

  def __init__(self):
    super(UiScreen, self).__init__()
    loadUi(UI_PATH, self)

    self.zdrojova_abeceda = ""
    self.n = 0

    self.comboBox_Abeceda.addItems(["ADFGX_CZ", "ADFGX_EN", "ADFGVX"])
    self.comboBox_Abeceda.currentTextChanged.connect(self.nastav_abecedu)

    #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    #self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    self.radioButton_Encrypt.setChecked(True)

    self.pushButton.clicked.connect(self.spracuj)

    self.nastav_abecedu()

  def nastav_abecedu(self):
    if self.comboBox_Abeceda.currentText() == "ADFGX_CZ":
        self.zdrojova_abeceda = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
        self.n = 5
    elif self.comboBox_Abeceda.currentText() == "ADFGX_EN":
        self.zdrojova_abeceda = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        self.n = 55
    else:
        self.zdrojova_abeceda = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        self.n = 6

  def spracuj(self):
    key = ADFGVX.osetri_kluc(self.textEdit_Key.toPlainText())
    seed = self.textEdit_Seed.toPlainText()

    #ak je kluc prazdny nastav base case
    if len(seed) == 0:
        QMessageBox.warning(
            self,
            "Bad seed",
            "The length of the key must be greater than 0"
        )
        return

    if len(key) == 0:
        QMessageBox.warning(
            self,
            "Bad key",
            "The length of the key must be greater than 0"
        )
        return

    rozmer = 6 if self.n == 6 else 5

    tabulka = ADFGVX.vytvor_tabulku(self.zdrojova_abeceda, rozmer, seed)

    #napln tabulku
    #for row in range(5):
        #for column in range(5):
            #item = QTableWidgetItem(table[row][column])
            #item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            #self.tableWidget.setItem(row, column, item)

    if self.radioButton_Encrypt.isChecked():
      plain_text = self.textEdit_plainText.toPlainText()

      if plain_text == "":
          return

      filtrovany_text = ADFGVX.osetri_vstup(plain_text, self.n)
      sifrovany_text = ADFGVX.zasifruj(filtrovany_text, self.n, tabulka)

      trans_text = ADFGVX.transformuj_maticu(sifrovany_text, key)

      self.textEdit_filteredText.setPlainText(filtrovany_text)
      self.textEdit_cipheredText.setPlainText(trans_text)

    elif self.radioButton_Decrypt.isChecked():
      plain_text = self.textEdit_plainText.toPlainText()

      if plain_text == "":
          return

      if len(plain_text) % 2 != 0:
          QMessageBox.warning(
              self,
              "Bad input",
              "The length of the text must be even."
          )
          return

      filtrovany_text = ADFGVX.osetri_vstup_pre_desifrovanie(plain_text, self.n)
      transponovany_text = ADFGVX.napln_maticu(filtrovany_text, key)
      desifrovany_text = ADFGVX.desifruj(transponovany_text, self.n, tabulka)

      self.textEdit_filteredText.setPlainText(filtrovany_text)
      self.textEdit_cipheredText.setPlainText(desifrovany_text)


if __name__ == "__main__":
  app = QApplication(sys.argv)

  # nacitanie fontu
  QFontDatabase.addApplicationFont(str(FONT_PATH))

  ui = UiScreen()
  ui.setFixedSize(ui.size())
  ui.show()

  try:
    sys.exit(app.exec())
  except:
    print("exiting")
import sys

from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
UI_PATH = SCRIPT_DIR / ("ADFGVX_GUI.ui")
FONT_PATH = SCRIPT_DIR / "ARCADECLASSIC.ttf"

class UiScreen(QDialog):

  def __init__(self):
    super(UiScreen, self).__init__()
    loadUi(UI_PATH, self)

    self.comboBox_Abeceda.addItems(["CZ", "EN"])
    self.comboBox_Abeceda.currentTextChanged.connect(self.nastav_abecedu)

    self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    self.radioButton_Encrypt.setChecked(True)

    self.pushButton.clicked.connect(self.spracuj)

    self.nastav_abecedu()

  def nastav_abecedu(self):
    if self.comboBox_Abeceda.currentText() == "CZ":
        sifra.zdrojova_abeceda = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
    else:
        sifra.zdrojova_abeceda = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

  def spracuj(self):
    key = sifra.osetri_kluc(self.textEdit_Key.toPlainText())

    #ak je kluc prazdny nastav base case
    if len(key) == 0:
        key = "A"

    table = sifra.vytvor_tabulku(key)

    #napln tabulku
    for row in range(5):
        for column in range(5):
            item = QTableWidgetItem(table[row][column])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.setItem(row, column, item)

    if self.radioButton_Encrypt.isChecked():
      plain_text = self.textEdit_plainText.toPlainText()

      if plain_text == "":
          return

      filtrovany_text = sifra.osetri_vstup(plain_text)
      sifrovany_text = sifra.zasifruj(filtrovany_text, table)

      self.textEdit_filteredText.setPlainText(' '.join(filtrovany_text))

      #rozdeli zasifrovany text po paticiach
      novy_text = " ".join(
          sifrovany_text[i:i + 5]
          for i in range(0, len(sifrovany_text), 5)
      )

      self.textEdit_cipheredText.setPlainText(novy_text)

    elif self.radioButton_Decrypt.isChecked():
      plain_text = self.textEdit_plainText.toPlainText()

      if plain_text == "":
          return

      plain_text = plain_text.replace(" ", "")
      filtrovany_text = sifra.osetri_vstup_pre_desifrovanie(plain_text)

      if len(filtrovany_text) % 2 != 0:
          QMessageBox.warning(
              self,
              "Bad input",
              "The length of the text must be even."
          )
          return

      desifrovany_text = sifra.desifruj(filtrovany_text, table)

      self.textEdit_filteredText.setPlainText(
          " ".join(sifra.vytvor_dvojice(filtrovany_text)))
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
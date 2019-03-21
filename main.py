# -*- coding: utf-8 -*-
from form import Ui_mainwindow
from registory import registory
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog,qApp
import sys
import subprocess

class main(Ui_mainwindow):

    def setupUi(self, mainwindow):
        super().setupUi(mainwindow)
        self.mainwindow = mainwindow
        self.setEvent()
        self.isopened = False
        self.selectedid = None
    
    def setEvent(self):
        self.btnAllOn.clicked.connect(self.btnAllOn_Clicked)
        self.btnAllOff.clicked.connect(self.btnAllOff_Clicked)
        self.btnExLead.clicked.connect(self.btnExLead_Clicked)
        self.btnMIDIUpload.clicked.connect(self.btnMIDIUpload_Clicked)
        self.btnBankUpload.clicked.connect(self.btnBankUpload_Clicked)
        self.btnFolderOpen.clicked.connect(self.btnFolderOpen_Clicked)
        self.actClose.triggered.connect(qApp.quit)
        self.actOpen.triggered.connect(self.Setting_Open)
        self.actSave.triggered.connect(self.save)

    def save(self):
        if not self.isopened:
            return
        if (len(self.lvFolder.selectedIndexes())>0):
            self.lvFolder_SelectionChanged()
        self.setting.write()
        
    def lvFolder_SelectionChanged(self):
        if not self.isopened:
            return
        if not (self.selectedid is None):
            self.setting.setValue(self.selectedid, registory.part["UK"], self.cbUpper.isChecked())
            self.setting.setValue(self.selectedid, registory.part["LK"], self.cbLower.isChecked())
            self.setting.setValue(self.selectedid, registory.part["PK"], self.cbFoot.isChecked())
            self.setting.setValue(self.selectedid, registory.part["XG"], self.cbXG.isChecked())
            self.setting.setValue(self.selectedid, registory.part["KBP"], self.cbKBP.isChecked())
            self.setting.setValue(self.selectedid, registory.part["LEAD"], self.cbLead.isChecked())
            self.setting.setValue(self.selectedid, registory.part["CTRL"], self.cbControl.isChecked())
        self.selectedid = list(self.setting.reg.keys())[self.lvFolder.selectedIndexes()[0].row()]
        self.displayreg(self.setting.reg[self.selectedid],self.selectedid)

    def displayreg(self, reg, id):
        self.tbNameOnElectone.setText(self.setting.getValue(id, "SONGNAME"))
        self.tbFolderName.setText(self.setting.getValue(id, "FOLDER"))
        self.tbBankFileName.setText(self.setting.getValue(id, "BLKFILE_001"))
        self.tbMIDIFileName.setText(self.setting.getValue(id, "MIDFILE"))
        self.cbUpper.setChecked(self.setting.getPartPlayOff(id, registory.part["UK"]))
        self.cbLower.setChecked(self.setting.getPartPlayOff(id, registory.part["LK"]))
        self.cbLead.setChecked(self.setting.getPartPlayOff(id, registory.part["LEAD"]))
        self.cbKBP.setChecked(self.setting.getPartPlayOff(id, registory.part["KBP"]))
        self.cbXG.setChecked(self.setting.getPartPlayOff(id, registory.part["XG"]))
        self.cbFoot.setChecked(self.setting.getPartPlayOff(id, registory.part["PK"]))
        self.cbControl.setChecked(self.setting.getPartPlayOff(id, registory.part["CTRL"]))
        self.mainwindow.repaint()

    def Setting_Open(self):
        nampath = QFileDialog.getOpenFileName(self.mainwindow, "NAMファイルを選んでください", "","NAM File (ELS_SONG.NAM)")[0]
        if not nampath :
            return
        self.setting = registory(nampath)
        self.isopened = True
        self.selectedid = None

        listModel = QtGui.QStandardItemModel(self.lvFolder)
        for i in self.setting.reg.values():
            item = QtGui.QStandardItem(i["SONGNAME"])
            listModel.appendRow(item)
        self.lvFolder.setModel(listModel)
        self.lvFolder.selectionModel().selectionChanged.connect(self.lvFolder_SelectionChanged)

    def btnFolderOpen_Clicked(self):
        try:
            # if file is not opened, process is passed.
            if not self.isopened:
                return
            
            # get the directory for id.
            path = self.setting.getIdFolderPath(self.selectedid)
            
            # select process for some OS.
            if sys.platform == 'darwin':
                    subprocess.check_call(['open', '--', path])
            elif sys.platform == 'linux2':
                    subprocess.check_call(['xdg-open', '--', path])
            elif sys.platform == 'win32':
                    subprocess.run('explorer {}'.format(path))

        except:
            QtWidgets.QMessageBox.warning(self.mainwindow, "Error", "フォルダを開けませんでした.")

    def btnBankUpload_Clicked(self):
        if not self.isopened:
            return
        fname = QFileDialog.getOpenFileName(self.mainwindow, "バルクファイルを選んでください", "","Bulk File (*.B00)")
        if not fname[0] :
            return
        self.setting.uploadFiletoIdDirectory(self.selectedid, fname[0])
    def btnMIDIUpload_Clicked(self):
        if not self.isopened:
            return
        fname = QFileDialog.getOpenFileName(self.mainwindow, "MIDIファイルを選んでください", "","SMF (*.mid)")
        if not fname[0] :
            return        
        self.setting.uploadMIDItoIdDirectory(self.selectedid, fname[0])
        self.tbMIDIFileName.setText(self.setting.getValue(self.selectedid,"MIDFILE"))
        self.cbXG.setChecked(True)

    def btnExLead_Clicked(self):
        """
        リードボイスと書かれているチェックボックス以外に全てチェックを入れる
        """
        if not self.isopened:
            return

        self.cbUpper.setChecked(True)
        self.cbLower.setChecked(True)
        self.cbLead.setChecked(False)
        self.cbFoot.setChecked(True)
        self.cbKBP.setChecked(True)
        self.cbXG.setChecked(True)
        self.cbControl.setChecked(True)
        self.mainwindow.repaint()

    def btnAllOn_Clicked(self):
        if not self.isopened:
            return
        self.cbUpper.setChecked(True)
        self.cbLower.setChecked(True)
        self.cbLead.setChecked(True)
        self.cbFoot.setChecked(True)
        self.cbKBP.setChecked(True)
        self.cbXG.setChecked(True)
        self.cbControl.setChecked(True)
        self.mainwindow.repaint()

    def btnAllOff_Clicked(self):
        if not self.isopened:
            return
        self.cbUpper.setChecked(False)
        self.cbLower.setChecked(False)
        self.cbLead.setChecked(False)
        self.cbFoot.setChecked(False)
        self.cbKBP.setChecked(False)
        self.cbXG.setChecked(False)
        self.cbControl.setChecked(False)
        self.mainwindow.repaint()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = main()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
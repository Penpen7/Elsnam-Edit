# -*- coding: utf-8 -*-
import os
import parse as pr
import pathlib
import shutil as st
class registory(object):
    partDefaultValue = {"PART_UK":True, "PART_LK":True, "PART_PK":True,
                        "PART_LEAD":False, "PART_KBP"  :True, "PART_XG":True,
                        "PART_CTRL":True,
                        "SONGNAME":"None", 
                        "FOLDER":"None",
                        "MIDFILE":""}
    part = {"UK":"PART_UK", "LK":"PART_LK","PK":"PART_PK","LEAD":"PART_LEAD",
            "KBP":"PART_KBP","XG":"PART_XG", "CTRL":"PART_CTRL"}
    def uploadMIDItoIdDirectory(self, id, filepath):
        self.uploadFiletoIdDirectory(id,filepath)
        self.setValue(id, "MIDFILE", str(pathlib.Path(filepath).name))
        self.setValue(id, self.part["XG"], True)
    def uploadBANKtoIdDirectory(self, id, filepath):
        self.uploadFiletoIdDirectory(id,filepath)
        self.setValue(id, "BLKFILE_001", str(pathlib.Path(filepath).name))

    def uploadFiletoIdDirectory(self,id, filepath):
        try:
            filename = pathlib.Path(filepath).name
            st.copy2(filepath, self.getIdFolderPath(id).joinpath(str(filename)))
        except st.SameFileError:
            pass
    def getIdFolderPath(self,id):
        return self.parentpath.joinpath(self.getValue(id, "FOLDER"))

    def setValue(self, id, column, value):
        if (column in self.part.values()):
            self.setPartPlayOff(id, column, value)
        else:
            if not self.isexistid(id):
                self.reg[id] = {}
            self.reg[id][column] = value
        
    def getValue(self, id, column):
        if column in self.reg[id]:
            return self.reg[id][column]
        else:
            return self.partDefaultValue[column]

    def setPartPlayOff(self, id, part, isplay):
        if not self.isexistid(id):
            self.reg[id] = {}
        if type(isplay) is str:
            if isplay == "PLAY":
                self.reg[id][part] = True
            else:
                self.reg[id][part] = False
        elif type(isplay) is bool:
            self.reg[id][part] = isplay
        
    def getPartPlayOff(self, id, part):
        if not self.isexistid(id):
            self.reg[id] = {}
        if self.isexistcolumn(id, part):
            return self.reg[id][part]
        else:
            if part in self.partDefaultValue:
                return self.partDefaultValue[part]
            else:
                return False
    def getValueStr(self, id, column):
        if column in self.reg[id]:
            if column in self.part.values():
                return self.getPartPlayOffStr(id,column)
            return self.reg[id][column]
        else:
            return self.partDefaultValue[column]
    def getPartPlayOffStr(self, id, part):
        if self.getPartPlayOff(id,part):
            return 'PLAY'
        else:
            return 'OFF'

    def isexistid(self, id):
        return id in self.reg

    def isexistcolumn(self, id, column):
        if not self.isexistid(id):
            return False
        return column in self.reg[id]

    def load(self,path):
        encode = 'shift_jis'
        fin = open(path,encoding = encode)
        self.reg = {}
        self.nampath = path
        self.parentpath = pathlib.Path(path).parent.resolve()

        for i in (j.rstrip('\n') for j in fin):

            # if i is blank, ignoring i.
            if not i:
                continue

            res = pr.parse("S{ID:d}:{column:<}={value:>}",i)
            # if i doesn't match the pattern, ignoring i.
            if res is None:
                continue
            
            # adding the dictionary value.
            self.setValue(res["ID"],res["column"], res["value"])

        self.reg = dict(sorted(self.reg.items(), key=lambda x: x[1]["SONGNAME"]))
        self.isopened = True
        
    def write(self):
        with open(self.nampath, mode='w', encoding='shift-jis') as f:
            for i, dic in dict(sorted(self.reg.items(), key=lambda x: x[0])).items():
                for col in dic.keys():
                    f.writelines("S%03d:%-13s= %s\n" % (i, col, self.getValueStr(i,col)))

    def __init__(self, path=None):
        self.isopened = False
        self.reg = {}
        if path is None:
            super().__init__()
        else:
            self.load(path)
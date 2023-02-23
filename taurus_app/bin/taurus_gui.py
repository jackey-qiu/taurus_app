import sys, os
from PyQt5 import uic
from taurus import Device
from taurus.qt.qtgui.container import TaurusMainWindow
from taurus.qt.qtgui.application import TaurusApplication
import taurus_app.config.synoptic_config as synoptic_config
from taurus_app.config.widget_model_config import widget_models, widget_taurus_form_models
from taurus_app.config.cad_config import taurus_form_name
from sardana.taurus.qt.qtgui.extra_macroexecutor.macroexecutor import ParamEditorManager, MacroExecutionWindow
from pathlib import Path
import click, glob

class MyMainWindow(MacroExecutionWindow):
    def __init__(self, parent=None, designMode=False):
        MacroExecutionWindow.__init__(self, parent, designMode)

    def init_gui(self, ui):
        #ui is a *.ui file from qt designer
        uic.loadUi(ui, self)
        self._qDoor = None
        self.doorChanged.connect(self.onDoorChanged)
        TaurusMainWindow.loadSettings(self)
        self.widget_terminal.update_name_space('main_gui',self)
        setattr(self.widget_drawing, 'holder', self)
        self.widget_drawing.setLabel(self.label_mouse_checker)
        self.pushButton_all_in.clicked.connect(self.put_down_all_absorbers)
        self.pushButton_all_out.clicked.connect(self.take_out_all_absorbers)
        self._set_model()

    def _set_model(self):
        for widget, model in widget_models.items():
            if hasattr(self, widget):
                getattr(self, widget).setModel(model)
            else:
                print('The main gui frame has no widget of {}'.format(widget))
            
    def put_down_all_absorbers(self):
        for each in self.widget_drawing.absorber_components:
            widget = self.widget_drawing.shape_config[each]['linked_widget']['widget']
            if hasattr(self, widget):
                getattr(self, widget).setChecked(True)

    def take_out_all_absorbers(self):
        for each in self.widget_drawing.absorber_components:
            widget = self.widget_drawing.shape_config[each]['linked_widget']['widget']
            if hasattr(self, widget):
                getattr(self, widget).setChecked(False)        

    def setCustomMacroEditorPaths(self, customMacroEditorPaths):
        MacroExecutionWindow.setCustomMacroEditorPaths(
            self, customMacroEditorPaths)
        ParamEditorManager().parsePaths(customMacroEditorPaths)
        ParamEditorManager().browsePaths()

    def onDoorChanged(self, doorName):
        MacroExecutionWindow.onDoorChanged(self, doorName)
        if self._qDoor:
            self._qDoor.macroStatusUpdated.disconnect(
                self.widget_sequence.onMacroStatusUpdated)
            self._qDoor.macroStatusUpdated.disconnect(
                self.widget_sequencer.onMacroStatusUpdated)
        if doorName == "":
            return
        self._qDoor = Device(doorName)
        self._qDoor.macroStatusUpdated.connect(
            self.widget_sequence.onMacroStatusUpdated)
        self.widget_sequence.onDoorChanged(doorName)
        self._qDoor.macroStatusUpdated.connect(
            self.widget_sequencer.onMacroStatusUpdated)
        self.widget_sequencer.onDoorChanged(doorName)
        self.widget_spock.setModel(doorName)

    def setModel(self, model):
        MacroExecutionWindow.setModel(self, model)
        self.widget_sequencer.setModel(model)
        self.widget_sequence.setModel(model)

    def updateParameter(self):
        self.taurusCommandButton.setParameters([self.lineEdit_mot1.text()])

qss_list=list(map(os.path.basename,glob.glob(str(Path(__file__).parent.parent/ "resources" / "stylesheets" / "*.qss"))))
ui_list=list(map(os.path.basename,glob.glob(str(Path(__file__).parent.parent/ "ui" / "*.ui"))))
@click.command()
@click.option('--ui', default='main_gui.ui',help="main gui ui file generated from Qt Desinger, possible ui files are :"+','.join(ui_list))
@click.option('--ss', default ='Takezo.qss', help='style sheet file *.qss, possible qss files include: '+','.join(qss_list))
def main(ui, ss):
    from taurus.core.util import argparse
    from taurus.qt.qtgui.application import TaurusApplication
    from PyQt5 import QtCore

    ui_file = str(Path(__file__).parent.parent/ "ui" / ui)
    parser = argparse.get_taurus_parser()
    app = TaurusApplication(sys.argv)
    app.setOrganizationName("DESY")
    myWin = MyMainWindow()
    myWin.init_gui(ui_file)
    TaurusMainWindow.loadSettings(myWin)
    #setup synotic widget: use the first frame at the beginning
    myWin.widget_synopic.run_init(synoptic_config.prepare_config(synoptic_config.synoptic['frame'][0]))
    myWin.widget_cad.set_taurus_form(getattr(myWin,taurus_form_name), taurus_form_name)
    myWin.widget_cad.set_synoptic_widget(myWin.widget_synopic)

    #open qss file
    #more style files can be downloaded from https://qss-stock.devsecstudio.com/index.php
    style_sheet_path = str(Path(__file__).parent.parent/ "resources" / "stylesheets" / ss)
    File = open(style_sheet_path,'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)
    myWin.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
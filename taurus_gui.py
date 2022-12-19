import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from taurus.qt.qtgui.container import TaurusMainWindow
import qdarkstyle
from taurus.qt.qtgui.input import TaurusValueLineEdit
# from py_gui2 import Ui_MainWindow
from PyQt5.QtCore import QCoreApplication 
from taurus.external.qt import Qt
from taurus.qt.qtgui.base import TaurusBaseComponent
from taurus.qt.qtgui.application import TaurusApplication
import sardana
from taurus import Device
from sardana.taurus.qt.qtgui.extra_macroexecutor.macroexecutor import ParamEditorManager, TaurusMacroExecutorWidget,createMacroExecutor,MacroExecutionWindow
from mouse_tracking import MouseTracker

class PowerMeter2(Qt.QProgressBar, TaurusBaseComponent):
    """A Taurus-ified QProgressBar with separate models for value and color"""
    # setFormat() defined by both TaurusBaseComponent and QProgressBar. Rename.
    setFormat = TaurusBaseComponent.setFormat
    setBarFormat = Qt.QProgressBar.setFormat

    modelKeys = ["power", "color"]  # support 2 models (default key is "power")
    _template = "QProgressBar::chunk {background: %s}"  # stylesheet template

    def __init__(self, parent=None, value_range=(0, 100)):
        super(PowerMeter2, self).__init__(parent=parent)
        self.parent = parent
        self.setOrientation(Qt.Qt.Vertical)
        self.setRange(*value_range)
        self.setTextVisible(False)
        self.setModel("eval:Q(60+20*rand())")  # implicit use of  key="power"
        self.setModel("eval:['green','red','blue'][randint(3)]", key='color')

    def handleEvent(self, evt_src, evt_type, evt_value):
        """reimplemented from TaurusBaseComponent"""
        try:
            if evt_src is self.getModelObj(key="power"):
                self.setValue(int(evt_value.rvalue.m))
            elif evt_src is self.getModelObj(key="color"):
                if hasattr(self,'holder'):
                    if self.holder.taurusLCD.value()>50:
                        self.setStyleSheet(self._template % 'red')
                    else:
                        self.setStyleSheet(self._template % 'green')
                else:
                    self.setStyleSheet(self._template % evt_value.rvalue)
        except Exception as e:
            self.info("Skipping event. Reason: %s", e)


class PowerMeter(Qt.QProgressBar, TaurusBaseComponent):
    """A Taurus-ified QProgressBar"""

    # setFormat() defined by both TaurusBaseComponent and QProgressBar. Rename.
    setFormat = TaurusBaseComponent.setFormat
    setBarFormat = Qt.QProgressBar.setFormat

    def __init__(self, parent=None, value_range=(0, 100)):
        super(PowerMeter, self).__init__(parent=parent)
        self.holder = None
        self.setOrientation(Qt.Qt.Vertical)
        self.setRange(*value_range)
        self.setTextVisible(False)
        self.setModel("eval:Q(60+20*rand())")
        self.setStyleSheet("QProgressBar::chunk {background: red}")

    def handleEvent(self, evt_src, evt_type, evt_value):
        """reimplemented from TaurusBaseComponent"""
        try:
            self.setValue(int(evt_value.rvalue.m))
        except Exception as e:
            self.info("Skipping event. Reason: %s", e)

class CustomLineEdit(TaurusValueLineEdit):
    def __init__(self):
        super(CustomLineEdit, self).__init__()
        self.setModel("motor/dummy_mot_ctrl/1/position")

class MyMainWindow(MacroExecutionWindow):
    def __init__(self, parent=None, designMode=False):
        MacroExecutionWindow.__init__(self, parent, designMode)
        uic.loadUi('gui2.ui', self)
        self._init_widget_()
        self._qDoor = None
        self.doorChanged.connect(self.onDoorChanged)
        # self.loadSettings()
        TaurusMainWindow.loadSettings(self)
        self.doorChanged.emit(self.doorName())
        self.widget_terminal.update_name_space('main_gui',self)
        self.power_meter = PowerMeter2()
        setattr(self.power_meter, 'holder', self)
        setattr(self.widget_drawing, 'holder', self)
        self.verticalLayout_4.addWidget(self.power_meter)
        self.lineEdit_mot1.editingFinished.connect(self.updateParameter)
        self.widget_drawing.setLabel(self.label_mouse_checker)
        self.pushButton_all_in.clicked.connect(self.put_down_all_absorbers)
        self.pushButton_all_out.clicked.connect(self.take_out_all_absorbers)

    def put_down_all_absorbers(self):
        for i, each in enumerate(self.widget_drawing.modelKeys):
            self.widget_drawing.getModelObj(key = each).write(True)
            getattr(self, 'taurusValueCheckBox_{}'.format(i+1)).setChecked(True)

    def take_out_all_absorbers(self):
        for i, each in enumerate(self.widget_drawing.modelKeys):
            self.widget_drawing.getModelObj(key = each).write(False)
            getattr(self, 'taurusValueCheckBox_{}'.format(i+1)).setChecked(False)

    def _init_widget_(self):
        self.registerConfigDelegate(self.widget_sequence)
        self.widget_sequence.setModelInConfig(True)
        self.widget_sequence.doorChanged.connect(
            self.widget_sequence.onDoorChanged)
        self.widget_sequence.shortMessageEmitted.connect(
            self.onShortMessage)
        self.statusBar().showMessage("MacroExecutor ready now")

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
        if doorName == "":
            return
        self._qDoor = Device(doorName)
        self._qDoor.macroStatusUpdated.connect(
            self.widget_sequence.onMacroStatusUpdated)
        self.widget_sequence.onDoorChanged(doorName)

    def onDoorChanged_old(self, doorName):
        MacroExecutionWindow.onDoorChanged(self, doorName)
        if self._qDoor:
            print('sensor1')
            self._qDoor.macroStatusUpdated.disconnect(
                self.widget_sequence.onMacroStatusUpdated)
        if doorName == "":
            return
        self._qDoor = Device(doorName)
        self._qDoor.macroStatusUpdated.connect(
            self.widget_sequence.onMacroStatusUpdated)
        self.widget_sequence.onDoorChanged(doorName)
        # self.widget_sequence.setModel('p25/macroserver/hase027tngtest.01')

    def setModel(self, model):
        MacroExecutionWindow.setModel(self, model)
        self.widget_sequence.setModel(model)

    def updateParameter(self):
        self.taurusCommandButton.setParameters([self.lineEdit_mot1.text()])

if __name__ == "__main__":
    from taurus.core.util import argparse
    from taurus.qt.qtgui.application import TaurusApplication

    parser = argparse.get_taurus_parser()
    parser.set_usage("%prog [options]")
    parser.set_description("Sardana macro executor.\n"
                           "It allows execution of macros, keeping history "
                           "of previous executions and favourites.")    
    app = TaurusApplication(sys.argv,
                            cmd_line_parser=parser,
                            app_name="macroexecutor",
                            app_version=sardana.Release.version)
    app.setOrganizationName("DESY")
    myWin = MyMainWindow()
    TaurusMainWindow.loadSettings(myWin)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myWin.show()
    sys.exit(app.exec_())

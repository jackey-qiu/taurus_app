from sardana.taurus.qt.qtgui.extra_macroexecutor.sequenceeditor.sequenceeditor import TaurusSequencer,TaurusSequencerWidget
from sardana.taurus.qt.qtgui.extra_macroexecutor.macroexecutor import TaurusMacroExecutorWidget,createMacroExecutorWidget
from taurus.qt.qtgui.container import TaurusMainWindow

sequencer = TaurusSequencer()
sequencer.loadSettings()

class SequenceWidget(TaurusSequencerWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        #self.setDoorName('p25/door/hase027tngtest.01')
        #self.setModelInConfig(True)
        # self.loadSettings()

class MacroExecutor(TaurusMacroExecutorWidget):
    def __init__(self,parent=None, designMode=False):
        super().__init__(parent, designMode)
        self.setModelInConfig(True)
        # self.onDoorChanged('p25/door/hase027tngtest.01')
        self.doorChanged.connect(self.onDoorChanged)

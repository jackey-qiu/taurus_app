from taurus.qt.qtgui.base import TaurusBaseComponent
from taurus.external.qt import Qt


class PowerMeter(Qt.QProgressBar, TaurusBaseComponent):
    """A Taurus-ified QProgressBar with separate models for value and color"""
    # setFormat() defined by both TaurusBaseComponent and QProgressBar. Rename.
    setFormat = TaurusBaseComponent.setFormat
    setBarFormat = Qt.QProgressBar.setFormat

    modelKeys = ["power", "color"]  # support 2 models (default key is "power")
    _template = "QProgressBar::chunk {background: %s}"  # stylesheet template

    def __init__(self, parent=None, value_range=(0, 100)):
        super(PowerMeter, self).__init__(parent=parent)
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
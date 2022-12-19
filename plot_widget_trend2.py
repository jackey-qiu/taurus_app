import sys
import numpy
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.tpg import TaurusPlotDataItem
from setBufferTool import BufferTool

import pyqtgraph as pg

import sys
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.tpg import (
    TaurusTrendSet,
    DateAxisItem,
    XAutoPanTool,
    ForcedReadTool,
)
import pyqtgraph as pg

from taurus.core.taurusmanager import TaurusManager

taurusM = TaurusManager()
taurusM.changeDefaultPollingPeriod(1000)
axis = DateAxisItem(orientation="bottom")

class TaurusPlotWidget2(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addLegend()

        axis.attachToPlotItem(self.getPlotItem())

        # Add the auto-pan ("oscilloscope mode") tool
        autopan = XAutoPanTool()
        autopan.attachToPlotItem(self.getPlotItem())

        # Add Forced-read tool
        fr = ForcedReadTool(self, period=1000)
        fr.attachToPlotItem(self.getPlotItem())
        
        #add buffer tool
        bt = BufferTool(self)
        bt.attachToPlotItem(self.getPlotItem())

        # add a taurus data item
        c2 = TaurusTrendSet(name="motor pos", pen="g", symbol="+")
        c2.setModel('motor/dummy_mot_ctrl/2/position')
        self.addItem(c2)


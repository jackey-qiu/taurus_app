import sys
import numpy
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.tpg import TaurusPlotDataItem
# print('post 1a')
import pyqtgraph as pg
import copy

import sys
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.tpg import (
    TaurusTrendSet,
    DateAxisItem,
    XAutoPanTool,
    ForcedReadTool,
)
import pyqtgraph as pg

# print('post 2a')
from taurus.core.taurusmanager import TaurusManager
from .setBufferTool import BufferTool

# print('post 3a')
taurusM = TaurusManager()
# print('post 4a')
taurusM.changeDefaultPollingPeriod(1000)
# print('post 5a')
axis = DateAxisItem(orientation="bottom")
model = 'motor/motctrl01/1/Position'
# print('post 6a')
class TaurusPlotWidget(pg.PlotWidget):
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
        c2 = TaurusTrendSet(name="motor pos", pen="r", symbol=None)
        # c2.setModel('motor/dummy_mot_ctrl/1/position')
        c2.setModel(model)
        self.addItem(c2)
        self.plot_item = c2


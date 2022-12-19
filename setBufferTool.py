__all__ = ["setBufferTool"]

from taurus.external.qt import QtGui, QtCore
from taurus.qt.qtcore.configuration import BaseConfigurableClass


class BufferTool(QtGui.QAction, BaseConfigurableClass):
    """
    This tool provides a menu option to control the "Forced Read" period of
    Plot data items that implement a `setForcedReadPeriod` method
    (see, e.g. :meth:`TaurusTrendSet.setForcedReadPeriod`).
    The force-read feature consists on forcing periodic attribute reads for
    those attributes being plotted with a :class:`TaurusTrendSet` object.
    This allows to force plotting periodical updates even for attributes
    for which the taurus polling is not enabled.
    Note that this is done at the widget level and therefore does not affect
    the rate of arrival of events for other widgets connected to the same
    attributes
    This tool inserts an action with a spinbox and emits a `valueChanged`
    signal whenever the value is changed.
    The connection between the data items and this tool can be done manually
    (by connecting to the `valueChanged` signal or automatically, if
    :meth:`autoconnect()` is `True` (default). The autoconnection feature works
    by discovering the compliant data items that share associated to the
    plot_item.
    This tool is implemented as an Action, and provides a method to attach it
    to a :class:`pyqtgraph.PlotItem`
    """

    valueChanged = QtCore.pyqtSignal(int)

    def __init__(
        self,
        parent=None,
        text="Change buffer size...",
    ):
        BaseConfigurableClass.__init__(self)
        QtGui.QAction.__init__(self, text, parent)
        tt = "Set the buffer size.\nLarger than 1"
        self.setToolTip(tt)
        self._bufferSize = 100

        # register config properties
        self.registerConfigProperty(self.buffersize, self.setBufferSize, "buffersize")

        # internal conections
        self.triggered.connect(self._onTriggered)

    def _onTriggered(self):
        buffer = self.buffersize()
        buffer, ok = QtGui.QInputDialog.getInt(
            self.parentWidget(),
            "New read buffer",
            "Set the buffer size.\nLarger than 1",
            buffer,
            1,
            600000,
            50,
        )
        if ok:
            self.setBufferSize(buffer)

    def buffersize(self):
        return self._bufferSize

    def attachToPlotItem(self, plot_item):
        """Use this method to add this tool to a plot
        :param plot_item: (PlotItem)
        """
        menu = plot_item.getViewBox().menu
        menu.addAction(self)
        self.plot_item = plot_item

    def setBufferSize(self, buffer):
        items = self.plot_item.listDataItems()
        if len(items)>1:
            if hasattr(items[1], 'setBufferSize'):
                items[1].setBufferSize(buffer)
                self._bufferSize = buffer
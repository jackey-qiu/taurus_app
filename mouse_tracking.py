import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from taurus.qt.qtgui.container import TaurusWidget


class MouseTracker(TaurusWidget):

    cursorCheck = pyqtSignal(int, int)
    #multi models
    modelKeys = ['ior1','ior10', 'ior11','ior12']
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.initUI()
        self.setMouseTracking(True)
        self.rgb = [(100,100,100)]*4
        self.length_hoz = 20
        self.length_ver = 80
        self.origin_x = 100
        self.origin_x_offset = 200
        self.origin_y = 100
        self.origin_y_offset = [0,0,0,0]
        self.cursorCheck.connect(self.checkCursorPos)
        #self.model = 'motor/dummy_mot_ctrl/2/position'
        self.label = None
        self.checkBox = None
        self.lineStyle = [Qt.SolidLine]*4
        self.setModel('ioregister/sis3610in_eh/1/SimulationMode', key = 'ior1')
        self.setModel('ioregister/sis3610in_eh/10/SimulationMode', key = 'ior10')
        self.setModel('ioregister/sis3610in_eh/11/SimulationMode', key = 'ior11')
        self.setModel('ioregister/sis3610in_eh/12/SimulationMode', key = 'ior12')

    def setLabel(self, label):
        self.label = label

    def setCheckBox(self, checkBox):
        self.checkBox = checkBox


    @pyqtSlot(int, int)
    def checkCursorPos(self, x, y):
        on, which = self._check_bounds(x, y)
        if on:
            if self.rgb[which]!=(255,0,0):
                self.rgb[which] = (255,0,0)
                self.lineStyle[which] = Qt.DashLine
                self.update()
        else:
            self.rgb = [(100, 100, 100)]*4
            self.lineStyle = [Qt.SolidLine]*4
            self.update()
        
    def handleEvent(self, e_s, e_t, e_v):
        for i in range(len(self.modelKeys)):
            if e_s is self.getModelObj(key = self.modelKeys[i]):
                if e_v.rvalue:
                    self.origin_y_offset[i] = 0
                else:
                    self.origin_y_offset[i] = 50
        self.update()        

    def paintEvent(self, e) -> None:
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(QColor(255,0,0), 1, Qt.SolidLine))
        qp.drawLine(10, self.origin_y+50, self.origin_x+2000, self.origin_y+50)
        for i in range(len(self.origin_y_offset)):
            qp.setPen(QPen(QColor(250, 250, 250), 1, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
            qp.setFont(QFont('Decorative', 12))
            qp.drawText(self.origin_x+self.origin_x_offset*i-20,self.origin_y+self.length_ver +20, f'Absorber {i+1}')
            qp.setPen(QPen(QColor(*self.rgb[i]), 2, self.lineStyle[i]))
            qp.setBrush(QColor(0,150,0))
            qp.drawRect(self.origin_x+self.origin_x_offset*i,self.origin_y-self.origin_y_offset[i],self.length_hoz,self.length_ver)
        qp.end()

    def mouseMoveEvent(self, event):
        if self.label !=None:
            self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
        self.cursorCheck.emit(event.x(), event.y())

    def _check_bounds(self, x, y):
        for i in range(len(self.origin_y_offset)):
            top_left_corner = (self.origin_x+int(self.origin_x_offset*i), self.origin_y-self.origin_y_offset[i])
            bottom_right_corner = (self.origin_x + +int(self.origin_x_offset*i) + self.length_hoz, self.origin_y - self.origin_y_offset[i]+self.length_ver)
            if (top_left_corner[0]<=x<= bottom_right_corner[0]) and (top_left_corner[1]<=y<= bottom_right_corner[1]):
                return True, i
        return False, 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            on, which = self._check_bounds(event.x(), event.y())
            if on:
                value = self.getModelObj(key = self.modelKeys[which]).rvalue
                self.getModelObj(key = self.modelKeys[which]).write(not value)
                getattr(self.holder, 'taurusValueCheckBox_{}'.format(which+1)).setChecked(not value)
                
                #self.checkBox.setChecked(not self.checkBox.isChecked())
            


if __name__ == '__main__':
    import sys
    from taurus.external.qt import Qt
    from taurus.qt.qtgui.application import TaurusApplication

    app = TaurusApplication(sys.argv, cmd_line_parser=None,)
    panel = Qt.QWidget()
    layout = Qt.QHBoxLayout()
    panel.setLayout(layout)

    from taurus.qt.qtgui.display import TaurusLabel
    w = TaurusLabel()
    layout.addWidget(w)
    w.model = 'sys/taurustest/1/position'
    print(type(w.getModelObj()))

    from PyQt5.QtCore import Qt
    ex = MouseTracker()
    w.getModelObj().addListener(ex)
    layout.addWidget(ex)
    panel.show()
    sys.exit(app.exec_())




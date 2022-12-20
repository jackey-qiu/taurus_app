import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from taurus.qt.qtgui.container import TaurusWidget

draw_components = {
    'comp1':{
        'caller':'drawRect',
        'init_pars': {'x':0,'y':0,'width':20,'height':80},
        'models': {'x':None,'y':'ior1','width':None,'height':None},
        'model_scales': {'x':0,'y':50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
    },
    'comp2':{
        'caller':'drawRect',
        'init_pars': {'x':200,'y':0,'width':20,'height':80},
        'models': {'x':None,'y':'ior10','width':None,'height':None},
        'model_scales': {'x':0,'y':50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
    },
    'comp3':{
        'caller':'drawRect',
        'init_pars': {'x':400,'y':0,'width':20,'height':80},
        'models': {'x':None,'y':'ior11','width':None,'height':None},
        'model_scales': {'x':0,'y':50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
    },
    'comp4':{
        'caller':'drawRect',
        'init_pars': {'x':600,'y':0,'width':20,'height':80},
        'models': {'x':None,'y':'ior12','width':None,'height':None},
        'model_scales': {'x':0,'y':50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
    },
}

class MouseTracker(TaurusWidget):

    cursorCheck = pyqtSignal(int, int)
    #multi models
    modelKeys = ['ior1','ior10', 'ior11','ior12']
    def __init__(self, parent=None, shape_config = draw_components):
        super().__init__(parent)
        # self.initUI()
        self.shape_config = self._check_shape(shape_config)
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

    def _check_shape(self, shape):
        for each in shape:
            models = [model for model in each['models'] if model!=None]
            if len(models)>1:
                raise Exception('You are allowed to attach maximum one model to each shape component.')
            if len(models)==1:
                if models[0] not in self.modelKeys:
                    raise Exception('The specified model key in the shape component does not match the class properties modelKeys.')
        return shape
        
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

        qp.setPen(QPen(QColor(*self.rgb[i]), 2, self.lineStyle[i]))
        qp.setBrush(QColor(0,150,0))
        self._drawComponents(qp)

        '''
        for i in range(len(self.origin_y_offset)):
            qp.setPen(QPen(QColor(250, 250, 250), 1, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
            qp.setFont(QFont('Decorative', 12))
            qp.drawText(self.origin_x+self.origin_x_offset*i-20,self.origin_y+self.length_ver +20, f'Absorber {i+1}')
            qp.setPen(QPen(QColor(*self.rgb[i]), 2, self.lineStyle[i]))
            qp.setBrush(QColor(0,150,0))
            qp.drawRect(self.origin_x+self.origin_x_offset*i,self.origin_y-self.origin_y_offset[i],self.length_hoz,self.length_ver)
        qp.end()
        '''

    def _drawComponents(self, qp):
        for each_comp in self.shape_config:
            each = self.shape_config[each_comp]
            caller = each['caller']
            init_pars = each['init_pars']
            final_pars = {}
            for key in init_pars:
                model_value = each['models'][key]
                if model_value!=None:
                    temp = self.getModelObj(key = model_value).wvalue
                    if type(temp)==bool:
                        model_value = 1 if temp else -1
                    else:
                        model_value = temp._magnitude
                else:
                    model_value = 0
                value_offset = model_value * each['model_scales'][key]
                final_pars[key] = init_pars[key] + value_offset
            self.shape_config[each_comp]['final_pars'] = final_pars
            getattr(qp, caller)(**final_pars)

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

    def check_bounds(self, x, y):
        for each in self.shape_config:
            if each['caller'] == 'drawRect':
                if self._check_bounds_rect(x, y, each['final_pars']):
                    return True, each
        return False, None
            
    def _check_bounds_rect(self, x, y, coords):
        top_left_corner = (coords['x'], coords['y'])
        bottom_right_corner = (coords['x']+coords['width'], coords['y']+coords['height'])
        if (top_left_corner[0]<=x<= bottom_right_corner[0]) and (top_left_corner[1]<=y<= bottom_right_corner[1]):
            return True
        return False

    def mousePressEvent_old(self, event):
        if event.button() == Qt.LeftButton:
            on, which = self._check_bounds(event.x(), event.y())
            if on:
                value = self.getModelObj(key = self.modelKeys[which]).rvalue
                self.getModelObj(key = self.modelKeys[which]).write(not value)
                getattr(self.holder, 'taurusValueCheckBox_{}'.format(which+1)).setChecked(not value)
                
                #self.checkBox.setChecked(not self.checkBox.isChecked())
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            on, which = self.check_bounds(event.x(), event.y())
            if on:
                model_key = None
                model_keys = [each for each in self.shape_config[which]['models'] if each != None]
                if len(model_keys)==1:
                    model_key = model_keys[0]
                value = self.getModelObj(key = model_key).rvalue
                self.getModelObj(key = self.modelKeys[which]).write(not value)
                getattr(self.holder, 'taurusValueCheckBox_{}'.format(which+1)).setChecked(not value)
                

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




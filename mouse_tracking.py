import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from taurus.qt.qtgui.container import TaurusWidget

draw_components = {
    'comp1':{
        'caller':'drawRect',
        'init_pars': {'x':100,'y':100,'width':20,'height':80},
        'models': {'x':None,'y':'ior1','width':'ampli','height':None},
        'model_scales': {'x':0,'y':-50,'width':1,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'linked_widget':{'widget':'taurusValueCheckBox_1','func':'setChecked','model':'ior1'},
    },
    'comp2':{
        'caller':'drawRect',
        'init_pars': {'x':300,'y':100,'width':20,'height':80},
        'models': {'x':None,'y':'ior10','width':None,'height':None},
        'model_scales': {'x':0,'y':-50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'linked_widget':{'widget':'taurusValueCheckBox_2','func':'setChecked','model':'ior10'},
    },
    'comp3':{
        'caller':'drawRect',
        'init_pars': {'x':500,'y':100,'width':20,'height':80},
        'models': {'x':None,'y':'ior11','width':None,'height':None},
        'model_scales': {'x':0,'y':-50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'linked_widget':{'widget':'taurusValueCheckBox_3','func':'setChecked','model':'ior11'},
    },
    'comp4':{
        'caller':'drawRect',
        'init_pars': {'x':700,'y':100,'width':20,'height':80},
        'models': {'x':None,'y':'ior12','width':None,'height':None},
        'model_scales': {'x':0,'y':-50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'linked_widget':{'widget':'taurusValueCheckBox_4','func':'setChecked','model':'ior12'},
    },
}

class MouseTracker(TaurusWidget):

    cursorCheck = pyqtSignal(int, int)
    #multi models
    modelKeys = ['ampli','ior1','ior10', 'ior11','ior12']
    def __init__(self, parent=None, shape_config = draw_components):
        super().__init__(parent)
        self.shape_config = self._check_shape(shape_config)
        self.setMouseTracking(True)
        self.cursorCheck.connect(self.checkCursorPos)
        self.setModel('sys/tg_test/1/ampli', key = 'ampli')
        self.setModel('ioregister/sis3610in_eh/1/SimulationMode', key = 'ior1')
        self.setModel('ioregister/sis3610in_eh/10/SimulationMode', key = 'ior10')
        self.setModel('ioregister/sis3610in_eh/11/SimulationMode', key = 'ior11')
        self.setModel('ioregister/sis3610in_eh/12/SimulationMode', key = 'ior12')

    def setLabel(self, label):
        self.label = label

    def _check_shape(self, shape):
        for each in shape:
            models = [model for model in shape[each]['models'].values() if model!=None]
            print(models)
            # if len(models)>1:
                # raise Exception('You are allowed to attach maximum one model to each shape component.')
            for model in models:
                if model not in self.modelKeys:
                    raise Exception('The specified model key in the shape component does not match the class properties modelKeys.')
        return shape

    @pyqtSlot(int, int)
    def checkCursorPos(self, x, y):
        on, which = self.check_bounds(x, y)
        if on:
            if self.shape_config[which]['rgb']!=(255,0,0):
                self.shape_config[which]['rgb'] = (255,0,0)
                self.shape_config[which]['lineStyle'] = Qt.DashLine
                self.update()
        else:
            for each in self.shape_config:
                self.shape_config[each]['rgb'] = (100, 100, 100)
                self.shape_config[each]['lineStyle'] = Qt.SolidLine
            self.update()
        
    def handleEvent(self, e_s, e_t, e_v):
        self.update()

    def paintEvent(self, e) -> None:
        qp = QPainter()
        qp.begin(self)
        #x ray beam simulation
        qp.setPen(QPen(QColor(255,0,0), 3, Qt.SolidLine))
        qp.drawLine(10, 90, 2100, 90)
        self._drawComponents(qp)
        qp.end()

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
            qp.setPen(QPen(QColor(*each['rgb']), 2, each['lineStyle']))
            qp.setBrush(QColor(0,150,0))
            getattr(qp, caller)(*final_pars.values())

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
            if self.shape_config[each]['caller'] == 'drawRect':
                if self._check_bounds_rect(x, y, self.shape_config[each]['final_pars']):
                    return True, each
        return False, None
            
    def _check_bounds_rect(self, x, y, coords):
        top_left_corner = (coords['x'], coords['y'])
        bottom_right_corner = (coords['x']+coords['width'], coords['y']+coords['height'])
        if (top_left_corner[0]<=x<= bottom_right_corner[0]) and (top_left_corner[1]<=y<= bottom_right_corner[1]):
            return True
        return False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            on, which = self.check_bounds(event.x(), event.y())
            if on:
                model_key = None
                model_keys = [each for each in self.shape_config[which]['models'].values() if each != None]
                if len(model_keys)==0:
                    return # not linked to any model, thus a static component
                else:
                    for model_key in model_keys:
                        value = self.getModelObj(key = model_key).rvalue
                        if type(value)==bool:
                            #left click will only map to a boolian attribute
                            self.getModelObj(key = model_key).write(not value)
                        else:
                            pass
                #update widget
                model_widget = self.shape_config[which]['linked_widget']['model']
                widget = self.shape_config[which]['linked_widget']['widget']
                func = self.shape_config[which]['linked_widget']['func']
                assert hasattr(self.holder, widget),'widget object not existing in the holder frame'
                assert (model_widget in self.modelKeys),'unregistered model object'
                widget_obj = getattr(self.holder, widget)
                getattr(widget_obj, func)(self.getModelObj(key = model_widget).rvalue)
                
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




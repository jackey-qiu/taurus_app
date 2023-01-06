import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QMenu, QDialog, QMessageBox)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from taurus.qt.qtgui.container import TaurusWidget
from PyQt5 import uic

draw_components = {
    'comp1':{
        'caller':'drawRect',
        'init_pars': {'x':100,'y':100,'width':20,'height':80},
        'models': {'x':None,'y':'ior1','width':'ampli','height':None},
        'model_scales': {'x':0,'y':-50,'width':1,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'text':{'text':'motor1','pos':'top'},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'paint': (0,150,0), 
        'clickable': True,
        'step_move': {'model':None, 'step':1},
        'linked_widget':{'widget':'taurusValueCheckBox_1','func':'setChecked','model':'ior1'},
    },
    'comp2':{
        'caller':'drawRect',
        'init_pars': {'x':300,'y':100,'width':20,'height':80},
        'models': {'x':None,'y':'ior2','width':None,'height':None},
        'model_scales': {'x':0,'y':-50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'text':{'text':'motor2','pos':'top'},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'paint': (0,150,0), 
        'clickable': True,
        'step_move': {'model':None, 'step':1},
        'linked_widget':{'widget':'taurusValueCheckBox_2','func':'setChecked','model':'ior2'},
    },
    'comp3':{
        'caller':'drawRect',
        'init_pars': {'x':500,'y':100,'width':20,'height':80},
        'models': {'x':None,'y':'ior3','width':None,'height':None},
        'model_scales': {'x':0,'y':-50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'text':{'text':'motor3','pos':'top'},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'paint': (0,150,0), 
        'clickable': True,
        'step_move': {'model':None, 'step':1},
        'linked_widget':{'widget':'taurusValueCheckBox_3','func':'setChecked','model':'ior3'},
    },
    'comp4':{
        'caller':'drawRect',
        'init_pars': {'x':700,'y':100,'width':20,'height':80},
        'models': {'x':None,'y':'ior2','width':None,'height':None},
        'model_scales': {'x':0,'y':-50,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':80},
        'text':{'text':'motor2','pos':'top'},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'paint': (0,150,0), 
        'clickable': True,
        'step_move': {'model':None, 'step':1},
        'linked_widget':{'widget':'taurusValueCheckBox_4','func':'setChecked','model':'ior2'},
    },
    'comp5':{
        'caller':'drawRect',
        'init_pars': {'x':900,'y':90,'width':20,'height':40},
        'models': {'x':None,'y':'offset','width':None,'height':None},
        'model_scales': {'x':0,'y':5,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':40},
        'text':{'text':'down','pos':'bottom'},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'paint': (0,150,0), 
        'clickable': True,
        'step_move': {'model':'offset', 'step':1},
        'linked_widget':{'widget':'taurusValueSpinBox_offset','func':'setValue','model':'offset'},
    },
    'comp6':{
        'caller':'drawRect',
        'init_pars': {'x':900,'y':50,'width':20,'height':40},
        'models': {'x':None,'y':'offset','width':None,'height':None},
        'model_scales': {'x':0,'y':-5,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':40},
        'text':{'text':'top','pos':'top'},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'paint': (0,150,0), 
        'clickable': True,
        'step_move': {'model':'offset', 'step':-1},
        'linked_widget':{'widget':'taurusValueSpinBox_offset','func':'setValue','model':'offset'},
    },
    'sample':{
        'caller':'drawRect',
        'init_pars': {'x':500,'y':350,'width':300,'height':300},
        'models': {'x':None,'y':None,'width':None,'height':None},
        'model_scales': {'x':5,'y':5,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':40},
        'text':{'text':'sample on top view','pos':'top'},
        'rgb': (100, 100, 100),
        'lineStyle': Qt.SolidLine,
        'paint': (150,150,150), 
        'clickable': False,
        'step_move': {'model':None, 'step':1},
        'linked_widget':{'widget':None,'func':None,'model':None},
    },
    'footprint':{
        'caller':'drawRect',
        'init_pars': {'x':635,'y':485,'width':30,'height':30},
        'models': {'x':'gx','y':'gy','width':None,'height':None},
        'model_scales': {'x':30,'y':30,'width':0,'height':0},
        'final_pars': {'x':0,'y':0,'width':20,'height':40},
        'text':{'text':'beamfootprint','pos':'top'},
        'rgb': (0, 0, 250),
        'lineStyle': Qt.DashLine,
        'paint': (250,0,0,180), 
        'clickable': True,
        'step_move': {'model':'gx', 'step':1},
        'linked_widget':{'widget':None,'func':None,'model':None},
    },
}

class MouseTracker(TaurusWidget):

    cursorCheck = pyqtSignal(int, int)
    #multi models
    modelKeys = ['ampli','ior1','ior2', 'ior3','offset','gx', 'gy']
    absorber_components = ['comp1','comp2', 'comp3','comp4']
    def __init__(self, parent=None, shape_config = draw_components):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popupMenu)
        self.shape_config = self._check_shape(shape_config)
        self.setMouseTracking(True)
        self.cursorCheck.connect(self.checkCursorPos)
        self.setModel('sys/tg_test/1/ampli', key = 'ampli')
        self.setModel('ioregister/iorctrl01/1/SimulationMode', key = 'ior1')
        self.setModel('ioregister/iorctrl01/2/SimulationMode', key = 'ior2')
        self.setModel('sys/tg_test/1/boolean_scalar', key = 'ior3')
        self.setModel('pm/slitctrl01/2/Position', key = 'offset')
        self.setModel('motor/motctrl01/3/Position', key = 'gx')
        self.setModel('motor/motctrl01/4/Position', key = 'gy')

        # self.setModel('ioregister/sis3610in_eh/12/SimulationMode', key = 'ior12')

    def popupMenu(self):
        menu = QMenu()
        pos = QCursor.pos()
        pos_widget = self.mapFromGlobal(pos)
        comps = self.check_bounds(pos_widget.x(), pos_widget.y())
        open_seting_panels = []
        if len(comps)!=0:
            for comp in comps:
                open_seting_panels.append(menu.addAction('Click to set up component: {}'.format(comp)))
        else:
             do_nothing = menu.addAction('You clicked on the empty space')
        action = menu.exec_(pos)   
        if action in open_seting_panels:
            #print('Pop up setting table!')
            self.onClickedMenu(key = comps[open_seting_panels.index(action)])  
        elif action == do_nothing:
            pass 

    def setLabel(self, label):
        self.label = label

    def _check_shape(self, shape):
        for each in shape:
            models = [model for model in shape[each]['models'].values() if model!=None]
            # if len(models)>1:
                # raise Exception('You are allowed to attach maximum one model to each shape component.')
            for model in models:
                if model not in self.modelKeys:
                    raise Exception('The specified model key in the shape component does not match the class properties modelKeys.')
        return shape

    @pyqtSlot(int, int)
    def checkCursorPos(self, x, y):
        whichs = self.check_bounds(x, y)
        for which in whichs:
            if self.shape_config[which]['clickable']:
                if self.shape_config[which]['rgb']!=(255,0,0):
                    self.shape_config[which]['rgb'] = (255,0,0)
                    self.shape_config[which]['lineStyle'] = Qt.DashLine
                    #self.update()
        for each in self.shape_config:
            if each not in whichs:
                if self.shape_config[each]['clickable']:
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

    def _draw_grids(self, center = (0,0), grid_size = (30,30), grid_pieces = (10,10)):
        top_left = (center[0]-grid_size[0]*grid_pieces[0]/2, center[1]-grid_size[1]*grid_pieces[1]/2)
        hor_lines = [(top_left[0],top_left[1]+i*grid_size[1],top_left[0]+grid_pieces[0]*grid_size[0],top_left[1]+i*grid_size[1]) for i in range(int(grid_pieces[1])+1)]
        ver_lines = [(top_left[0]+i*grid_size[0],top_left[1],top_left[0]+i*grid_size[0],top_left[1]+grid_pieces[1]*grid_size[1]) for i in range(int(grid_pieces[0])+1)]
        return hor_lines + ver_lines

    def _align_text(self, pos = {'x':0, 'y':0}, flag = 'top'):
        #flag in ['top','bottom']
        offset = 10
        assert 'x' in pos and 'y' in pos, 'the pos has a wrong structure, should contain x and y key at least'
        if flag == 'top':
            return [pos['x'], pos['y'] - offset]
        elif flag == 'bottom':
            height = 0
            if 'height' in pos:
                height = pos['height']
            return [pos['x'], pos['y'] + height + offset]
        else:
            return [pos['x'], pos['y']]

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
            qp.setBrush(QColor(*each['paint']))
            getattr(qp, caller)(*final_pars.values())
            qp.setPen(QPen(QColor(*[200,200,200]), 2, each['lineStyle']))
            qp.drawText(*self._align_text(final_pars, flag = self.shape_config[each_comp]['text']['pos']), self.shape_config[each_comp]['text']['text'])
            if each_comp == 'sample':
                lines = self._draw_grids(center = (final_pars['x'] + final_pars['width']/2, final_pars['y'] + final_pars['height']/2),
                                                   grid_size = (self.shape_config['footprint']['final_pars']['width'],self.shape_config['footprint']['final_pars']['height']), 
                                                   grid_pieces = (int(final_pars['width']/self.shape_config['footprint']['final_pars']['width']),int(final_pars['height']/self.shape_config['footprint']['final_pars']['height'])))
                qp.setPen(QPen(QColor(*[100,100,100]), 2, each['lineStyle']))
                [qp.drawLine(*line) for line in lines]

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
        return_ = []
        for each in self.shape_config:
            if self.shape_config[each]['caller'] == 'drawRect':
                if self._check_bounds_rect(x, y, self.shape_config[each]['final_pars']):
                    return_.append(each)
        return return_
        #return False, None
            
    def _check_bounds_rect(self, x, y, coords):
        top_left_corner = (coords['x'], coords['y'])
        bottom_right_corner = (coords['x']+coords['width'], coords['y']+coords['height'])
        if (top_left_corner[0]<=x<= bottom_right_corner[0]) and (top_left_corner[1]<=y<= bottom_right_corner[1]):
            return True
        return False

    def mousePressEvent(self, event):
        return_ = [each for each in self.check_bounds(event.x(), event.y()) if self.shape_config[each]['clickable']]
        if return_==[]:
            return

        for which in return_:
            model_key = None
            model_keys = [each for each in self.shape_config[which]['models'].values() if each != None]
            if len(model_keys)==0:
                return # not linked to any model, thus a static component
            else:
                for model_key in model_keys:
                    value = self.getModelObj(key = model_key).rvalue
                    if type(value)==bool:
                        if event.button() == Qt.LeftButton:
                            #left click will only map to a boolian attribute
                            self.getModelObj(key = model_key).write(not value)
                    else:
                        if model_key == self.shape_config[which]['step_move']['model']:
                            if event.button() == Qt.LeftButton:
                                #old_value = self.getModelObj(key = model_key).rvalue._magnitude
                                self.getModelObj(key = model_key).write(value._magnitude + self.shape_config[which]['step_move']['step'])
                            elif event.button() == Qt.RightButton:
                                # print('event',event.x(),event.y())
                                pass
                                #self.getModelObj(key = model_key).write(value._magnitude - self.shape_config[which]['step_move']['step'])

            #update widget
            model_widget = self.shape_config[which]['linked_widget']['model']
            widget = self.shape_config[which]['linked_widget']['widget']
            func = self.shape_config[which]['linked_widget']['func']
            if model_widget==None:
                return
            assert hasattr(self.holder, widget),'widget object not existing in the holder frame'
            assert (model_widget in self.modelKeys),'unregistered model object'
            widget_obj = getattr(self.holder, widget)
            value = self.getModelObj(key = model_widget).rvalue
            if type(value)==bool:
                getattr(widget_obj, func)(value)
            else:
                getattr(widget_obj, func)(value._magnitude)

    def onClickedMenu(self, key):
        setup_dialog = setupComponent(self, self.shape_config[key], key)
        setup_dialog.exec()

class setupComponent(QDialog):
    def __init__(self, parent=None, config_dict = {}, comp_key = None):
        super().__init__(parent)
        self.parent = parent
        uic.loadUi("setup_table.ui", self)
        self.keys_lineEdit = []
        self.comp_key = comp_key
        self.load_config(config_dict)
        self.pushButton_update.clicked.connect(self.update_config)

    def load_config(self, config):
        self.keys_lineEdit = []
        self.lineEdit_key.setText(self.comp_key)
        for key, value in config.items():
            if hasattr(self, 'lineEdit_{}'.format(key)):
                getattr(self, 'lineEdit_{}'.format(key)).setText(str(value))
                self.keys_lineEdit.append('lineEdit_{}'.format(key))

    def update_config(self):
        try:
            config_dict = {}
            for each in self.keys_lineEdit:
                if each=='lineEdit_caller':
                    config_dict['caller'] = getattr(self, each).text()
                else:
                    config_dict[each[9:]] = eval(getattr(self, each).text())
            original_dict = self.parent.shape_config[self.comp_key]
            original_dict.update(config_dict)
            self.parent.shape_config[self.comp_key] = original_dict
            self.parent.update()
            info_pop_up('Succed to update pars. Close the dialog to continue on!','Information')
        except Exception as e:
            info_pop_up('Fail to update pars. Error:{}'.format(str(e)), 'Error')

def info_pop_up(msg_text = 'error', window_title = ['Error','Information','Warning'][0]):
    msg = QMessageBox()
    if window_title == 'Error':
        msg.setIcon(QMessageBox.Critical)
    elif window_title == 'Warning':
        msg.setIcon(QMessageBox.Warning)
    else:
        msg.setIcon(QMessageBox.Information)

    msg.setText(msg_text)
    # msg.setInformativeText('More information')
    msg.setWindowTitle(window_title)
    msg.exec_()

    
                
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




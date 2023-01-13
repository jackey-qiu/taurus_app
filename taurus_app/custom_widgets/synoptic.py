import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
import xml.etree.ElementTree as ET
from taurus.qt.qtgui.container import TaurusWidget
import re

class SynopticWidget(QSvgWidget, TaurusWidget):

    cursorCheck = pyqtSignal(int, int)
    modelKeys = []

    def __init__(self, parent=None):
        super(SynopticWidget, self).__init__(parent = parent)

    def run_init(self, config):
        #supposed to be called inside main gui
        #config is a dict with keys of svg_file, model and hover_style
        self.svg_file = config['svg_file']
        self.hover_style = config['hover_style']
        self.model_list = config['model']
        self.modelKeys = list(set(self.modelKeys + list(config['model'].keys())))
        self.tree = ET.parse(self.svg_file)
        self._init_actions()
        #signal slot connection
        self.setMouseTracking(True)
        self.cursorCheck.connect(self.checkCursorPos)

    def _init_actions(self):
        self._init_svg()
        self._get_ids_from_svg()
        self._set_style_model_when_hovered()
        self._set_init_transform()
        self.set_tango_models()
        self.reload_svg()
        self.style_box = self._get_init_styles()
        self.last_clicked_shapes_id= []

    def set_tango_models(self):
        for key, model in self.model_list.items():
            self.setModel(model, key = key)

    def update_style_when_hovered(self, id):
        style = self._get_element_with_id(id).get('style_model_when_hovered')
        if style!=None:
            self.update_xml_tree(id, {'style':style})

    def _set_style_model_when_hovered(self):
        for id in self.ids_shape:
            if self._get_element_with_id(id).get('style_model_when_hovered') == None:
                self._get_element_with_id(id).set('style_model_when_hovered', self.hover_style)

    def _set_init_transform(self):
        for id in self.ids_shape:
            if self._get_element_with_id(id).get('transform') == None:
                self._get_element_with_id(id).set('transform', 'translate(0,0)')

    def mousePressEvent(self, event):
        x, y  = self._transform_mouse_cursor_coords_on_VB(event.x(), event.y())
        pos_ids = self._cursor_on_which_component(x, y)
        if len(pos_ids)==0:
            return
        for id in pos_ids:
            self.update_when_left_clicked(id)

    def update_when_left_clicked(self, id):
        #click event can connect to only one model at most
        #here you are supposed to change some tango model value
        #for that, a tango model must be either a bool or a number
        #reconized tags: <model>+0.1(add 0.1 when clicked), <model>-2 (subtract 2 when clicked), not <model> (opposite, hint of a bool type for this model)
        change_string = self._get_element_with_id(id).get('move_when_left_clicked')
        if change_string==None:
            return
        matched_models = re.findall('<(.*?)>',change_string)
        if len(matched_models)==0:
            print('No model found!')
            return
        elif len(matched_models)>1:
            print('More than one model found, but you are allowed to make change to a single model')
            return
        model = matched_models[0] 
        if model in self.modelKeys:
            model_value = self.getModelObj(key = model).rvalue
            if type(model_value)==bool:
                assert change_string.startswith('not'), 'unsupported operation for bool type model:{}'.format(change_string)
                self.getModelObj(key = model).write(not model_value)
            else:
                model_value = model_value._magnitude
                new_model_value = eval(change_string.replace('<{}>'.format(model),str(model_value)))
                self.getModelObj(key = model).write(new_model_value)

    def _get_init_styles(self):
        return dict((each,self._get_element_with_id(each).get('style')) for each in self.ids_shape)

    def _get_ids_from_svg(self):
        self.ids = [each.attrib['id'] for each in self.tree.getroot().iter('*') if 'id' in each.attrib]
        self.ids_shape = [id for id in self.ids if self.renderer().elementExists(id)]
        #group layer id is also included, drop them from the ids_shape
        ids_ = []
        for id in self.ids_shape:
            #this rule would fail if you change the default attribute name for a layer in Inkscape
             if "{http://www.inkscape.org/namespaces/inkscape}groupmode" not in self._get_element_with_id(id).attrib:
                ids_.append(id)
        self.ids_shape = ids_

    def _update_model_move_to_svg(self, id):
        search_pattern = {
                          'translate':"translate\((\-?\d+\.?\d*),(\-?\d+\.?\d*)\)",#get ('20', '30')' in 'translate(20,30)'
                          'rotate':"rotate\((\-?\d+\.?\d*),(\-?\d+\.?\d*),(\-?\d+\.?\d*)\)",#get ('10', '20', '30') in 'rotate(10,20,30)'
                          }
        #model_move_string eg. "translate(<old_1>+<offset>*1,<old_2>);rotate(int(<offset>),<old_2>,<old_3>)"
        model_move_string = self._get_element_with_id(id).get('model_move')
        transform_attribute = self._get_element_with_id(id).get('transform')
        if model_move_string==None or transform_attribute==None:
            return
        else:
            #remove all empty spaces
            model_move_string = model_move_string.replace(' ', '')
            transform_attribute = transform_attribute.replace(' ','')
        moves = model_move_string.rstrip().rsplit(';')
        for i,move in enumerate(moves):
            move_updated = move
            #step 1 find <old_x> tag x = 1, 2, or 3
            old_tags = re.findall("(<old_[1-3]>)", move)
            #get old values only two possibilities, either translate or rotate
            old_values = None
            if move.startswith('translate'):
                old_values = re.search(search_pattern['translate'],transform_attribute).groups()
            elif move.startswith('rotate'):
                old_values = re.search(search_pattern['rotate'],transform_attribute).groups()
            for tag in old_tags:#eg <old_1>
                index_ = int(tag[-2])-1 #either 0 or 1 or 2
                assert len(old_values)>index_, 'the size of old_values {} is too small'.format(old_values)
                #replace the tag with the associated old values
                move_updated = move_updated.replace(tag, str(old_values[index_]))
            #now get the model tags
            matched_model_names = re.search("<(.*?)>",move_updated).groups()
            for each_model in matched_model_names:
                value = 'undefined'
                if each_model in self.modelKeys:
                    value = self.getModelObj(key = each_model).rvalue
                    if type(value)!=bool:
                        value = value._magnitude
                    else:
                        value = int(value)
                #replace the model tag with the assiciated model values
                move_updated = move_updated.replace('<{}>'.format(each_model), str(value))
            #move_updated_items eg (('translate','(0,2*3)'))
            move_updated_items = re.findall("(translate|rotate)(\(.*\))",move_updated)[0]
            # do some evaluation for some math equation eg. 2*3 --> 6, since svg is not happy about math symbol
            move_updated = move_updated_items[0] + str(eval(move_updated_items[1]))
            moves[i] = move_updated
        self._get_element_with_id(id).set('transform',''.join(moves))
        return ''.join(moves)

    def _cursor_on_which_component(self, cx, cy):
        ids_cursor_on = []
        for id in self.ids_shape:
            if self.renderer().boundsOnElement(id).contains(cx, cy):
                ids_cursor_on.append(id)
        return ids_cursor_on

    def _get_element_with_id(self, id):
        eles = [each for each in self.tree.getroot().iter("*") if 'id' in each.attrib and each.attrib['id']==id]
        if len(eles)!=0:
            return eles[0]
        else:
            return None

    def _regenerate_svg_bytes(self):
        for id in self.ids_shape:
            self._update_model_move_to_svg(id)
        self.svg_bytes = bytearray(ET.tostring(self.tree.getroot()).decode(), encoding='utf-8')

    def update_xml_tree(self, shape_id, modifier_dict = {}):
        #shape_id should be a string segments seperated by / representing the
        #modifier_dict hold the attribute as keys and the updated attribute values as the values
            #note the spetial attribute of 'text' means modifying the text of the node, which can be
            #done by querying text directly. Therefore, you should never use 'text' for attrib names to
            #avoid this conflict.

        def _update_style_attrib(style_str, modifier):
            #style_str is ; seperated string for styling eg 'display:inline;fill:#008000;stroke:#ff0000;stroke-width:3.11811;stroke-dasharray:3.11811, 9.35433;stroke-dashoffset:0'
            #modifier is one/muti ; seperated segments eg 'display:inline;fill:#008000'
            #style_list_original = style_str.rsplit(';')
            style_str_new = dict((x.strip(), y.strip()) for x, y in (each.rsplit(':') for each in style_str.rsplit(';')))
            style_str_updated = dict((x.strip(), y.strip()) for x, y in (each.rsplit(':') for each in modifier.rsplit(';')))
            style_str_new.update(style_str_updated)
            return ';'.join([':'.join(each) for each in style_str_new.items()])

        temp_ = self._get_element_with_id(shape_id)
        if temp_ != None:
            for key, value in modifier_dict.items():
                if key!='text':
                    if key!='style':
                        temp_.set(key, str(value))
                    else:#if key is style
                        value = _update_style_attrib(temp_.get('style'), value)
                        temp_.set(key, str(value))
                else:
                    temp_.text = str(value)
        self.reload_svg()

    def handleEvent(self, e_s, e_t, e_v):
        self.reload_svg()

    def reload_svg(self):
        self._regenerate_svg_bytes()
        self.load(self.svg_bytes)
        self.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        self.show()

    def _init_svg(self):#only called in init
        self.svg_bytes = bytearray(ET.tostring(self.tree.getroot()).decode(), encoding='utf-8')
        self.load(self.svg_bytes)
        self.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        self.show()

    def mouseMoveEvent(self, event):
        x, y = self._transform_mouse_cursor_coords_on_VB(event.x(), event.y())
        self.cursorCheck.emit(x, y)

    @pyqtSlot(int, int)
    def checkCursorPos(self, x, y):
        pos_ids = self._cursor_on_which_component(x, y)
        if len(pos_ids)!=0:
            self.last_clicked_shapes_id = pos_ids
            [self.update_style_when_hovered(each) for each in pos_ids]
        else:
            for each in self.last_clicked_shapes_id:
                self._get_element_with_id(each).set('style', self.style_box[each])
            self.reload_svg()

    def _transform_mouse_cursor_coords_on_VB(self, x, y):
        width = self.width()
        height = self.height()
        asp_ratio_widget = width/height
        width_vb = self.renderer().viewBoxF().width()
        height_vb = self.renderer().viewBoxF().height()
        asp_ratio_vb = width_vb/height_vb
        if asp_ratio_widget < asp_ratio_vb:
            scale = width/width_vb
            delta_y = (height - height_vb*scale)/2
            return x/scale, (y-delta_y)/scale
        else:
            scale = height/height_vb
            delta_x = (width - width_vb*scale)/2
            return (x-delta_x)/scale, y/scale

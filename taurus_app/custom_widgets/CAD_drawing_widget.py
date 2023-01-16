from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QImage, QPainterPath, QColor, QBrush, QFont, QPen
from PyQt5.QtCore import Qt, QTimer
import sys
from pathlib import Path
import imageio, cv2
from taurus_app.config.cad_config import config
from taurus_app.config.widget_model_config import widget_taurus_form_models
import taurus_app.config.synoptic_config as synoptic_config

class cadWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.img = None
        self.img_ratio_original = None
        self.img_width_original = None
        self.img_height_original = None
        self.frame = {}
        self.anchored_frames = []
        self.taurus_form = None
        self.model_labels = []
        self.run_init(config)

    def run_init(self, config):
        self.img = config['img']
        self.img_resize = config['size']

    def set_taurus_form(self, taurus_form, form_name):
        self.taurus_form = taurus_form
        self.taurus_form_model = widget_taurus_form_models[form_name]

    def set_synoptic_widget(self, widget):
        self.synoptic_widget = widget

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self._draw_image(qp)
        self._draw_rect(qp)
        qp.end()

    def _draw_image(self, pq):
        image = imageio.imread(self.img)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        if self.img_ratio_original==None:
            self.img_ratio_original = image.shape[1]/image.shape[0]
            self.img_width_original, self.img_height_original = image.shape[1], image.shape[0]
        image = cv2.resize(image, dsize=self.img_resize, interpolation=cv2.INTER_CUBIC)
        im = QImage(image,image.shape[1],image.shape[0], image.shape[1] * 3, QImage.Format_BGR888)
        pq.drawImage(0, 0, im)

    def _set_img_dim_upon_resize(self):
        #we would like to keep the img_ratio
        view_box_ratio = self.width()/self.height()
        if view_box_ratio >= self.img_ratio_original:
            self.img_resize = (int(self.img_ratio_original*self.height()),int(self.height()))
        else:
            self.img_resize = (int(self.width()),int(self.width()/self.img_ratio_original))

    def resizeEvent(self, e):
        if self.img_ratio_original==None:
            return
        self._set_img_dim_upon_resize()
        self.update()

    def _draw_rect(self, pq):
        x_scale = self.img_resize[0]/self.img_width_original
        y_scale = self.img_resize[1]/self.img_height_original
        pq.setPen(QPen(QColor(255,0,0), 2, Qt.DotLine))
        for key,(dim, line_color, line_style, brush_color) in config['rect_frames'].items():
            dim = (int(dim[0]*x_scale),int(dim[1]*y_scale),int(dim[2]*x_scale),int(dim[3]*y_scale))
            self.frame[key] = {'x': dim[0], 'y':dim[1], 'width': dim[2], 'height': dim[3]}
            pq.setPen(QPen(QColor(*line_color), 2, line_style))
            pq.setBrush(QColor(*brush_color))
            pq.drawRect(*dim)

    def check_bounds_rect(self, x, y, coords):
        top_left_corner = (coords['x'], coords['y'])
        bottom_right_corner = (coords['x']+coords['width'], coords['y']+coords['height'])
        if (top_left_corner[0]<=x<= bottom_right_corner[0]) and (top_left_corner[1]<=y<= bottom_right_corner[1]):
            return True
        return False

    def mouseMoveEvent(self, event):
        for each in self.frame:
            if self.check_bounds_rect(event.x(), event.y(), self.frame[each]):
                config['rect_frames'][each] = [config['rect_frames'][each][0]] + config['hover_style']
            else:
                config['rect_frames'][each] = [config['rect_frames'][each][0]] + config['non_hover_style']
            if each in self.anchored_frames:
                config['rect_frames'][each] = [config['rect_frames'][each][0]] + config['anchor_style']
        self.update()

    def mousePressEvent(self, event):
        for each in self.frame:
            if self.check_bounds_rect(event.x(), event.y(), self.frame[each]):
                if event.button() == Qt.LeftButton:
                    self.synoptic_widget.run_init(synoptic_config.prepare_config(each))
                if each in self.anchored_frames and event.button() == Qt.RightButton:#right click to remove
                    self.anchored_frames.remove(each)
                    self.remove_taurus_form_model(each)
                    return
                else:
                    if each not in self.anchored_frames:
                        self.anchored_frames.append(each)
                        self.add_taurus_form_model(each)
                        return

    def add_taurus_form_model(self, frame_key):
        models_raw = self.taurus_form_model[frame_key]
        labels = []
        models = []
        for each in models_raw:
            label, model = each.split(':')
            labels.append(label)
            models.append(model)
        self.model_labels = self.model_labels + labels
        self.taurus_form.addModels(models)
        for i in range(len(self.model_labels)):
            self.taurus_form[i].labelConfig = self.model_labels[i]  

    def remove_taurus_form_model(self, frame_key):
        models_raw = self.taurus_form_model[frame_key]
        models = []
        for each in models_raw:
            label, model = each.split(':')
            models.append(model)
            self.model_labels.remove(label)
        self.taurus_form.removeModels(models)
        for i in range(len(self.model_labels)):
            self.taurus_form[i].labelConfig = self.model_labels[i]  
      
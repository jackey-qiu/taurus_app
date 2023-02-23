from .tango_model_manager import get_model

#keys are the widget names, values are the associated tango model address
widget_models = {'taurusLed': get_model('dmot1','State'),
          'taurusLCD': get_model('dmot1','Position'),
          'taurusValueSpinBox':get_model('dmot1','Position'),
          'taurusLed_2': get_model('dmot2','State'),
          'taurusLCD_2': get_model('dmot2','Position'),
          'taurusValueSpinBox_2':get_model('dmot2','Position'),
          'taurusValueCheckBox_1':get_model('ior1','SimulationMode'),
          'taurusValueCheckBox_2':get_model('ior2','SimulationMode'),
          'taurusValueCheckBox_3':get_model('ior3','SimulationMode'),
          'taurusValueCheckBox_4':get_model('ior4','SimulationMode'),
          'taurusValueSpinBox_offset':get_model('omot1','Position'),
          'taurusValueSpinBox_gx':get_model('omot2','Position'),
          'taurusValueSpinBox_gy':get_model('omot3','Position'),
          'plot_widget':get_model('dmot1','Position'),
          'plot_widget2':get_model('dmot2','Position'),
          }

widget_taurus_form_models = {'taurusForm':{'OH':[f"motor1:{get_model('omot1','Position')}"],
                                           'CC':[f"motor2:{get_model('omot2','Position')}"],
                                           'PD':[f"motor3:{get_model('omot3','Position')}"],
                                           'XFI':[f"ior1:{get_model('ior1','SimulationMode')}"],
                                           'IM':[f"ior2:{get_model('ior2','SimulationMode')}",f"ior3:{get_model('ior3','SimulationMode')}"]},
                            }
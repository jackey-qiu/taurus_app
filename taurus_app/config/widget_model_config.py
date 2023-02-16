#keys are the widget names, values are the associated tango model address
widget_models = {'taurusLed': 'motor/dummy_mot_ctrl/1/State',
          'taurusLCD': 'motor/dummy_mot_ctrl/1/Position',
          'taurusValueSpinBox':'motor/dummy_mot_ctrl/1/Position',
          'taurusLed_2': 'motor/dummy_mot_ctrl/2/State',
          'taurusLCD_2': 'motor/dummy_mot_ctrl/2/Position',
          'taurusValueSpinBox_2':'motor/dummy_mot_ctrl/2/Position',
          'taurusValueCheckBox_1':'ioregister/sis3610in_eh/1/SimulationMode',
          'taurusValueCheckBox_2':'ioregister/sis3610in_eh/2/SimulationMode',
          'taurusValueCheckBox_3':'ioregister/sis3610in_eh/3/SimulationMode',
          'taurusValueCheckBox_4':'ioregister/sis3610in_eh/4/SimulationMode',
          'taurusValueSpinBox_offset':'motor/omsvme58_motor_eh/1/Position',
          'taurusValueSpinBox_gx':'motor/omsvme58_motor_eh/2/Position',
          'taurusValueSpinBox_gy':'motor/omsvme58_motor_eh/3/Position'}

widget_taurus_form_models = {'taurusForm':{'OH':['motor1:motor/omsvme58_motor_eh/1/Position'],'CC':['motor2:motor/omsvme58_motor_eh/2/Position'],'PD':['motor3:motor/omsvme58_motor_eh/3/Position'],
                                           'XFI':['ior1:ioregister/sis3610in_eh/1/SimulationMode'],'IM':['ior2:ioregister/sis3610in_eh/2/SimulationMode','ior3:ioregister/sis3610in_eh/3/SimulationMode']},
                            }
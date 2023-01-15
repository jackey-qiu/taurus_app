#keys are the widget names, values are the associated tango model address
widget_models = {'taurusLed': 'motor/motctrl01/1/State',
          'taurusLCD': 'motor/motctrl01/1/Position',
          'taurusValueSpinBox':'motor/motctrl01/1/Position',
          'taurusLed_2': 'motor/motctrl01/2/State',
          'taurusLCD_2': 'motor/motctrl01/2/Position',
          'taurusValueSpinBox_2':'motor/motctrl01/2/Position',
          'taurusValueCheckBox_1':'ioregister/iorctrl01/1/SimulationMode',
          'taurusValueCheckBox_2':'ioregister/iorctrl01/2/SimulationMode',
          'taurusValueCheckBox_3':'sys/tg_test/1/boolean_scalar',
          'taurusValueCheckBox_4':'ioregister/iorctrl01/2/SimulationMode',
          'taurusValueSpinBox_offset':'pm/slitctrl01/2/Position',
          'taurusValueSpinBox_gx':'motor/motctrl01/3/Position',
          'taurusValueSpinBox_gy':'motor/motctrl01/4/Position'}

widget_taurus_form_models = {'taurusForm':{'OH':['motor1:motor/motctrl01/1/Position'],'CC':['motor2:motor/motctrl01/2/Position'],'PD':['motor3:motor/motctrl01/3/Position'],
                                           'XFI':['ior1:ioregister/iorctrl01/1/SimulationMode'],'IM':['ior2:ioregister/iorctrl01/2/SimulationMode','ior3:sys/tg_test/1/boolean_scalar']},
                            }
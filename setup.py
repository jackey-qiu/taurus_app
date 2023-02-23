from setuptools import setup, find_packages

setup(
    name = 'taurus_app',
    version= '0.1.0',
    description='beamline control software based on taurus toolkit',
    author='Canrong Qiu (Jackey)',
    author_email='canrong.qiu@desy.de',
    url='https://github.com/jackey-qiu/taurus_app',
    classifiers=['Topic :: beamline control GUI',
                 'Programming Language :: Python'],
    license='MIT',
    install_requires=['imageio','taurus_pyqtgraph','Taurus==5.1.4','opencv-python'],
    packages=find_packages(where='taurus_app'),
    package_dir={'': 'taurus_app'},
    package_data={'':['*.ui','*.svg','*.qss','.xml'],'resources':['imgs/*.*']},
    scripts=['./taurus_app/bin/taurus_gui.py'],
    entry_points = {
        'console_scripts' : [
            'tad = taurus_app.bin.taurus_gui:main'
        ],
    }
)
import sys
from cx_Freeze import setup, Executable


# Command to create .exe file
# python setup.py build


base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'include_files': [
            ('static', 'static'),
        ],

    },
}

executables = [Executable(
    script="main.py",
    base=base,
    target_name="PSD_Combiner.exe",
    icon="static/img/favicon.ico",
)]

setup(
    name='PSD Combiner',
    version='1.0',
    options=options,
    executables=executables,
    install_requires=[
        'beautifulsoup4==4.12.2',
        'certifi==2023.7.22',
        'charset-normalizer==3.3.0',
        'click==8.1.7',
        'colorama==0.4.6',
        'CurrencyConverter==0.17.11',
        'idna==3.4',
        'PyQt5==5.15.9',
        'pyqt5-plugins==5.15.9.2.3',
        'PyQt5-Qt5==5.15.2',
        'PyQt5-sip==12.12.2',
        'pyqt5-tools==5.15.9.3.3',
        'python-dotenv==1.0.0',
        'qt5-applications==5.15.2.2.3',
        'qt5-tools==5.15.2.1.3',
        'requests==2.31.0',
        'simplejson==3.19.2',
        'soupsieve==2.5',
        'urllib3==2.0.6',
    ],
)

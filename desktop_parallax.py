import os, winreg, math, sys
from PIL import Image, ImageTk
from PySide2.QtWidgets import QApplication,QLabel
from PySide2.QtGui import QScreen, QPixmap
from PySide2.QtCore import QSize

DESKTOP_PATH = os.path.expanduser("~/Desktop")

def setup():
    IMG_PATH = get_img()
    print(f'Loading this desktop: {IMG_PATH}')
    create_window(IMG_PATH)

def get_img():
    try:
        registry = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
        reg_key = winreg.OpenKey(registry,r"Control Panel\Desktop")
        IMG_PATH = winreg.QueryValueEx(reg_key,"WallPaper")[0]
        return IMG_PATH
    except:
        print("Could not find Windows Desktop Background Path. Suggest feature to set as variable.")
        return None


def scale_toScreen(desktop,qpix):
    w,h = get_screen_dim(desktop)
    imw = qpix.width()
    imh = qpix.height()
    scale_x = w/imw
    scale_y = h/imh
    scale = max(scale_x,scale_y)
    scaled_w = int(math.ceil(imw * scale))
    print(f'{imw},{imh} => {w},{h} scale by {scale} to {scaled_w}')
    return qpix.scaledToWidth(scaled_w)
    #return qpix

def get_screen_dim(desktop):
    geo = desktop.screenGeometry()
    return geo.width(),geo.height()

def create_window(IMG_PATH):
    app = QApplication([])
    desktop = app.desktop()
    qpix = QPixmap(IMG_PATH)
    qpix = scale_toScreen(desktop,qpix)
    label = QLabel()
    label.setPixmap(qpix)
    label.show()
    sys.exit(app.exec_())


if __name__ == '__main__': setup()

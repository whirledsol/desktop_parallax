import os, winreg, math, sys
from PIL import Image, ImageTk
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QScreen, QPixmap
from PySide2.QtCore import QSize,Qt
from QBackgroundImage import QBackgroundImage

DESKTOP_PATH = os.path.expanduser("~/Desktop")


def setup():
    #start here
    IMG_PATH = get_img()
    print(f'Loading this desktop: {IMG_PATH}')
    create_window(IMG_PATH)

def on_mouse_move(e):
    #mouse move
    print(e)

def get_img():
    #find the background image from the registry
    try:
        registry = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
        reg_key = winreg.OpenKey(registry,r"Control Panel\Desktop")
        IMG_PATH = winreg.QueryValueEx(reg_key,"WallPaper")[0]
        return IMG_PATH
    except:
        print("Could not find Windows Desktop Background Path. Suggest feature to set as variable.")
        return None
        
def scale_qpix(qpix,w,h):
    #scale the QPixmap
    imw = qpix.width()
    imh = qpix.height()
    scale_x = w/imw
    scale_y = h/imh
    scale = max(scale_x,scale_y)
    scaled_w = int(math.ceil(imw * scale))
    scaled_h = int(math.ceil(imh * scale))
    #print(f'{imw},{imh} => {w},{h} scale by {scale} to {scaled_w}')
    return qpix.scaled(scaled_w,scaled_h),scaled_w,scaled_h
    #return qpix



def get_screen_dim(desktop):
    #get screen dimensions
    geo = desktop.screenGeometry()
    return geo.width(),geo.height()

def create_window(IMG_PATH):
    #initial window creation
    app = QApplication([])
    qpix = QPixmap(IMG_PATH)
    w,h = get_screen_dim(app.desktop())
    qpix,iw,ih = scale_qpix(qpix,w,h)
    window = QMainWindow()
    window.resize(w,h) 
    window.setWindowFlags(Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint)
    bg = QBackgroundImage(window,w,h)
    bg.setBackground(qpix,iw,ih)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__': setup()

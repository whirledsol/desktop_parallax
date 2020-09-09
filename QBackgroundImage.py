import sys
from PySide2.QtWidgets import QLabel


class QBackgroundImage(QLabel):
    w=0
    h=0
    im_w=0
    im_h=0
    center_x=0
    center_y=0
    overflow_x=0
    overflow_y=0
    max_overflow=400

    def __init__(self, parent, w, h):
        #sets the parent and basic props
        super(QBackgroundImage,self).__init__(parent)
        self.w = w
        self.h = h
        self.setMouseTracking(True)

    def setBackground(self, qpix, iw,ih):
        #sets the image and size parameters
        self.im_w = iw
        self.im_h = ih

        self.overflow_x = (self.im_w - self.w)/2
        self.overflow_y = (self.im_h - self.h)/2
        self.overflow_x = max_overflow if self.overflow_x > self.max_overflow else self.overflow_x
        self.overflow_y = max_overflow if self.overflow_y > self.max_overflow else self.overflow_y
        
        self.setPixmap(qpix)

        self.resize(self.im_w,self.im_h)
        self.center_x, self.center_y = self.get_center_coord()
        self.move(self.center_x,self.center_y)
        

    def mouseMoveEvent(self, event):
        #event handler
        p = event.pos() # relative to widget
        gp = self.mapToGlobal(p) # relative to screen
        rw = self.window().mapFromGlobal(gp) # relative to window
        #print("position relative to window: ", rw)

        offset_x = ((2*rw.x() - self.w)/self.w)*self.overflow_x
        offset_y = ((2*rw.y() - self.h)/self.h)*self.overflow_y
        self.move(self.center_x-offset_x,self.center_y-offset_y)
        
        super(QBackgroundImage, self).mouseMoveEvent(event)
    
    def get_center_coord(self):
        #calculates the top-left coordinates so that iwxih is in the center of wxh
        return int(round(self.w-self.im_w)/2),int(round(self.h-self.im_h)/2)

    def get_center_diff(self,x,y):
        #calculates diff from center
        return int(round((self.w/2)-x)),int(round((self.h/2)-y))
        
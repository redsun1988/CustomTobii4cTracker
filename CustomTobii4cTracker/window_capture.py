import ctypes
import win32con
import win32gui
from PIL import Image
from ctypes import windll
from struct import calcsize, pack

class WindowCapture:
    def __init__(self):
        self.user32 = windll.user32
        self.gdi32 = windll.gdi32
        self.PW_RENDERFULLCONTENT = 2

    def get_snapshot(self, hwnd: int) -> Image.Image:
        """Получает снимок окна"""
        hbmp, w, h, img = self.getWindowBMAP(hwnd,True)
        self.gdi32.DeleteObject(hbmp)
        return img

    def getWindowBMAP(self, hwnd, returnImage=False):
        # get Window size and crop pos/size
        L,T,R,B = win32gui.GetWindowRect(hwnd)
        W,H = R-L,B-T
        x,y,w,h = (8,8,W-16,H-16) if self.user32.IsZoomed(hwnd) else (7,0,W-14,H-7)

        # create dc's and bmp's
        dc = self.user32.GetWindowDC(hwnd)
        dc1, dc2 = self.gdi32.CreateCompatibleDC(dc), self.gdi32.CreateCompatibleDC(dc)
        bmp1, bmp2 = self.gdi32.CreateCompatibleBitmap(dc,W,H), self.gdi32.CreateCompatibleBitmap(dc,w,h)

        # render dc1 and dc2 (bmp1 and bmp2) (uncropped and cropped)
        obj1,obj2 = self.gdi32.SelectObject(dc1,bmp1), self.gdi32.SelectObject(dc2,bmp2) # select bmp's into dc's
        self.user32.PrintWindow(hwnd,dc1,self.PW_RENDERFULLCONTENT) # render window to dc1
        self.gdi32.BitBlt(dc2,0,0,w,h,dc1,x,y,win32con.SRCCOPY) # copy dc1 (x,y,w,h) to dc2 (0,0,w,h)
        self.gdi32.SelectObject(dc1,obj1); self.gdi32.SelectObject(dc2,obj2) # restore dc's default obj's

        if returnImage: # create Image from bmp2
            data = ctypes.create_string_buffer((w*4)*h)
            bmi = ctypes.c_buffer(pack("IiiHHIIiiII",calcsize("IiiHHIIiiII"),w,-h,1,32,0,0,0,0,0,0))
            self.gdi32.GetDIBits(dc2,bmp2,0,h,ctypes.byref(data),ctypes.byref(bmi),win32con.DIB_RGB_COLORS)
            img = Image.frombuffer('RGB',(w,h),data,'raw','BGRX')

        # clean up
        self.gdi32.DeleteObject(bmp1) # delete bmp1 (uncropped)
        self.gdi32.DeleteDC(dc1); self.gdi32.DeleteDC(dc2) # delete created dc's
        self.user32.ReleaseDC(hwnd,dc) # release retrieved dc

        return (bmp2,w,h,img) if returnImage else (bmp2,w,h)
import time
import math
import win32gui
import async_timer
from typing import Tuple
from CustomTobii4cTracker.event import Event
from CustomTobii4cTracker.image_processor import ImageProcessor
from CustomTobii4cTracker.window_capture import WindowCapture
from CustomTobii4cTracker.utils import TrackerInfo

class Tobii4cTracker:
    def __init__(self, target_color: Tuple, window_title="SSOverlay"):
        self.window_title: str = window_title
        self._timer_interval = 0.1
        self.window_capture = WindowCapture()
        self.image_processor = ImageProcessor(target_color)
        self.on_center_updated = Event()

    async def start_monitoring(self) -> None:
        """Запускает процесс мониторинга"""
        old_target_center = None
        async with async_timer.Timer(self._timer_interval, target=time.time) as timer:
            async for time_rv in timer:
                target_center = self.find_center()
                # Проверка и уведомление о изменении
                if target_center != old_target_center:
                    self.on_center_updated.notify(target_center)
                    old_target_center = target_center

    def find_center(self) -> TrackerInfo:
        hwnd = win32gui.FindWindow(None, self.window_title)
        if hwnd:
            pil_image = self.window_capture.get_snapshot(hwnd)
            colored_centers = self.image_processor.process_image(pil_image)
            target_centers = [(c[0], c[1], c[2]) for c in colored_centers if c[3] == self.image_processor.target_color]
            target_center = target_centers[0] if len(target_centers) > 0 else (None, None, None)
        info: TrackerInfo = TrackerInfo()
        info.x=target_center[0]
        info.y=target_center[1]
        if target_center[2] is not None:
            info.radius=math.sqrt(target_center[2] / (2 * math.pi))
        else:
            info.radius=None

        return info
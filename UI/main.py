"""
UI 入口。之後將直接 import 並呼叫 features 中的函式，不透過 API。
目前僅展示空視窗，不實作任何 UI 邏輯。
"""
import wx
from features import calculate_distance as calc_distance
from features import calculate_parallel_turnout_distance as calc_parallel_turnout_distance


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetTitle("Minecraft Transit Railway Calculation API")
        self.SetSize((800, 600))
        self.Center()

        self.calculate_distance_label = wx.StaticText(self, label="计算在固定坡度要求下，升起对应高度所需的距离")
        self.calculate_distance_label.SetFont(wx.Font(wx.FontInfo(12)))
        self.calculate_distance_label.SetPosition(wx.Point(10, 10))

        self.slope_text_ctrl = wx.TextCtrl(self)
        self.slope_text_ctrl.SetPosition(wx.Point(10, 30))
        self.slope_text_ctrl.SetSize(wx.Size(100, 20))
        self.slope_text_ctrl.SetValue("0.0")
        self.slope_text_unit = wx.StaticText(self, label="‰")
        self.slope_text_unit.SetPosition(wx.Point(110, 30))
        self.slope_text_unit.SetSize(wx.Size(20, 20))

class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None)
        self.frame.Show(True)
        return True


def run_ui():
    """供 app.py 呼叫，啟動 wx 主視窗並進入主迴圈。"""
    app = App()
    app.MainLoop()


if __name__ == "__main__":
    run_ui()

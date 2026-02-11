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
        font = self.calculate_distance_label.GetFont()
        font.PointSize = 12
        self.calculate_distance_label.SetFont(font)
        self.calculate_distance_label.SetPosition(wx.Point(10, 10))

        self.slope_text_ctrl = wx.TextCtrl(self)
        self.slope_text_ctrl.SetPosition(wx.Point(10, 35))
        self.slope_text_ctrl.SetSize(wx.Size(100, 20))
        self.slope_text_ctrl.SetValue("0.0")
        self.slope_text_unit = wx.StaticText(self, label="‰")
        self.slope_text_unit.SetPosition(wx.Point(110, 35))

        self.height_text_ctrl = wx.TextCtrl(self)
        self.height_text_ctrl.SetPosition(wx.Point(210, 35))
        self.height_text_ctrl.SetSize(wx.Size(100, 20))
        self.height_text_ctrl.SetValue("0.0")
        self.height_text_unit = wx.StaticText(self, label="米")
        self.height_text_unit.SetPosition(wx.Point(310, 35))

        self.distance_text_ctrl = wx.TextCtrl(self)
        self.distance_text_ctrl.SetPosition(wx.Point(10, 70))
        self.distance_text_ctrl.SetSize(wx.Size(100, 20))
        self.distance_text_ctrl.SetValue("0.0")
        self.distance_text_unit = wx.StaticText(self, label="米")
        self.distance_text_unit.SetPosition(wx.Point(110, 70))

        self.distance_rounded_text_ctrl = wx.TextCtrl(self)
        self.distance_rounded_text_ctrl.SetPosition(wx.Point(210, 70))
        self.distance_rounded_text_ctrl.SetSize(wx.Size(100, 20))
        self.distance_rounded_text_ctrl.SetValue("0")
        self.distance_rounded_text_unit = wx.StaticText(self, label="米")
        self.distance_rounded_text_unit.SetPosition(wx.Point(310, 70))

        self.slope_length_text_ctrl = wx.TextCtrl(self)
        self.slope_length_text_ctrl.SetPosition(wx.Point(10, 95))
        self.slope_length_text_ctrl.SetSize(wx.Size(100, 20))
        self.slope_length_text_ctrl.SetValue("0.0")
        self.slope_length_text_unit = wx.StaticText(self, label="米")
        self.slope_length_text_unit.SetPosition(wx.Point(110, 95))

        self.calculate_distance_button = wx.Button(self, label="计算")
        self.calculate_distance_button.SetPosition(wx.Point(10, 120))
        self.calculate_distance_button.SetSize(wx.Size(100, 20))
        self.calculate_distance_button.Bind(wx.EVT_BUTTON, self.on_calculate_distance)

    def on_calculate_distance(self, event):
        slope = float(self.slope_text_ctrl.GetValue())/1000
        height = float(self.height_text_ctrl.GetValue())
        result = calc_distance(slope, height)
        self.distance_text_ctrl.SetValue(str(result["distance"]))
        self.distance_rounded_text_ctrl.SetValue(str(result["distance_rounded"]))
        self.slope_length_text_ctrl.SetValue(str(result["slope_length"][0]))

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

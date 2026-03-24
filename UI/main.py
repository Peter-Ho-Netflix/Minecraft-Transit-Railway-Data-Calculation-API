"""
UI 入口。之後將直接 import 並呼叫 features 中的函式，不透過 API。
"""
import math
import wx
from features import calculate_distance as calc_distance
from features import calculate_parallel_turnout_distance as calc_parallel_turnout_distance
from features.main import 计算规定转弯半径和转弯角度下的xy偏移量


def _make_label_input_row(parent, label_text, unit_text, value="0.0", readonly=False):
    """建立「標籤 + 輸入 + 單位」一列，回傳 (hbox, text_ctrl)。"""
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    lbl = wx.StaticText(parent, label=label_text)
    style = wx.TE_READONLY if readonly else 0
    ctrl = wx.TextCtrl(parent, value=value, style=style, size=(100, -1))
    unit = wx.StaticText(parent, label=unit_text)
    hbox.Add(lbl, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
    hbox.Add(ctrl, flag=wx.RIGHT, border=5)
    hbox.Add(unit, flag=wx.ALIGN_CENTER_VERTICAL)
    return hbox, ctrl


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetTitle("Minecraft Transit Railway Calculation API")
        self.SetSize((600, 700))
        self.Center()

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # ----- 分區一：坡度距離計算 -----
        box1 = wx.StaticBoxSizer(wx.VERTICAL, panel, "坡度距離計算（固定坡度下升起對應高度所需距離）")
        box1_inner = box1.GetStaticBox()

        row_slope, self.slope_text_ctrl = _make_label_input_row(box1_inner, "坡度", "‰", "0.0", readonly=False)
        box1.Add(row_slope, flag=wx.ALL, border=5)

        row_height, self.height_text_ctrl = _make_label_input_row(box1_inner, "高度", "米", "0.0", readonly=False)
        box1.Add(row_height, flag=wx.ALL, border=5)

        row_dist, self.distance_text_ctrl = _make_label_input_row(box1_inner, "距离", "米", "—", readonly=True)
        box1.Add(row_dist, flag=wx.ALL, border=5)

        row_dist_r, self.distance_rounded_text_ctrl = _make_label_input_row(box1_inner, "距离（四舍五入）", "米", "—", readonly=True)
        box1.Add(row_dist_r, flag=wx.ALL, border=5)

        row_slope_len, self.slope_length_text_ctrl = _make_label_input_row(box1_inner, "坡长", "米", "—", readonly=True)
        box1.Add(row_slope_len, flag=wx.ALL, border=5)

        btn1 = wx.Button(box1_inner, label="计算")
        btn1.Bind(wx.EVT_BUTTON, self.on_calculate_distance)
        box1.Add(btn1, flag=wx.ALL, border=5)

        main_sizer.Add(box1, flag=wx.EXPAND | wx.ALL, border=10)

        # ----- 分區二：平行道岔距離 -----
        box2 = wx.StaticBoxSizer(wx.VERTICAL, panel, "平行道岔距離（滿足轉彎半徑要求所需經過的距離）")
        box2_inner = box2.GetStaticBox()

        row_radius, self.radius_text_ctrl = _make_label_input_row(box2_inner, "转弯半径", "米", "0.0", readonly=False)
        box2.Add(row_radius, flag=wx.ALL, border=5)

        row_spacing, self.spacing_text_ctrl = _make_label_input_row(box2_inner, "平行道岔间距", "米", "0.0", readonly=False)
        box2.Add(row_spacing, flag=wx.ALL, border=5)

        row_df, self.distance_forward_text_ctrl = _make_label_input_row(box2_inner, "前进距离", "米", "—", readonly=True)
        box2.Add(row_df, flag=wx.ALL, border=5)

        row_df_r, self.distance_forward_rounded_text_ctrl = _make_label_input_row(box2_inner, "前进距离（进一法）", "米", "—", readonly=True)
        box2.Add(row_df_r, flag=wx.ALL, border=5)

        btn2 = wx.Button(box2_inner, label="计算")
        btn2.Bind(wx.EVT_BUTTON, self.on_calculate_parallel_turnout_distance)
        box2.Add(btn2, flag=wx.ALL, border=5)

        main_sizer.Add(box2, flag=wx.EXPAND | wx.ALL, border=10)

        # ----- 分區三：xy 偏移量 -----
        box3 = wx.StaticBoxSizer(wx.VERTICAL, panel, "xy 偏移量")
        box3_inner = box3.GetStaticBox()

        row_r3, self.radius_text_ctrl_xy_offset = _make_label_input_row(box3_inner, "转弯半径", "米", "0.0", readonly=False)
        box3.Add(row_r3, flag=wx.ALL, border=5)

        row_angle, self.angle_text_ctrl_xy_offset = _make_label_input_row(box3_inner, "转弯角度", "°", "0.0", readonly=False)
        box3.Add(row_angle, flag=wx.ALL, border=5)

        row_ext, self.external_x_offset_text_ctrl = _make_label_input_row(box3_inner, "额外x偏移量", "米", "0.0", readonly=False)
        box3.Add(row_ext, flag=wx.ALL, border=5)

        row_x, self.x_text_ctrl_xy_offset = _make_label_input_row(box3_inner, "x偏移量", "米", "—", readonly=True)
        box3.Add(row_x, flag=wx.ALL, border=5)

        row_y, self.y_text_ctrl_xy_offset = _make_label_input_row(box3_inner, "y偏移量", "米", "—", readonly=True)
        box3.Add(row_y, flag=wx.ALL, border=5)

        row_xr, self.x_rounded_text_ctrl = _make_label_input_row(box3_inner, "x偏移量（进一法）", "米", "—", readonly=True)
        box3.Add(row_xr, flag=wx.ALL, border=5)

        row_yr, self.y_rounded_text_ctrl = _make_label_input_row(box3_inner, "y偏移量（进一法）", "米", "—", readonly=True)
        box3.Add(row_yr, flag=wx.ALL, border=5)

        btn3 = wx.Button(box3_inner, label="计算")
        btn3.Bind(wx.EVT_BUTTON, self.on_calculate_xy_offset)
        box3.Add(btn3, flag=wx.ALL, border=5)

        main_sizer.Add(box3, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(main_sizer)
        self.CreateStatusBar()

    def _show_error(self, msg: str) -> None:
        sb = self.GetStatusBar()
        sb.SetStatusText(msg)
        sb.SetBackgroundColour(wx.Colour(255, 200, 200))
        sb.Refresh()

    def _clear_error(self) -> None:
        sb = self.GetStatusBar()
        sb.SetStatusText("")
        sb.SetBackgroundColour(wx.NullColour)
        sb.Refresh()

    def on_calculate_distance(self, event):
        try:
            slope = float(self.slope_text_ctrl.GetValue()) / 1000
            height = float(self.height_text_ctrl.GetValue())
            result = calc_distance(slope, height)
            self._clear_error()
            self.distance_text_ctrl.SetValue(str(result["distance"]))
            self.distance_rounded_text_ctrl.SetValue(str(result["distance_rounded"]))
            self.slope_length_text_ctrl.SetValue(str(result["slope_length"][0]))
        except ValueError:
            self._show_error("輸入格式錯誤：請輸入有效數字（例如 0.0）")
        except (StopIteration, ZeroDivisionError):
            self._show_error("計算無效：無符合條件的解（請檢查坡度、高度是否合理）")
        except Exception as e:
            self._show_error(f"計算失敗：{str(e)}")

    def on_calculate_parallel_turnout_distance(self, event):
        try:
            radius = float(self.radius_text_ctrl.GetValue())
            spacing = float(self.spacing_text_ctrl.GetValue())
            result = calc_parallel_turnout_distance(radius, spacing)
            self._clear_error()
            self.distance_forward_text_ctrl.SetValue(str(result["distance"]))
            self.distance_forward_rounded_text_ctrl.SetValue(str(result["distance_rounded"]))
        except ValueError:
            self._show_error("輸入格式錯誤：請輸入有效數字（例如 0.0）")
        except (StopIteration, ZeroDivisionError):
            self._show_error("計算無效：無符合條件的解（請檢查轉彎半徑、道岔間距是否合理）")
        except Exception as e:
            self._show_error(f"計算失敗：{str(e)}")

    def on_calculate_xy_offset(self, event):
        try:
            radius = float(self.radius_text_ctrl_xy_offset.GetValue())
            angle = float(self.angle_text_ctrl_xy_offset.GetValue()) * math.pi / 180
            external_x_offset = float(self.external_x_offset_text_ctrl.GetValue())
            result = 计算规定转弯半径和转弯角度下的xy偏移量(radius, angle, external_x_offset)
            self._clear_error()
            self.x_text_ctrl_xy_offset.SetValue(str(result["x"]))
            self.y_text_ctrl_xy_offset.SetValue(str(result["y"]))
            self.x_rounded_text_ctrl.SetValue(str(result["x_rounded"]))
            self.y_rounded_text_ctrl.SetValue(str(result["y_rounded"]))
        except ValueError:
            self._show_error("輸入格式錯誤：請輸入有效數字（例如 0.0）")
        except (StopIteration, ZeroDivisionError):
            self._show_error("計算無效：無符合條件的解（請檢查轉彎半徑、轉彎角度是否合理）")
        except Exception as e:
            self._show_error(f"計算失敗：{str(e)}")


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

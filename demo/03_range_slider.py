"""
Demo 3: QRangeSlider - 范围滑块

本 demo 展示 superqt 的 QRangeSlider 控件：
- 双滑块，可以选择一个数值范围
- 实时显示选中的范围
- 应用场景：价格筛选、时间范围选择、数值过滤

QRangeSlider 允许用户选择一段数值范围，常用于筛选、缩放等场景。
"""

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGroupBox
from PySide6.QtCore import Qt
from superqt import QRangeSlider


class RangeSliderDemo(QWidget):
    """QRangeSlider 演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 3: QRangeSlider")
        self.resize(500, 350)

        layout = QVBoxLayout(self)

        # 1. 基本范围滑块
        group1 = QGroupBox("1. 基本范围选择")
        layout1 = QVBoxLayout()
        self.range_label = QLabel("当前范围: 10 - 90")
        self.range_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.range_slider.setRange(0, 100)
        self.range_slider.setValue((10, 90))
        self.range_slider.valueChanged.connect(self.on_range_changed)
        layout1.addWidget(self.range_label)
        layout1.addWidget(self.range_slider)
        group1.setLayout(layout1)
        layout.addWidget(group1)

        # 2. 价格筛选示例
        group2 = QGroupBox("2. 价格筛选 (¥0 - ¥10000)")
        layout2 = QVBoxLayout()
        self.price_label = QLabel("价格范围: ¥1000 - ¥5000")
        self.price_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.price_slider.setRange(0, 10000)
        self.price_slider.setValue((1000, 5000))
        self.price_slider.valueChanged.connect(self.on_price_changed)
        layout2.addWidget(self.price_label)
        layout2.addWidget(self.price_slider)
        group2.setLayout(layout2)
        layout.addWidget(group2)

        # 3. 缩放示例
        group3 = QGroupBox("3. 图表缩放范围")
        layout3 = QVBoxLayout()
        self.zoom_label = QLabel("显示范围: 0% - 100%")
        self.zoom_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(0, 100)
        self.zoom_slider.setValue((0, 100))
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        layout3.addWidget(self.zoom_label)
        layout3.addWidget(self.zoom_slider)
        group3.setLayout(layout3)
        layout.addWidget(group3)

        layout.addStretch()

    def on_range_changed(self, value):
        """处理范围变化"""
        self.range_label.setText(f"当前范围: {value[0]} - {value[1]}")

    def on_price_changed(self, value):
        """处理价格范围变化"""
        self.price_label.setText(f"价格范围: ¥{value[0]} - ¥{value[1]}")

    def on_zoom_changed(self, value):
        """处理缩放范围变化"""
        self.zoom_label.setText(f"显示范围: {value[0]}% - {value[1]}%")


if __name__ == "__main__":
    app = QApplication([])
    window = RangeSliderDemo()
    window.show()
    app.exec()

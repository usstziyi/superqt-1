"""
Demo 12: 综合示例 - 超级控制面板

本 demo 结合多个 superqt 控件，构建一个完整的应用程序：
- QLabeledSlider: 参数调节
- QRangeSlider: 范围筛选
- QEnumComboBox: 模式选择
- QCollapsible: 面板折叠
- QToggleSwitch: 功能开关
- QElidingLabel: 长文本显示
- QSearchableComboBox: 搜索选择

这是一个综合性的示例，展示了如何在实际项目中组合使用 superqt 的各种控件。
"""

from enum import Enum
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QPushButton,
    QTextEdit,
)
from PySide6.QtCore import Qt
from superqt import (
    QLabeledSlider,
    QRangeSlider,
    QEnumComboBox,
    QCollapsible,
    QToggleSwitch,
    QElidingLabel,
    QSearchableComboBox,
)


class ProcessingMode(Enum):
    """处理模式"""
    Fast = "快速模式"
    Balanced = "平衡模式"
    Quality = "质量优先"
    Custom = "自定义"


class ColorScheme(Enum):
    """色彩方案"""
    RGB = "RGB (红绿蓝)"
    CMYK = "CMYK (印刷色)"
    HSV = "HSV (色相/饱和度/明度)"
    LAB = "LAB (感知均匀)"


class ControlPanelDemo(QWidget):
    """综合控制面板"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 12: 综合控制面板")
        self.resize(600, 750)

        layout = QVBoxLayout(self)

        # 标题
        layout.addWidget(QLabel("<h2>🎛️ 超级控制面板</h2>"))
        layout.addWidget(
            QElidingLabel("这是一个综合示例，展示了 superqt 各种控件的组合使用")
        )

        # 1. 基本参数设置
        self.params = QCollapsible("基本参数")
        self.params.layout().setContentsMargins(0, 0, 0, 0)
        self.params.setStyleSheet("QCollapsible { border: none; }")
        params_layout = self.params.content().layout()

        params_layout.addWidget(QLabel("处理模式:"))
        self.mode_combo = QEnumComboBox()
        self.mode_combo.setEnumClass(ProcessingMode)
        params_layout.addWidget(self.mode_combo)

        params_layout.addWidget(QLabel("亮度:"))
        self.brightness = QLabeledSlider(Qt.Orientation.Horizontal)
        self.brightness.setRange(0, 100)
        self.brightness.setValue(50)
        params_layout.addWidget(self.brightness)

        params_layout.addWidget(QLabel("对比度:"))
        self.contrast = QLabeledSlider(Qt.Orientation.Horizontal)
        self.contrast.setRange(-50, 50)
        self.contrast.setValue(0)
        params_layout.addWidget(self.contrast)
        layout.addWidget(self.params)

        # 2. 范围筛选
        self.range_group = QCollapsible("范围设置")
        self.range_group.layout().setContentsMargins(0, 0, 0, 0)
        self.range_group.setStyleSheet("QCollapsible { border: none; }")
        range_layout = self.range_group.content().layout()

        range_layout.addWidget(QLabel("处理范围:"))
        self.range_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.range_slider.setRange(0, 100)
        self.range_slider.setValue((10, 90))
        range_layout.addWidget(self.range_slider)

        range_layout.addWidget(QLabel("色彩空间:"))
        self.color_combo = QEnumComboBox()
        self.color_combo.setEnumClass(ColorScheme)
        range_layout.addWidget(self.color_combo)
        layout.addWidget(self.range_group)

        # 3. 功能开关
        self.features = QCollapsible("功能开关")
        features_layout = self.features.content().layout()

        self.auto_enhance = QToggleSwitch(text="自动增强")
        features_layout.addWidget(self.auto_enhance)

        self.noise_reduction = QToggleSwitch(text="降噪处理")
        self.noise_reduction.setChecked(True)
        features_layout.addWidget(self.noise_reduction)

        self.sharpen = QToggleSwitch(text="锐化")
        features_layout.addWidget(self.sharpen)

        self.batch_mode = QToggleSwitch(text="批处理模式")
        features_layout.addWidget(self.batch_mode)
        layout.addWidget(self.features)

        # 4. 输出设置
        self.output = QCollapsible("输出设置")
        output_layout = self.output.content().layout()

        output_layout.addWidget(QLabel("输出格式:"))
        self.format_combo = QSearchableComboBox()
        self.format_combo.addItems([
            "PNG", "JPEG", "WEBP", "TIFF", "BMP", "GIF", "SVG"
        ])
        output_layout.addWidget(self.format_combo)

        output_layout.addWidget(QLabel("输出质量:"))
        self.quality = QLabeledSlider(Qt.Orientation.Horizontal)
        self.quality.setRange(1, 100)
        self.quality.setValue(90)
        output_layout.addWidget(self.quality)
        layout.addWidget(self.output)

        # 5. 操作按钮
        btn_layout = QHBoxLayout()
        self.apply_btn = QPushButton("应用设置")
        self.apply_btn.clicked.connect(self.apply_settings)
        btn_layout.addWidget(self.apply_btn)

        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_settings)
        btn_layout.addWidget(self.reset_btn)
        layout.addLayout(btn_layout)

        # 状态显示
        layout.addWidget(QLabel("当前配置:"))
        self.config_text = QTextEdit()
        self.config_text.setReadOnly(True)
        self.config_text.setMaximumHeight(120)
        layout.addWidget(self.config_text)
        layout.addStretch()

        self.update_config()

    def apply_settings(self):
        """应用设置"""
        self.update_config()
        self.config_text.append("\n✅ 设置已应用!")

    def reset_settings(self):
        """重置设置"""
        self.brightness.setValue(50)
        self.contrast.setValue(0)
        self.range_slider.setValue((10, 90))
        self.quality.setValue(90)
        self.auto_enhance.setChecked(False)
        self.noise_reduction.setChecked(True)
        self.sharpen.setChecked(False)
        self.batch_mode.setChecked(False)
        self.update_config()
        self.config_text.append("\n🔄 设置已重置!")

    def update_config(self):
        """更新配置显示"""
        config = (
            f"模式: {self.mode_combo.currentEnum().name}\n"
            f"亮度: {self.brightness.value()}\n"
            f"对比度: {self.contrast.value()}\n"
            f"范围: {self.range_slider.value()[0]} - {self.range_slider.value()[1]}\n"
            f"色彩: {self.color_combo.currentEnum().name}\n"
            f"格式: {self.format_combo.currentText()}\n"
            f"质量: {self.quality.value()}\n"
            f"自动增强: {'是' if self.auto_enhance.isChecked() else '否'}\n"
            f"降噪: {'是' if self.noise_reduction.isChecked() else '否'}\n"
            f"锐化: {'是' if self.sharpen.isChecked() else '否'}\n"
            f"批处理: {'是' if self.batch_mode.isChecked() else '否'}"
        )
        self.config_text.setText(config)


if __name__ == "__main__":
    app = QApplication([])
    window = ControlPanelDemo()
    window.show()
    app.exec()

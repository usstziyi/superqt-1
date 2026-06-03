"""
Demo 4: QEnumComboBox - 枚举下拉框

本 demo 展示 superqt 的 QEnumComboBox 控件：
- 基于 Python Enum 自动填充下拉选项
- 类型安全的选择
- 应用场景：设置面板、模式选择、状态切换

QEnumComboBox 继承自 QComboBox，但使用 Python Enum 来填充选项，
确保选择的类型安全和代码可维护性。
"""

from enum import Enum
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QTextEdit,
)
from superqt import QEnumComboBox


# 定义各种枚举类型
class Theme(Enum):
    """主题枚举"""
    Light = "浅色主题"
    Dark = "深色主题"
    System = "跟随系统"


class Language(Enum):
    """语言枚举"""
    Chinese = "中文"
    English = "English"
    Japanese = "日本語"
    Korean = "한국어"


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = "调试信息"
    INFO = "一般信息"
    WARNING = "警告信息"
    ERROR = "错误信息"
    CRITICAL = "严重错误"


class EnumComboBoxDemo(QWidget):
    """QEnumComboBox 演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 4: QEnumComboBox")
        self.resize(500, 500)

        layout = QVBoxLayout(self)

        # 1. 主题选择
        group1 = QGroupBox("1. 选择主题")
        layout1 = QVBoxLayout()
        self.theme_combo = QEnumComboBox()
        self.theme_combo.setEnumClass(Theme)
        self.theme_combo.currentEnumChanged.connect(self.on_theme_changed)
        layout1.addWidget(self.theme_combo)
        group1.setLayout(layout1)
        layout.addWidget(group1)

        # 2. 语言选择
        group2 = QGroupBox("2. 选择语言")
        layout2 = QVBoxLayout()
        self.lang_combo = QEnumComboBox()
        self.lang_combo.setEnumClass(Language)
        self.lang_combo.currentEnumChanged.connect(self.on_language_changed)
        layout2.addWidget(self.lang_combo)
        group2.setLayout(layout2)
        layout.addWidget(group2)

        # 3. 日志级别选择
        group3 = QGroupBox("3. 设置日志级别")
        layout3 = QVBoxLayout()
        self.log_combo = QEnumComboBox()
        self.log_combo.setEnumClass(LogLevel)
        self.log_combo.currentEnumChanged.connect(self.on_log_level_changed)
        layout3.addWidget(self.log_combo)
        group3.setLayout(layout3)
        layout.addWidget(group3)

        # 显示当前设置的文本区域
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(150)
        layout.addWidget(QLabel("当前设置状态:"))
        layout.addWidget(self.info_text)

        # 初始化状态
        self.current_theme = Theme.Light
        self.current_lang = Language.Chinese
        self.current_log = LogLevel.INFO
        self.update_info()

    def on_theme_changed(self, theme: Theme):
        """主题改变时的处理"""
        self.current_theme = theme
        self.update_info()

    def on_language_changed(self, lang: Language):
        """语言改变时的处理"""
        self.current_lang = lang
        self.update_info()

    def on_log_level_changed(self, level: LogLevel):
        """日志级别改变时的处理"""
        self.current_log = level
        self.update_info()

    def update_info(self):
        """更新状态显示"""
        text = (
            f"主题: {self.current_theme.name} ({self.current_theme.value})\n"
            f"语言: {self.current_lang.name} ({self.current_lang.value})\n"
            f"日志级别: {self.current_log.name} ({self.current_log.value})"
        )
        self.info_text.setText(text)


if __name__ == "__main__":
    app = QApplication([])
    window = EnumComboBoxDemo()
    window.show()
    app.exec()

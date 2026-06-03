"""
Demo 10: 线程装饰器 - 后台任务处理

本 demo 展示 superqt 的线程装饰器工具：
- @thread_worker: 在后台线程运行函数
- 保持 GUI 响应性
- 应用场景：文件加载、网络请求、数据处理

在 GUI 编程中，耗时操作会阻塞主线程导致界面卡顿。
superqt 提供了简洁的装饰器来将函数放到后台线程执行。
"""

import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QTextEdit,
)
from superqt.utils import thread_worker


class ThreadingDemo(QWidget):
    """线程装饰器演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 10: 线程装饰器")
        self.resize(550, 500)

        layout = QVBoxLayout(self)

        # 添加说明
        layout.addWidget(
            QLabel(
                "<h2>thread_worker - 后台任务处理</h2>"
                "<p>耗时操作在后台线程执行，界面保持响应</p>"
            )
        )

        # 进度条
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

        # 状态标签
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.start_btn = QPushButton("开始耗时任务 (后台)")
        self.start_btn.clicked.connect(self.run_background_task)
        btn_layout.addWidget(self.start_btn)

        self.block_btn = QPushButton("开始耗时任务 (阻塞)")
        self.block_btn.clicked.connect(self.run_blocking_task)
        btn_layout.addWidget(self.block_btn)

        layout.addLayout(btn_layout)

        # 日志输出
        layout.addWidget(QLabel("操作日志:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # 计数器（用于证明界面没有卡住）
        self.counter_label = QLabel("计数器: 0")
        layout.addWidget(self.counter_label)

    def log(self, message):
        """添加日志"""
        current = self.log_text.toPlainText()
        self.log_text.setText(current + message + "\n")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    @thread_worker
    def background_task(self):
        """后台任务 - 使用装饰器自动在后台线程运行"""
        for i in range(1, 11):
            time.sleep(0.3)  # 模拟耗时操作
            self.log(f"后台任务进度: {i * 10}%")
            # 通过信号更新进度条
            self.update_progress.emit(i * 10)
        return "后台任务完成!"

    def run_background_task(self):
        """启动后台任务"""
        self.status_label.setText("正在执行后台任务...")
        self.log("启动后台任务...")
        self.start_btn.setEnabled(False)

        worker = self.background_task()
        worker.returned.connect(self.on_task_finished)
        worker.started.connect(lambda: self.log("任务开始执行"))

    def run_blocking_task(self):
        """启动阻塞任务（会卡住界面）"""
        self.status_label.setText("正在执行阻塞任务 (界面将卡住)...")
        self.log("启动阻塞任务...")
        self.block_btn.setEnabled(False)

        # 直接在主线程执行，会卡住界面
        for i in range(1, 11):
            time.sleep(0.3)
            self.log(f"阻塞任务进度: {i * 10}%")
            self.progress.setValue(i * 10)

        self.status_label.setText("阻塞任务完成!")
        self.log("阻塞任务完成")
        self.block_btn.setEnabled(True)

    def on_task_finished(self, result):
        """任务完成回调"""
        self.status_label.setText(result)
        self.progress.setValue(100)
        self.log(result)
        self.start_btn.setEnabled(True)

    def update_progress(self, value):
        """更新进度条"""
        self.progress.setValue(value)

    def update_counter(self):
        """更新计数器"""
        if hasattr(self, '_counter'):
            self._counter += 1
        else:
            self._counter = 1
        self.counter_label.setText(f"计数器: {self._counter}")


if __name__ == "__main__":
    app = QApplication([])
    window = ThreadingDemo()

    # 使用定时器更新计数器，证明界面没有卡住
    from PySide6.QtCore import QTimer
    timer = QTimer()
    timer.timeout.connect(window.update_counter)
    timer.start(100)

    window.show()
    app.exec()

# ui/animated_stack.py
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, pyqtSlot, Qt

class AnimatedStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation_duration = 400  # мс
        self._anim = QPropertyAnimation(self, b"geometry", self)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def slide_to_index(self, index: int):
        if index == self.currentIndex():
            return
        current_widget = self.currentWidget()
        next_widget = self.widget(index)

        # Показываем next_widget за пределами текущей геометрии
        direction = 1 if index > self.currentIndex() else -1
        rect = self.frameRect()
        offset = rect.width() * direction
        next_widget.setGeometry(rect.translated(offset, 0))
        next_widget.show()

        # Анимируем текущий и следующий виджеты
        anim_out = QPropertyAnimation(current_widget, b"geometry", self)
        anim_in = QPropertyAnimation(next_widget, b"geometry", self)
        anim_out.setDuration(self._animation_duration)
        anim_in.setDuration(self._animation_duration)

        anim_out.setStartValue(rect)
        anim_out.setEndValue(rect.translated(-offset, 0))
        anim_in.setStartValue(rect.translated(offset, 0))
        anim_in.setEndValue(rect)

        anim_out.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim_in.setEasingCurve(QEasingCurve.Type.InOutCubic)

        def on_finish():
            self.setCurrentIndex(index)
            next_widget.setGeometry(rect)

        anim_out.finished.connect(on_finish)
        anim_out.start()
        anim_in.start()

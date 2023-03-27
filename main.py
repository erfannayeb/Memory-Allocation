import sys

from PyQt5.QtWidgets import QApplication, QStackedWidget
import segmentation
import paging


class SegmentationRoot(segmentation.Segmentation):
    def __init__(self):
        super().__init__()
        self.pushButton_paging.clicked.connect(self.go_to_paging)
        self.pushButton_segmentation.setEnabled(False)

    def go_to_paging(self):
        pagingWindow = PagingRoot()
        widget.addWidget(pagingWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class PagingRoot(paging.Paging):
    def __init__(self):
        super().__init__()
        self.pushButton_segmentation.clicked.connect(self.go_to_demo_page)
        self.pushButton_paging.setEnabled(False)

    def go_to_demo_page(self):
        segmentWindow = SegmentationRoot()
        widget.addWidget(segmentWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    mainWindow = SegmentationRoot()
    widget.setFixedWidth(1097)
    widget.setFixedHeight(750)
    widget.addWidget(mainWindow)
    widget.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

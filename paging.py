import math
from typing import List
import random

from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QTableWidgetItem, QWidget
from PyQt5 import uic

from memory import Memory
from page import Page
from segment import Segment
from request import Request


class Paging(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('paging.ui', self)

        self.row = 0
        self.time = -1
        self.memory = Memory
        self.number_of_seg: int
        self.requests: List[Request]
        self.segments: List[Segment]
        self.pages: List[Page] = []
        self.frame_unit: int
        self.frame_dict: dict
        self.total_unit: int
        self.free_unit: int

        self.pushButton_SIMULATE.setEnabled(False)
        self.pushButton_increase_time.setEnabled(False)
        self.pushButton_reset.setEnabled(False)

        self.button_set_info.clicked.connect(self.set_info)
        self.pushButton_increase_time.clicked.connect(self.increase_time)
        self.pushButton_add_request.clicked.connect(self.add_request)
        self.pushButton_SIMULATE.clicked.connect(self.simulate)
        self.pushButton_remove_request.clicked.connect(self.remove_request)
        self.pushButton_reset.clicked.connect(self.reset)

    def set_info(self):
        user_space = self.spinBox_user_space.text()
        os_space = self.spinBox_os_space.text()
        frame_unit = self.spinBox_num_frame_unit.text()
        self.number_of_seg = int(self.spinBox_num_segments.text())

        self.memory.user_space = int(user_space)
        self.memory.os_space = int(os_space)
        self.frame_unit = int(frame_unit)
        self.pushButton_SIMULATE.setEnabled(True)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Set information successfully")
        msg.exec()

    def increase_time(self):
        self.time += 1
        # Add request to paging table
        remain_requests = []
        for request in self.requests:
            if request.space_need <= self.free_unit and request.arrival_time <= self.time:
                self.free_unit -= request.space_need
                for i in range(0, request.space_need):
                    for frame_id, page_id in self.frame_dict.items():
                        if page_id == -1:
                            page = Page('req_' + str(request.req_id), frame_id, end_time=request.time_need + self.time)
                            self.pages.append(page)
                            self.frame_dict[frame_id] = page.page_id
                            break
            else:
                remain_requests.append(request)
        self.requests = remain_requests

        # Remove request from paging table
        remain_pages = []
        for page in self.pages:
            if page.end_time != -1 and page.end_time <= self.time:
                self.frame_dict[page.frame_id] = -1
                self.free_unit += 1
            else:
                remain_pages.append(page)

        self.pages = remain_pages
        self.update_ui_page_table()
        self.label_time_num.setText(str(self.time))

    def add_request(self):
        request_ID = self.spinBox_request_ID.text()
        space_need = self.spinBox_space_need.text()
        arrival_time = self.spinBox_arrival_time.text()
        time_need = self.spinBox_time_need.text()
        data = {
            'request_ID': str(request_ID),
            'space_need': str(space_need),
            'arrival_time': str(arrival_time),
            'time_need': str(time_need)
        }

        self.tableWidget_request_memory.setRowCount(self.row + 1)
        self.tableWidget_request_memory.setItem(self.row, 0, QTableWidgetItem(data['request_ID']))
        self.tableWidget_request_memory.setItem(self.row, 1, QTableWidgetItem(data['space_need']))
        self.tableWidget_request_memory.setItem(self.row, 2, QTableWidgetItem(data['arrival_time']))
        self.tableWidget_request_memory.setItem(self.row, 3, QTableWidgetItem(data['time_need']))
        self.row += 1

        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Information)
        # msg.setText("Added successfully")
        # msg.exec()

    def simulate(self):
        self.time = -1
        self.requests = []
        self.set_requests()
        self.set_segments()

        self.update_page_table()

        self.pushButton_increase_time.setEnabled(True)
        self.pushButton_SIMULATE.setEnabled(False)
        self.button_set_info.setEnabled(False)
        self.pushButton_add_request.setEnabled(False)
        self.pushButton_remove_request.setEnabled(False)
        self.pushButton_reset.setEnabled(True)

        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def update_page_table(self):
        self.segments.sort(key=lambda obj: obj.id)

        for segment in self.segments:
            if self.free_unit >= segment.num_page:
                self.free_unit -= segment.num_page
                for i in range(0, segment.num_page):
                    for frame_id, page_id in self.frame_dict.items():
                        if page_id == -1:
                            page = Page(segment.id, frame_id)
                            self.pages.append(page)
                            self.frame_dict[frame_id] = page.page_id
                            break

        self.update_ui_page_table()

    def update_ui_page_table(self):
        self.tableWidget_segments.setRowCount(self.total_unit - self.free_unit)
        for index, page in enumerate(self.pages):
            self.tableWidget_segments.setItem(index, 0, QTableWidgetItem(str(page.id)))
            self.tableWidget_segments.setItem(index, 1, QTableWidgetItem(str(page.page_id)))
            self.tableWidget_segments.setItem(index, 2, QTableWidgetItem(str(page.frame_id)))

    def set_requests(self):
        for row in range(0, self.row):
            request_id = self.tableWidget_request_memory.item(row, 0).text()
            space_need = self.tableWidget_request_memory.item(row, 1).text()
            arrival_time = self.tableWidget_request_memory.item(row, 2).text()
            time_need = self.tableWidget_request_memory.item(row, 3).text()

            request = Request(int(request_id),
                              math.ceil(int(space_need) / self.frame_unit),
                              int(arrival_time),
                              int(time_need))
            self.requests.append(request)

    def set_segments(self):
        self.segments = []
        # OS segment
        self.segments.append(Segment(seg_id='OS_seg', num_page=math.ceil(self.memory.os_space / self.frame_unit)))

        max_memory = int(self.memory.os_space) + int(self.memory.user_space)
        min_memory = int(self.memory.os_space)
        self.total_unit = int(max_memory / self.frame_unit)
        self.free_unit = self.total_unit
        self.frame_dict = {}

        for i in range(0, self.total_unit):
            self.frame_dict[i] = -1

        if self.number_of_seg != 0:

            base_addresses = []

            for _ in range(0, self.number_of_seg):
                base_addresses.append(random.randint(min_memory, max_memory + 1))
            base_addresses.sort()

            for i in range(0, self.number_of_seg - 1):
                if base_addresses[i + 1] - base_addresses[i] < 2:
                    return self.set_segments()
                else:
                    limit = random.randint(1, base_addresses[i + 1] - base_addresses[i] - 1)
                self.segments.append(Segment(seg_id='seg_' + str(i + 1), num_page=math.ceil(limit / self.frame_unit)))

            # last segment
            self.segments.append(Segment(seg_id='seg_' + str(self.number_of_seg),
                                         num_page=math.ceil(
                                             random.randint(0, max_memory - base_addresses[-1]) / self.frame_unit)))

    def remove_request(self):
        if self.tableWidget_request_memory.rowCount() > 0:
            currentRow = self.tableWidget_request_memory.currentRow()
            self.tableWidget_request_memory.removeRow(currentRow)
            self.row -= 1

    def reset(self):
        self.time = -1
        self.label_time_num.setText('n')

        removed_pages = []
        for i in range(0, len(self.pages)):
            removed_pages.append(i)

        removed_pages.reverse()
        for i in removed_pages:
            self.tableWidget_segments.removeRow(i)

        self.pages = []
        for _ in range(0, self.row):
            self.tableWidget_request_memory.removeRow(self.row - 1)
            self.row -= 1

        self.number_of_seg = 0
        self.spinBox_user_space.setValue(100)
        self.spinBox_os_space.setValue(100)
        self.spinBox_num_segments.setValue(0)
        self.spinBox_num_frame_unit.setValue(1)
        self.pushButton_increase_time.setEnabled(False)
        self.button_set_info.setEnabled(True)
        self.pushButton_add_request.setEnabled(True)
        self.pushButton_remove_request.setEnabled(True)
        self.pushButton_reset.setEnabled(False)

        # edit tabel triggers
        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.EditKeyPressed)
        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.AnyKeyPressed)
        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.AllEditTriggers)

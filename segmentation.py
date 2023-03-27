from typing import List
import random

from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QTableWidgetItem, QWidget
from PyQt5 import uic

from memory import Memory
from segment import Segment
from request import Request


class Segmentation(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('segmentation.ui', self)

        self.row = 0
        self.time = -1
        self.memory = Memory
        self.number_of_seg: int
        self.requests: List[Request]
        self.segments: List[Segment]
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
        self.number_of_seg = int(self.spinBox_num_segments.text())
        self.memory.user_space = user_space
        self.memory.os_space = os_space
        self.pushButton_SIMULATE.setEnabled(True)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Set information successfully")
        msg.exec()

    def increase_time(self):
        max_memory = int(self.memory.os_space) + int(self.memory.user_space)

        self.time += 1

        # Add request to segment
        removed_index = []
        if self.segments:
            self.segments.sort(key=lambda obj: obj.base_addr)

            for index, request in enumerate(self.requests):
                if self.number_of_seg == 0 and request.arrival_time <= self.time:
                    if request.space_need < max_memory - (self.segments[-1].base_addr + self.segments[-1].limit):
                        new_seg = Segment('req_' + str(request.req_id),
                                          self.segments[-1].base_addr + self.segments[-1].limit + 1,
                                          request.space_need,
                                          self.time + request.time_need)
                        self.segments.append(new_seg)
                        self.segments.sort(key=lambda obj: obj.base_addr)
                        removed_index.append(index)
                        self.number_of_seg += 1

                elif request.arrival_time <= self.time:
                    for i in range(0, self.number_of_seg):
                        if request.space_need < self.segments[i + 1].base_addr - (self.segments[i].base_addr + self.segments[i].limit):
                            removed_index.append(index)
                            self.number_of_seg += 1
                            new_seg = Segment('req_' + str(request.req_id),
                                              self.segments[i].base_addr + self.segments[i].limit + 1,
                                              request.space_need,
                                              self.time + request.time_need)
                            self.segments.append(new_seg)
                            self.segments.sort(key=lambda obj: obj.base_addr)
                            break

                        elif request.space_need < max_memory - (self.segments[-1].base_addr + self.segments[-1].limit):
                            removed_index.append(index)
                            self.number_of_seg += 1
                            new_seg = Segment('req_' + str(request.req_id),
                                              self.segments[-1].base_addr + self.segments[-1].limit + 1,
                                              request.space_need,
                                              self.time + request.time_need)
                            self.segments.append(new_seg)
                            self.segments.sort(key=lambda obj: obj.base_addr)
                            break

            removed_index.sort(reverse=True)
            for i in removed_index:
                del self.requests[i]

        removed_segments = []
        for i in range(0, len(self.segments)):
            if self.segments[i].end_time != -1 and self.segments[i].end_time <= self.time:
                removed_segments.append(i)
                self.number_of_seg -= 1

        removed_segments.sort(reverse=True)
        for i in removed_segments:
            del self.segments[i]

        self.update_segment_table()
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

        self.update_segment_table()

        self.pushButton_increase_time.setEnabled(True)
        self.pushButton_SIMULATE.setEnabled(False)
        self.button_set_info.setEnabled(False)
        self.pushButton_add_request.setEnabled(False)
        self.pushButton_remove_request.setEnabled(False)
        self.pushButton_reset.setEnabled(True)

        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def update_segment_table(self):
        self.segments.sort(key=lambda obj: obj.base_addr)

        self.tableWidget_segments.setRowCount(self.number_of_seg + 1)
        for i in range(0, self.number_of_seg + 1):
            self.tableWidget_segments.setItem(i, 0, QTableWidgetItem(str(self.segments[i].id)))
            self.tableWidget_segments.setItem(i, 1, QTableWidgetItem(str(self.segments[i].base_addr)))
            self.tableWidget_segments.setItem(i, 2, QTableWidgetItem(str(self.segments[i].limit)))

    def set_requests(self):
        for row in range(0, self.row):
            request_id = self.tableWidget_request_memory.item(row, 0).text()
            space_need = self.tableWidget_request_memory.item(row, 1).text()
            arrival_time = self.tableWidget_request_memory.item(row, 2).text()
            time_need = self.tableWidget_request_memory.item(row, 3).text()

            request = Request(int(request_id), int(space_need),
                              int(arrival_time), int(time_need))
            self.requests.append(request)

    def set_segments(self):
        self.segments = []
        # OS segment
        self.segments.append(Segment('OS_seg', 0, int(self.memory.os_space)))

        if self.number_of_seg != 0:
            max_memory = int(self.memory.os_space) + int(self.memory.user_space)
            min_memory = int(self.memory.os_space)
            base_addresses = []

            for _ in range(0, self.number_of_seg):
                base_addresses.append(random.randint(min_memory, max_memory + 1))
            base_addresses.sort()

            for i in range(0, self.number_of_seg - 1):
                if base_addresses[i + 1] - base_addresses[i] < 2:
                    return self.set_segments()
                else:
                    limit = random.randint(1, base_addresses[i + 1] - base_addresses[i] - 1)
                self.segments.append(Segment(i + 1, base_addresses[i], limit))

            # last segment
            self.segments.append(Segment(self.number_of_seg,
                                         base_addresses[-1],
                                         random.randint(0, max_memory - base_addresses[-1])))

    def remove_request(self):
        if self.tableWidget_request_memory.rowCount() > 0:
            currentRow = self.tableWidget_request_memory.currentRow()
            self.tableWidget_request_memory.removeRow(currentRow)
            self.row -= 1

    def reset(self):
        self.time = -1
        self.label_time_num.setText('n')

        for _ in range(0, self.number_of_seg + 1):
            self.tableWidget_segments.removeRow(self.number_of_seg)
            self.number_of_seg -= 1
        for _ in range(0, self.row):
            self.tableWidget_request_memory.removeRow(self.row - 1)
            self.row -= 1

        self.number_of_seg = 0
        self.spinBox_user_space.setValue(100)
        self.spinBox_os_space.setValue(100)
        self.spinBox_num_segments.setValue(0)
        self.pushButton_increase_time.setEnabled(False)
        self.button_set_info.setEnabled(True)
        self.pushButton_add_request.setEnabled(True)
        self.pushButton_remove_request.setEnabled(True)
        self.pushButton_reset.setEnabled(False)

        # edit tabel
        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.EditKeyPressed)
        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.AnyKeyPressed)
        self.tableWidget_request_memory.setEditTriggers(QAbstractItemView.AllEditTriggers)

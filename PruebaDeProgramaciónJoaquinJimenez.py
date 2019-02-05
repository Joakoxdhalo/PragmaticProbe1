"""
Prueba de software Pragmatic
Creador del proyecto: Joaquín Alonso Jiménez Caviedes
Fecha de inicio: 26/12/2018
"""

import time
import os
from PyQt5.QtWidgets import QApplication
import sys

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, QFrame, QWidget, QComboBox,
    QGridLayout, QHBoxLayout, QVBoxLayout, QDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


###############################################################################
# Class FinishDialog
###############################################################################


class FinishDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmation dialog")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        # create objects
        self.dialog_message = QLabel("")
        self.dialog_message.setText("<p align='center'>All the data is correct and ready to print?")

        self.frame = QFrame()

        self.accept_button = QPushButton("YES")
        self.cancel_button = QPushButton("NO")

        self.accept_button.setMinimumSize(90, 36)
        self.cancel_button.setMinimumSize(90, 36)

        self.accept_button.setMaximumSize(90, 36)
        self.cancel_button.setMaximumSize(90, 36)

        self.accept_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

        # connections
        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # layout
        self.layout = QVBoxLayout()
        self.vlayout = QVBoxLayout(self.frame)
        self.hlayout = QHBoxLayout()

        self.layout.addWidget(self.frame)
        self.vlayout.addWidget(self.dialog_message)
        self.vlayout.addLayout(self.hlayout)
        self.hlayout.addWidget(self.accept_button)
        self.hlayout.addWidget(self.cancel_button)
        self.setLayout(self.layout)
        self.setModal(True)
        self.show()


###############################################################################
# Class DataBaseAccess
###############################################################################

class DataBaseAccess():
    database_filename = "TheSoftwareTaste.DB"
    engine = create_engine("sqlite:///{}".format(database_filename), echo=False)
    Base = declarative_base(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    def __init__(self):
        self.amount_of_inks_table = self.session.query(self.amount_of_inks)
        self.kind_of_paper_table = self.session.query(self.kind_of_paper)
        self.kind_of_print_table = self.session.query(self.kind_of_print)
        self.printing_machine_table = self.session.query(self.printing_machine)
        self.utility_table = self.session.query(self.utility)

    class amount_of_inks(Base):
        __tablename__ = 'AmountOfInks'
        __table_args__ = {'autoload': True}

    class kind_of_paper(Base):
        __tablename__ = 'KindOfPaper'
        __table_args__ = {'autoload': True}

    class kind_of_print(Base):
        __tablename__ = 'KindOfPrint'
        __table_args__ = {'autoload': True}

    class printing_machine(Base):
        __tablename__ = 'PrintingMachine'
        __table_args__ = {'autoload': True}

    class utility(Base):
        __tablename__ = 'Utility'
        __table_args__ = {'autoload': True}


###############################################################################
# Class MainWindow
###############################################################################


class MainWindow(QMainWindow):

    def __init__(self, *args):
        super().__init__()
        QThread.currentThread().setObjectName('GUI')
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # Creating objects:
        self.database = DataBaseAccess()

        self.amount_of_inks_list = [i.types for i in self.database.amount_of_inks_table]
        self.kind_of_paper_list = ["{}, cost: {} pesos per square meter".format(i.origin, i.cost_in_pesos_per_square_meter) for i in self.database.kind_of_paper_table]
        self.kind_of_print_list = [i.types for i in self.database.kind_of_print_table]
        self.printing_machine_list = ["{}, preparation time[h]: {}, roll length[in]: {}, printing speed[in/min]: {}".format(i.branch, i.preparation_time_in_hours, i.roll_length_in_inches, i.printing_speed_in_inches_per_minute) for i in self.database.printing_machine_table]
        self.utility_list = [i.percentage for i in self.database.utility_table]

        self.client_name_edit = QLineEdit('')
        self.client_locality_edit = QLineEdit('')
        self.client_phone_edit = QLineEdit('')
        self.client_adress_edit = QLineEdit('')
        self.client_city_edit = QLineEdit('')
        self.client_mail_edit = QLineEdit('')

        self.width_of_each_label_edit = QLineEdit('')
        self.length_of_each_label_edit = QLineEdit('')
        self.space_between_labels_edit = QLineEdit('')
        self.list_of_labels_to_quote_edit = QLineEdit('')
        self.amount_of_labels_edit = QLineEdit('')

        self.impressions_label = QLabel("Impressions 'The Software Taste'")
        self.autor_label = QLabel('by Joaquín Jiménez')
        self.quotation_label = QLabel('Quotation')

        self.client_information = QLabel('Client information')
        self.client_name = QLabel('Name:')
        self.client_locality = QLabel('Locality:')
        self.client_phone = QLabel('Phone:')
        self.client_adress = QLabel("Adress:")
        self.client_city = QLabel('City:')
        self.client_mail = QLabel('E-mail:')

        self.quotation_elements = QLabel('Quotation elements')
        self.amount_of_inks_label = QLabel('Amount of inks:')
        self.kind_of_paper_label = QLabel('Kind of paper:')
        self.kind_of_print_label = QLabel('Kinf of print:')
        self.printing_machine_label = QLabel('Printing machine:')
        self.width_of_each_label = QLabel('Width of each label:')
        self.length_of_each_label = QLabel('Length of each label:')
        self.space_between_labels = QLabel('Space between labels in the paper:')
        self.amount_of_labels = QLabel('Separe by a comma the amount of labels that you want to quotate, (example: 200, 100, 50, 500):')
        self.utility_label = QLabel('Utility:')
        self.millimetersLabel = QLabel('mm')
        self.millimetersLabel2 = QLabel('mm')
        self.millimetersLabel3 = QLabel('mm')

        self.amount_of_inks_select = QComboBox()
        self.kind_of_paper_select = QComboBox()
        self.kind_of_print_select = QComboBox()
        self.printing_machine_select = QComboBox()
        self.utility_select = QComboBox()

        self.amount_of_inks_select.addItem("Select")
        self.kind_of_paper_select.addItem("Select")
        self.kind_of_print_select.addItem("Select")
        self.printing_machine_select.addItem("Select")
        self.utility_select.addItem("Select")

        for i in self.amount_of_inks_list:
            self.amount_of_inks_select.addItem(str(i))

        for i in self.kind_of_paper_list:
            self.kind_of_paper_select.addItem(i)

        for i in self.kind_of_print_list:
            self.kind_of_print_select.addItem(i)

        for i in self.printing_machine_list:
            self.printing_machine_select.addItem(i)

        for i in self.utility_list:
            self.utility_select.addItem(str(i))

        self.finish_quotation_button = QPushButton("Finish quotation")
        self.finish_quotation_button.clicked.connect(self.create_dialog)
        self.finish_quotation_button.setMinimumSize(200, 50)
        self.finish_quotation_button.setMaximumSize(200, 50)

        self.frame_up = QFrame()
        self.frame_down = QFrame()

        self.main_layout = QVBoxLayout(widget)
        self.button_layout = QHBoxLayout()
        self.LabelsAmountLayout = QVBoxLayout()

        self.grid_layout_for_large_option_boxes = QGridLayout()
        self.grid_layout_for_large_option_boxes.addWidget(self.kind_of_paper_label, 1, 1)
        self.grid_layout_for_large_option_boxes.addWidget(self.kind_of_paper_select, 1, 2)
        self.grid_layout_for_large_option_boxes.addWidget(self.printing_machine_label, 2, 1)
        self.grid_layout_for_large_option_boxes.addWidget(self.printing_machine_select, 2, 2)

        self.button_layout.addWidget(self.finish_quotation_button)
        self.client_info_vertical_layout = QVBoxLayout(self.frame_up)

        self.client_info_grid_layout = QGridLayout()
        self.client_info_grid_layout.addWidget(self.client_name, 1, 1)
        self.client_info_grid_layout.addWidget(self.client_name_edit, 1, 2)
        self.client_info_grid_layout.addWidget(self.client_adress, 1, 3)
        self.client_info_grid_layout.addWidget(self.client_adress_edit, 1, 4)
        self.client_info_grid_layout.addWidget(self.client_locality, 2, 1)
        self.client_info_grid_layout.addWidget(self.client_locality_edit, 2, 2)
        self.client_info_grid_layout.addWidget(self.client_city, 2, 3)
        self.client_info_grid_layout.addWidget(self.client_city_edit, 2, 4)
        self.client_info_grid_layout.addWidget(self.client_phone, 3, 1)
        self.client_info_grid_layout.addWidget(self.client_phone_edit, 3, 2)
        self.client_info_grid_layout.addWidget(self.client_mail, 3, 3)
        self.client_info_grid_layout.addWidget(self.client_mail_edit, 3, 4)

        self.client_info_vertical_layout.addWidget(self.client_information)
        self.client_info_vertical_layout.addLayout(self.client_info_grid_layout)

        self.quotation_e_vertical_layout = QVBoxLayout(self.frame_down)

        self.quotation_e_grid_layout = QGridLayout()
        self.quotation_e_grid_layout.addWidget(self.amount_of_inks_label, 1, 1)
        self.quotation_e_grid_layout.addWidget(self.amount_of_inks_select, 1, 2)
        self.quotation_e_grid_layout.addWidget(self.width_of_each_label, 1, 3)
        self.quotation_e_grid_layout.addWidget(self.width_of_each_label_edit, 1, 4)

        self.quotation_e_grid_layout.addWidget(self.length_of_each_label, 2, 3)
        self.quotation_e_grid_layout.addWidget(self.length_of_each_label_edit, 2, 4)
        self.quotation_e_grid_layout.addWidget(self.kind_of_print_label, 2, 1)
        self.quotation_e_grid_layout.addWidget(self.kind_of_print_select, 2, 2)
        self.quotation_e_grid_layout.addWidget(self.space_between_labels, 3, 3)
        self.quotation_e_grid_layout.addWidget(self.space_between_labels_edit, 3, 4)

        self.quotation_e_grid_layout.addWidget(self.millimetersLabel, 1, 5)
        self.quotation_e_grid_layout.addWidget(self.millimetersLabel2, 2, 5)
        self.quotation_e_grid_layout.addWidget(self.millimetersLabel3, 3, 5)
        self.quotation_e_grid_layout.addWidget(self.utility_label, 3, 1)
        self.quotation_e_grid_layout.addWidget(self.utility_select, 3, 2)

        self.LabelsAmountLayout.addLayout(self.grid_layout_for_large_option_boxes)
        self.LabelsAmountLayout.addWidget(self.amount_of_labels)
        self.LabelsAmountLayout.addWidget(self.amount_of_labels_edit)

        self.quotation_e_vertical_layout.addWidget(self.quotation_elements)
        self.quotation_e_vertical_layout.addLayout(self.quotation_e_grid_layout)
        self.quotation_e_vertical_layout.addLayout(self.LabelsAmountLayout)

        self.main_layout.addWidget(self.impressions_label)
        self.main_layout.addWidget(self.autor_label)
        self.main_layout.addWidget(self.quotation_label)
        self.main_layout.addWidget(self.frame_up)
        self.main_layout.addWidget(self.frame_down)
        self.main_layout.addLayout(self.button_layout)

        self.setWindowTitle("Impressions 'The Software Taste' by Joaquín Jiménez")

        title_font = QFont("Arial", 18, QFont.Normal)
        small_font = QFont("Arial", 8, QFont.Light)
        big_font = QFont("Arial", 16, QFont.Normal)
        medium_font = QFont("Arial", 12, QFont.Normal)

        self.impressions_label.setFont(title_font)
        self.quotation_label.setFont(big_font)
        self.quotation_elements.setFont(medium_font)
        self.client_information.setFont(medium_font)
        self.finish_quotation_button.setFont(big_font)
        self.autor_label.setFont(small_font)

        self.impressions_label.setAlignment(Qt.AlignCenter)
        self.quotation_label.setAlignment(Qt.AlignCenter)
        self.client_information.setAlignment(Qt.AlignLeft)
        self.quotation_elements.setAlignment(Qt.AlignLeft)
        self.autor_label.setAlignment(Qt.AlignCenter)
        self.width_of_each_label.setAlignment(Qt.AlignRight)
        self.length_of_each_label.setAlignment(Qt.AlignRight)
        self.space_between_labels.setAlignment(Qt.AlignRight)

        self.show()

    def check_finish_button(self):

        flag = True

        for x in self.findChildren(QLineEdit):
            if x.text() == "":
                flag = False

        for x in self.findChildren(QComboBox):
            if x.currentText() == "Select":
                flag = False

        if flag is True:
            self.finish_quotation_button.setEnabled(True)
        else:
            self.finish_quotation_button.setEnabled(False)

    def create_dialog(self):
        self.finish_dialog = FinishDialog(self)
        self.finish_dialog.accept_button.clicked.connect(self.print_the_quotation)
        self.finish_dialog.cancel_button.clicked.connect(self.finish_dialog_rejected)

    def print_the_quotation(self):
        paper = str(self.kind_of_paper_select.currentText().split(",")[0])
        printing_machine = str(self.printing_machine_select.currentText().split(",")[0])
        total_printing_time = list()
        total_cost_with_utilities = list()

        for i in self.database.session.query(self.database.kind_of_paper).filter(self.database.kind_of_paper.origin == paper).all():
            paper_cost_in_pesos_per_square_mm = float(i.cost_in_pesos_per_square_meter) / (1000 * 1000)

        for i in self.database.session.query(self.database.printing_machine).filter(self.database.printing_machine.branch == printing_machine).all():
            preparation_time_in_minutes = float(i.preparation_time_in_hours) * 60
            roll_length_in_mm = float(i.roll_length_in_inches) * 25.4
            printing_speed_in_mm_per_minute = float(i.printing_speed_in_inches_per_minute) * 25.4

        label_width = float(self.width_of_each_label_edit.text())
        label_length = float(self.length_of_each_label_edit.text())
        label_area_in_square_mm = label_width * label_length
        amount_of_labels = [int(s) for s in self.amount_of_labels_edit.text().replace(" ", "").split(",") if s.isdigit()]
        operator_hour_cost = 45000
        shortest_label_side, longest_label_side = (label_width, label_length) if label_width < label_length else (label_length, label_width)
        utility = int(self.utility_select.currentText())

        separation_between_labels = float(self.space_between_labels_edit.text())
        labels_across_the_paper_width, total_waste_of_paper_in_square_mm, total_paper_used_in_square_mm, total_length_paper_to_print = self.optimization_and_paper_managing(shortest_label_side, longest_label_side, separation_between_labels, roll_length_in_mm, amount_of_labels)
        for i in range(len(total_length_paper_to_print)):
            total_printing_time.append(float(total_length_paper_to_print[i] / printing_speed_in_mm_per_minute))

        if self.kind_of_print_select.currentText() == "Digital":
            for i in range(len(amount_of_labels)):
                temp_total_cost = ((label_area_in_square_mm * amount_of_labels[i] * paper_cost_in_pesos_per_square_mm) + (total_printing_time[i] * operator_hour_cost))
                total_cost_with_utilities.append(temp_total_cost * (1 + (utility / 100)))
        else:
            for i in range(len(amount_of_labels)):
                temp_total_cost = ((total_paper_used_in_square_mm[i] * paper_cost_in_pesos_per_square_mm) + ((preparation_time_in_minutes * int(self.amount_of_inks_select.currentText())) * operator_hour_cost) + total_printing_time[i] * operator_hour_cost)
                total_cost_with_utilities.append(temp_total_cost * (1 + (utility / 100)))

        path = "txtfiles/"
        os.makedirs(path, exist_ok=True)
        txt_file = ("{}{}.txt".format(path, time.strftime("%Y%m%d   %H%M%S").replace(" ", "_")))

        with open(txt_file, "w+") as textedit_file:
            textedit_file.write("\t\t\tImpressions 'The Software Taste'\n")
            textedit_file.write("\t\t\t\tBy Joaquín Jiménez\n")
            textedit_file.write("\t\t\t\t\tQuotation\n\n\n")
            textedit_file.write("Client name: {}\n".format(self.client_name_edit.text()))
            textedit_file.write("Client locality: {}\n".format(self.client_locality_edit.text()))
            textedit_file.write("Client phone: {}\n".format(self.client_phone_edit.text()))
            textedit_file.write("Client adress: {}\n".format(self.client_adress_edit.text()))
            textedit_file.write("Client city: {}\n".format(self.client_city_edit.text()))
            textedit_file.write("Client mail: {}\n".format(self.client_mail_edit.text()))
            textedit_file.write("Label width: {}\n".format(label_width))
            textedit_file.write("Label length: {}\n".format(label_length))
            textedit_file.write("Label area: {}\n".format(label_area_in_square_mm))
            textedit_file.write("Amount of inks: {}\n".format(self.amount_of_inks_select.currentText()))
            textedit_file.write("\n\nFor this amount of labels \t this cost in pesos\n")

            for i in range(len(amount_of_labels)):
                textedit_file.write("\t{}\t\t\t       {}\n".format(amount_of_labels[i], int(total_cost_with_utilities[i])))
            os.popen("notepad {}".format(txt_file))

    def optimization_and_paper_managing(self, label_short_side, label_long_side, separation_between_labels, roll_length, amount_of_labels):
        number_of_labels_that_fit_per_row = 0
        temp = 0
        used_paper_width = 0
        total_waste_of_paper_in_square_mm = list()
        total_paper_used_in_square_mm = list()
        total_length_paper_to_print = list()
        paper_width = roll_length

        while(paper_width >= used_paper_width):
            number_of_labels_that_fit_per_row = temp
            temp = number_of_labels_that_fit_per_row + 1
            used_paper_width = (temp * label_short_side) + ((temp + 1) * separation_between_labels)

        for i in amount_of_labels:
            paper_columns = int(i / number_of_labels_that_fit_per_row)
            paper_columns_rest = i % number_of_labels_that_fit_per_row
            total_waste_of_paper_in_square_mm_with_out_rest = ((paper_width - (number_of_labels_that_fit_per_row * label_short_side)) * label_long_side * paper_columns) + ((paper_columns + 1) * (paper_width * separation_between_labels))
            total_waste_of_paper_in_square_mm_rest = ((paper_columns_rest + 1) * (label_long_side + separation_between_labels) * separation_between_labels) + (paper_columns_rest * label_short_side * separation_between_labels)
            temp_total_waste_of_paper_in_square_mm = total_waste_of_paper_in_square_mm_with_out_rest + total_waste_of_paper_in_square_mm_rest
            total_waste_of_paper_in_square_mm.append(temp_total_waste_of_paper_in_square_mm)
            temp_total_paper_used_in_square_mm = temp_total_waste_of_paper_in_square_mm + (label_long_side * label_short_side * i)
            total_paper_used_in_square_mm.append(temp_total_paper_used_in_square_mm)
            total_length_paper_to_print.append(float(temp_total_paper_used_in_square_mm / paper_width))

        return number_of_labels_that_fit_per_row, total_waste_of_paper_in_square_mm, total_paper_used_in_square_mm, total_length_paper_to_print

    def finish_dialog_rejected(self):
        print("voliendo a la interfaz")


def main():
    app = QApplication(sys.argv)
    _window = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

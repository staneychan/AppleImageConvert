# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGroupBox, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QSlider, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(712, 532)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.group_box_path = QGroupBox(Dialog)
        self.group_box_path.setObjectName(u"group_box_path")
        self.group_box_path.setGeometry(QRect(10, 10, 691, 171))
        self.edt_source_path = QLineEdit(self.group_box_path)
        self.edt_source_path.setObjectName(u"edt_source_path")
        self.edt_source_path.setGeometry(QRect(110, 20, 571, 31))
        self.txt_source = QLabel(self.group_box_path)
        self.txt_source.setObjectName(u"txt_source")
        self.txt_source.setGeometry(QRect(12, 19, 91, 31))
        self.txt_source.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.btn_select_file = QPushButton(self.group_box_path)
        self.btn_select_file.setObjectName(u"btn_select_file")
        self.btn_select_file.setGeometry(QRect(110, 60, 111, 31))
        self.btn_select_folder = QPushButton(self.group_box_path)
        self.btn_select_folder.setObjectName(u"btn_select_folder")
        self.btn_select_folder.setGeometry(QRect(230, 60, 111, 31))
        self.txt_dest = QLabel(self.group_box_path)
        self.txt_dest.setObjectName(u"txt_dest")
        self.txt_dest.setGeometry(QRect(10, 124, 91, 31))
        self.txt_dest.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.txt_dest.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.edt_save_path = QLineEdit(self.group_box_path)
        self.edt_save_path.setObjectName(u"edt_save_path")
        self.edt_save_path.setGeometry(QRect(110, 124, 491, 31))
        self.btn_save_browse = QPushButton(self.group_box_path)
        self.btn_save_browse.setObjectName(u"btn_save_browse")
        self.btn_save_browse.setGeometry(QRect(610, 124, 71, 31))
        self.line = QFrame(self.group_box_path)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(10, 97, 671, 20))
        self.line.setStyleSheet(u"color: rgb(220, 220, 220);\n"
"")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.chk_recursive_sub_dir = QCheckBox(self.group_box_path)
        self.chk_recursive_sub_dir.setObjectName(u"chk_recursive_sub_dir")
        self.chk_recursive_sub_dir.setGeometry(QRect(360, 66, 111, 19))
        self.chk_include_livp = QCheckBox(self.group_box_path)
        self.chk_include_livp.setObjectName(u"chk_include_livp")
        self.chk_include_livp.setGeometry(QRect(492, 66, 80, 19))
        self.chk_include_heic = QCheckBox(self.group_box_path)
        self.chk_include_heic.setObjectName(u"chk_include_heic")
        self.chk_include_heic.setGeometry(QRect(590, 66, 80, 19))
        self.group_box_log = QGroupBox(Dialog)
        self.group_box_log.setObjectName(u"group_box_log")
        self.group_box_log.setGeometry(QRect(10, 330, 691, 191))
        self.edt_log = QPlainTextEdit(self.group_box_log)
        self.edt_log.setObjectName(u"edt_log")
        self.edt_log.setGeometry(QRect(10, 20, 671, 161))
        self.edt_log.setStyleSheet(u"background-color: rgb(199, 237, 204);")
        self.edt_log.setReadOnly(True)
        self.btn_start_converter = QPushButton(Dialog)
        self.btn_start_converter.setObjectName(u"btn_start_converter")
        self.btn_start_converter.setGeometry(QRect(290, 288, 111, 41))
        self.group_box_convert_param = QGroupBox(Dialog)
        self.group_box_convert_param.setObjectName(u"group_box_convert_param")
        self.group_box_convert_param.setGeometry(QRect(10, 190, 691, 91))
        self.chk_overwrite_same_jpg = QCheckBox(self.group_box_convert_param)
        self.chk_overwrite_same_jpg.setObjectName(u"chk_overwrite_same_jpg")
        self.chk_overwrite_same_jpg.setGeometry(QRect(10, 20, 231, 19))
        self.txt_img_quality_tip = QLabel(self.group_box_convert_param)
        self.txt_img_quality_tip.setObjectName(u"txt_img_quality_tip")
        self.txt_img_quality_tip.setGeometry(QRect(10, 53, 151, 16))
        self.sld_image_quality = QSlider(self.group_box_convert_param)
        self.sld_image_quality.setObjectName(u"sld_image_quality")
        self.sld_image_quality.setGeometry(QRect(170, 52, 461, 22))
        self.sld_image_quality.setMinimum(1)
        self.sld_image_quality.setMaximum(100)
        self.sld_image_quality.setSliderPosition(100)
        self.sld_image_quality.setOrientation(Qt.Orientation.Horizontal)
        self.txt_img_quality = QLabel(self.group_box_convert_param)
        self.txt_img_quality.setObjectName(u"txt_img_quality")
        self.txt_img_quality.setGeometry(QRect(640, 54, 31, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.group_box_path.setTitle(QCoreApplication.translate("Dialog", u"\u6587\u4ef6\u8def\u5f84", None))
        self.txt_source.setText(QCoreApplication.translate("Dialog", u"\u6e90\u6587\u4ef6/\u6587\u4ef6\u5939\uff1a", None))
        self.btn_select_file.setText(QCoreApplication.translate("Dialog", u"\u9009\u62e9\u5355\u4e2a\u6587\u4ef6", None))
        self.btn_select_folder.setText(QCoreApplication.translate("Dialog", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.txt_dest.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58\u5230\uff1a", None))
        self.btn_save_browse.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8", None))
        self.chk_recursive_sub_dir.setText(QCoreApplication.translate("Dialog", u"\u5305\u62ec\u6240\u6709\u5b50\u76ee\u5f55", None))
        self.chk_include_livp.setText(QCoreApplication.translate("Dialog", u"\u5305\u62eclivp", None))
        self.chk_include_heic.setText(QCoreApplication.translate("Dialog", u"\u5305\u62echeic", None))
        self.group_box_log.setTitle(QCoreApplication.translate("Dialog", u"\u8f6c\u6362\u65e5\u5fd7", None))
        self.btn_start_converter.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u8f6c\u6362", None))
        self.group_box_convert_param.setTitle(QCoreApplication.translate("Dialog", u"\u8f6c\u6362\u53c2\u6570\u914d\u7f6e", None))
        self.chk_overwrite_same_jpg.setText(QCoreApplication.translate("Dialog", u"\u8986\u76d6\u540c\u540djpeg\u56fe\u7247", None))
        self.txt_img_quality_tip.setText(QCoreApplication.translate("Dialog", u"\u8f6c\u6362\u7684\u56fe\u7247\u8d28\u91cf\uff081-100\uff09\uff1a", None))
        self.txt_img_quality.setText(QCoreApplication.translate("Dialog", u"100", None))
    # retranslateUi


from PySide6.QtCore import QThread, Signal
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QDialog, QFileDialog


from app import Ui_Dialog
from converter import *
from app_language import update_language



class ConverterDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.thread = None
        self.is_include_heic = True
        self.is_include_livp = True
        self.image_quality = 0
        self.overwrite_image = True

        # 设置界面为designer生成的界面
        self.ui = Ui_Dialog()
        self.ui.setupUi(self) # 导入界面
        self.setFixedSize(self.size()) # 固定大小
        self.setWindowTitle("Iphone Image Tool (heic,livp -> jpeg)")
        # 默认同时可转换heic,livp
        self.ui.chk_include_heic.setChecked(self.is_include_heic)
        self.ui.chk_include_livp.setChecked(self.is_include_livp)
        self.ui.chk_recursive_sub_dir.setVisible(False) # 默认扫描所有子目录
        self.ui.chk_overwrite_same_jpg.setChecked(self.overwrite_image)
        self.ui.chk_include_heic.clicked.connect(self.on_check_changed)
        self.ui.chk_include_livp.clicked.connect(self.on_check_changed)
        self.ui.chk_overwrite_same_jpg.clicked.connect(self.on_check_changed)

        self.ui.sld_image_quality.valueChanged.connect(self.on_slider_value_changed)
        self.image_quality = self.ui.sld_image_quality.value()

        self.ui.btn_select_file.clicked.connect(self.on_click_select_file)
        self.ui.btn_select_folder.clicked.connect(self.on_click_select_folder)
        self.ui.btn_save_browse.clicked.connect(self.on_click_select_save_folder)
        self.ui.btn_start_converter.clicked.connect(self.on_click_start_converter)
        # 根据当前系统语言更新界面文本
        update_language(self.ui)


    def on_check_changed(self, checked):
        self.is_include_heic = self.ui.chk_include_heic.isChecked()
        self.is_include_livp = self.ui.chk_include_livp.isChecked()
        self.overwrite_image = self.ui.chk_overwrite_same_jpg.isChecked()

    def on_slider_value_changed(self, value):
        """
         调整转换的图片质量(1-100)
         """
        self.image_quality = value
        self.ui.txt_img_quality.setText(str(value))

    def on_click_select_file(self):
        """
         选择单个图片文件用于转换
         """
        # 两种文件都不勾选时提示错误
        if not self.is_include_heic and not self.is_include_livp:
            self.ui.edt_log.appendPlainText("必需选择<包括heic>或<包括livp>文件选项!!")
            return

        img_filter = "*.livp *.heic"
        if self.is_include_heic and not self.is_include_livp:
            img_filter = "*.heic"
        elif not self.is_include_heic and self.is_include_livp:
            img_filter = "*.livp"

        file_name, selected_filter = QFileDialog.getOpenFileName(
            self,
            "选择图片",  # 对话框标题
            "",  # 初始目录 (空字符串表示使用默认或上次目录)
            f"图片文件 ({img_filter})",  # 过滤器
            ""  # 默认选中的过滤器 (空字符串表示使用第一个)
        )
        # 当用户点击了"取消"或关闭了对话框时，file_name == ''
        if file_name:
            self.ui.edt_source_path.setText(file_name)
            self.ui.edt_log.appendPlainText(f"选择的文件: {file_name}")
            # 生成保存路径
            save_filename = os.path.splitext(file_name)[0] + ".jpeg"
            self.ui.edt_save_path.setText(save_filename)

    def on_click_select_folder(self):
        """
        选择整个文件夹，里面所有图片用于转换
        """
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择要转换的图片文件夹",
            ""  # 初始目录
        )
        # 当用户点击了"取消"或关闭了对话框时，directory == ''
        if directory:
            self.ui.edt_source_path.setText(directory)
            self.ui.edt_log.appendPlainText(f"选择转换的文件夹: {directory}")
            # 生成保存路径
            save_filename = directory + "_jpeg"
            self.ui.edt_save_path.setText(save_filename)

    def on_click_select_save_folder(self):
        """
        选择用于保存转换后的jpeg图片文件夹
        """
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择保存图片的文件夹",
            ""  # 初始目录
        )
        if directory:
            self.ui.edt_save_path.setText(directory)
            self.ui.edt_log.appendPlainText(f"选择保存的文件夹: {directory}")

    def on_click_start_converter(self):
        source_path = self.ui.edt_source_path.text()
        dest_path = self.ui.edt_save_path.text()

        if not os.path.exists(source_path):
            QMessageBox.information(self, "错误", "<源文件/文件夹> 路径不存在！")
            return
        if len(dest_path) == 0:
            QMessageBox.information(self, "错误", "请指定 <保存到> 的路径！")
            return

        result = False
        if os.path.isdir(source_path): # 转换文件夹所有图片
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            file_list = []
            if self.is_include_heic:
                file_list.extend(scan_files(source_path, suffix=".heic"))
            if self.is_include_livp:
                file_list.extend(scan_files(source_path, suffix=".livp"))

            self.thread = ConvertThread(dest_path, file_list, self.overwrite_image, self.image_quality)
            self.thread.task_signal.connect(self.on_update_task)
            self.thread.start()

            # for file in file_list:
            #     print(f"convert:{file}")
            #     save_file = dest_path + os.sep + os.path.splitext(os.path.basename(file))[0] + ".jpeg"
            #     if os.path.splitext(file)[-1].lower() == '.heic':
            #         result = convert_heic_file(file, save_file, self.overwrite_image, False, self.image_quality)
            #     elif os.path.splitext(file)[-1].lower() == '.livp':
            #         result = convert_livp_to_jpeg(file, save_file, self.overwrite_image, 100)
            #     self.ui.edt_log.appendPlainText("转换成功:"+save_file if result else "转换失败!")

        elif os.path.isfile(source_path): # 转换单个图片
            if os.path.splitext(source_path)[-1].lower() == '.heic':
                result = convert_heic_file(source_path, dest_path, self.overwrite_image, False, self.image_quality)
            elif os.path.splitext(source_path)[-1].lower() == '.livp':
                result = convert_livp_to_jpeg(source_path, dest_path, self.overwrite_image, 100)
            self.ui.edt_log.appendPlainText("转换成功:"+dest_path if result else "转换失败!")

    def on_update_task(self, msg: str):
        self.ui.edt_log.appendPlainText(msg)


class ConvertThread(QThread):
    task_signal = Signal(str) # 通知任务状态变化信号

    def __init__(self, save_path: str, file_list: list[str], overwrite_image: bool, image_quality: int):
        super().__init__()
        print('ConvertThread init')
        self.save_path = save_path
        self.file_list = file_list
        self.overwrite_image = overwrite_image
        self.image_quality = image_quality

    def run(self):
        result = False
        for file in self.file_list:
            print(f"convert:{file}")
            save_file = self.save_path + os.sep + os.path.splitext(os.path.basename(file))[0] + ".jpeg"
            if os.path.splitext(file)[-1].lower() == '.heic':
                result = convert_heic_file(file, save_file, self.overwrite_image, False, self.image_quality)
            elif os.path.splitext(file)[-1].lower() == '.livp':
                result = convert_livp_to_jpeg(file, save_file, self.overwrite_image, 100)
            self.task_signal.emit("转换成功:" + save_file if result else "转换失败!")
        self.task_signal.emit("全部完成")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = ConverterDialog()
    dialog.show()

    sys.exit(app.exec())
import locale
from PySide6.QtCore import QLocale
from app import Ui_Dialog


def set_ui_text(ui: Ui_Dialog, text_list: list[str]):
    ui.group_box_path.setTitle(text_list[0])
    ui.txt_source.setText(text_list[1])
    ui.btn_select_file.setText(text_list[2])
    ui.btn_select_folder.setText(text_list[3])
    ui.chk_recursive_sub_dir.setText(text_list[4])
    ui.chk_include_livp.setText(text_list[5])
    ui.chk_include_heic.setText(text_list[6])
    ui.txt_dest.setText(text_list[7])
    ui.btn_save_browse.setText(text_list[8])

    ui.group_box_convert_param.setTitle(text_list[9])
    ui.chk_overwrite_same_jpg.setText(text_list[10])
    ui.txt_img_quality_tip.setText(text_list[11])
    ui.btn_start_converter.setText(text_list[12])
    ui.group_box_log.setTitle(text_list[13])

def update_language(ui: Ui_Dialog):
    # 输出:('Chinese (Simplified)_China', '936')
    # print(f"lang:{locale.getlocale()}")

    # 获取语言名称 (英文)
    system_locale = QLocale.system()
    language_name = system_locale.languageToString(system_locale.language())
    print(f"语言 (英文): {language_name}")  # 输出如 "Chinese", "English"

    text_list_cn = ['文件路径', '源文件/文件夹：', '选择单个文件', '选择文件夹', '包括所有子目录',
                 '包括livp', '包括heic', '保存到：', '浏览', '转换参数配置', '覆盖同名jpeg图片',
                 '转换的图片质量（1-100）：', '开始转换', '转换日志']
    text_list_eng = ['File Paths', 'Input：', 'Select File', 'Select Folder', 'Search subdirectories',
                 'livp', 'heic', 'Output：', 'Browse', 'Conversion Options', 'Overwrite existing JPEG files',
                 'Image Quality（1-100）：', 'Convert', 'Conversion Log']

    set_ui_text(ui, text_list_cn if language_name == 'Chinese' else text_list_eng)


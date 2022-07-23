from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QMainWindow
from ui import Ui_Form
import os
import cv2


# 游览时会遇到五种情况：
# situation_1：游览到倒数第二张，只有四张图
# situation_2：游览到倒数第一张，只有三张图
# situation_3：游览到正数第一张，只有三张图
# situation_4：游览到正数第二张，只有四张图
# situation_normal：正常情况，五张图

# 五张图片的路径分别表示为：
# 主图的路径：self.path_pic_main
# 上一张图的路径：self.path_pic_previous1
# 上上一张图的路径：self.path_pic_previous2
# 下一张图的路径：self.path_pic_next1
# 下下一张图的路径：self.path_pic_next2


class Select(QMainWindow):

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.path_pic_next1 = None
        self.ui = Ui_Form()
        # 初始化界面
        self.ui.setupUi(self)
        # 链接按钮与函数
        self.ui.button_52.clicked.connect(self.select_pic)
        self.ui.button_53.clicked.connect(self.next_pic)
        self.ui.button_51.clicked.connect(self.previous_pic)
        # 用于检查是否选择了文件的变量，防止未选择文件就点击“下一张或“上一张”而崩溃
        self.variable_of_chick = 0

    def select_pic(self):
        # “选择文件”函数
        self.variable_of_chick = 1  # 已经选择文件，置1
        self.path_pic_main = QFileDialog.getOpenFileName(self, "选择图片", ".", "Images (*.jpg)")[0]  # 选择jpg图片
        if self.path_pic_main:  # 判断路径是否为空，防止因中途取消而崩溃
            position_of_key = self.path_pic_main.rfind("/")  # 从后往前寻找关键字'/'的位置
            self.path_of_pic_folder = self.path_pic_main[0:position_of_key]  # 截取图片所在文件夹的路径
            self.name_of_main_pic = self.path_pic_main[position_of_key + 1:len(self.path_pic_main)]  # 截取图片名
            self.names_all_pics = os.listdir(self.path_of_pic_folder)  # 获取图片所在文件夹中所有文件的文件名
            self.index_main = self.names_all_pics.index(self.name_of_main_pic)  # 获取主图的索引
            if self.index_main == len(self.names_all_pics) - 2:  # 选择的图片是倒数第二张
                self.situation_1()
            elif self.index_main == len(self.names_all_pics) - 1:  # 选择的图片是倒数第一张
                self.situation_2()
            elif self.index_main == 0:  # 选择的图片是正数第一张
                self.situation_3()
            elif self.index_main == 1:  # 选择的图片是正数第二张
                self.situation_4()
            else:
                self.situation_normal()  # 正常情况

        return None

    def next_pic(self):
        # “下一张”函数
        if self.variable_of_chick == 1:  # 检查是否选择过文件
            print("next")
            self.ui.button_51.setEnabled(True)  # 激活“上一张”的按钮，用于在其在正数第一张时被禁用后的激活
            self.index_main = self.index_main + 1  # 将主图的索引加一
            self.path_pic_main = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main]  # 合成主图路径
            if self.index_main == len(self.names_all_pics) - 2:  # 下一张的图片是倒数第二张
                self.situation_1()
            elif self.index_main == len(self.names_all_pics) - 1:  # 下一张的图片是倒数第一张
                self.situation_2()
                QMessageBox.about(self, '警告', '这已经是最后一张照片了！')
            elif self.index_main == 1:  # 下一张的图片是正数第二张
                self.situation_4()
            else:  # 正常情况
                self.situation_normal()
        else:
            QMessageBox.about(self, '警告', '未指定图片')
            return None

    def previous_pic(self):
        if self.variable_of_chick == 1:  # 检查是否选择过文件
            print("previous")
            self.ui.button_53.setEnabled(True)  # 激活“下一张”的按钮，用于在其在倒数第一张时被禁用后的激活
            self.index_main = self.index_main - 1  # 将主图的索引减一
            self.path_pic_main = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main]  # 合成主图路径
            if self.index_main == len(self.names_all_pics) - 2:  # 下一张的图片是倒数第二张
                self.situation_1()
            elif self.index_main == 1:  # 下一张的图片是正数第二张
                self.situation_4()
            elif self.index_main == 0:  # 下一张的图片是正数第一张
                self.situation_3()
                QMessageBox.about(self, '警告', '这已经是第一张照片了！')
            else:  # 正常情况
                self.situation_normal()
        else:
            QMessageBox.about(self, '警告', '未指定图片')
            return None

    def situation_1(self):
        # 这种情况只需要四张图片的路径，主图路径在主函数合成，其他三张图的路径在本函数进行合成
        self.path_pic_previous2 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 2]
        self.path_pic_previous1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 1]
        self.path_pic_next1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main + 1]
        self.pic_previous2 = self.fill(self.path_pic_previous2, self.ui.label_51.width() / self.ui.label_51.height())
        self.ui.label_51.setPixmap(QPixmap(self.pic_previous2))
        self.ui.label_56.setText(self.names_all_pics[self.index_main - 2])

        self.pic_previous1 = self.fill(self.path_pic_previous1, self.ui.label_52.width() / self.ui.label_52.height())
        self.ui.label_52.setPixmap(QPixmap(self.pic_previous1))
        self.ui.label_57.setText(self.names_all_pics[self.index_main - 1])

        self.pic_main = self.fill(self.path_pic_main, self.ui.label_53.width() / self.ui.label_53.height())
        self.ui.label_53.setPixmap(QPixmap.fromImage(self.pic_main))
        self.ui.label_58.setText(self.names_all_pics[self.index_main])

        self.pic_next1 = self.fill(self.path_pic_next1, self.ui.label_54.width() / self.ui.label_54.height())
        self.ui.label_54.setPixmap(QPixmap(self.pic_next1))
        self.ui.label_59.setText(self.names_all_pics[self.index_main + 1])
        self.ui.label_55.setPixmap(QPixmap(""))  # 给lab传入空图片
        self.ui.label_60.setText("")  # 给lab传入空字符
        # 以下函数同理

    def situation_2(self):
        self.path_pic_previous2 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 2]
        self.path_pic_previous1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 1]
        self.pic_previous2 = self.fill(self.path_pic_previous2, self.ui.label_51.width() / self.ui.label_51.height())
        self.ui.label_51.setPixmap(QPixmap(self.pic_previous2))
        self.ui.label_56.setText(self.names_all_pics[self.index_main - 2])
        self.pic_previous1 = self.fill(self.path_pic_previous1, self.ui.label_52.width() / self.ui.label_52.height())
        self.ui.label_52.setPixmap(QPixmap(self.pic_previous1))
        self.ui.label_57.setText(self.names_all_pics[self.index_main - 1])
        self.pic_main = self.fill(self.path_pic_main, self.ui.label_53.width() / self.ui.label_53.height())
        self.ui.label_53.setPixmap(QPixmap.fromImage(self.pic_main))
        self.ui.label_58.setText(self.names_all_pics[self.index_main])
        self.ui.label_54.setPixmap(QPixmap(""))
        self.ui.label_59.setText("")
        self.ui.label_55.setPixmap(QPixmap(""))
        self.ui.label_60.setText("")
        self.ui.button_53.setDisabled(True)  # 游览到最后一张时时禁用下一张按钮

    def situation_3(self):
        self.path_pic_next1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main + 1]
        self.path_pic_next2 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main + 2]
        self.ui.label_51.setPixmap(QPixmap(""))
        self.ui.label_56.setText("")
        self.ui.label_52.setPixmap(QPixmap(""))
        self.ui.label_57.setText("")
        self.pic_main = self.fill(self.path_pic_main, self.ui.label_53.width() / self.ui.label_53.height())
        self.ui.label_53.setPixmap(QPixmap.fromImage(self.pic_main))
        self.ui.label_58.setText(self.names_all_pics[self.index_main])
        self.pic_next1 = self.fill(self.path_pic_next1, self.ui.label_54.width() / self.ui.label_54.height())
        self.ui.label_54.setPixmap(QPixmap(self.pic_next1))
        self.ui.label_59.setText(self.names_all_pics[self.index_main + 1])
        self.pic_next2 = self.fill(self.path_pic_next2, self.ui.label_55.width() / self.ui.label_55.height())
        self.ui.label_55.setPixmap(QPixmap(self.pic_next2))
        self.ui.label_60.setText(self.names_all_pics[self.index_main + 2])
        self.ui.button_51.setDisabled(True)  # 游览到第一张时时禁用上一张按钮

    def situation_4(self):
        self.path_pic_previous1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 1]
        self.path_pic_next1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main + 1]
        self.path_pic_next2 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main + 2]
        self.ui.label_51.setPixmap(QPixmap(""))
        self.ui.label_56.setText("")

        self.pic_previous1 = self.fill(self.path_pic_previous1, self.ui.label_52.width() / self.ui.label_52.height())
        self.ui.label_52.setPixmap(QPixmap(self.pic_previous1))
        self.ui.label_57.setText(self.names_all_pics[self.index_main - 1])

        self.pic_main = self.fill(self.path_pic_main, self.ui.label_53.width() / self.ui.label_53.height())
        self.ui.label_53.setPixmap(QPixmap.fromImage(self.pic_main))
        self.ui.label_58.setText(self.names_all_pics[self.index_main])

        self.pic_next1 = self.fill(self.path_pic_next1, self.ui.label_54.width() / self.ui.label_54.height())
        self.ui.label_54.setPixmap(QPixmap(self.pic_next1))
        self.ui.label_59.setText(self.names_all_pics[self.index_main + 1])

        self.pic_next2 = self.fill(self.path_pic_next2, self.ui.label_55.width() / self.ui.label_55.height())
        self.ui.label_55.setPixmap(QPixmap(self.pic_next2))
        self.ui.label_60.setText(self.names_all_pics[self.index_main + 2])

    def situation_normal(self):
        self.path_pic_previous2 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 2]
        self.path_pic_previous1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 1]
        self.path_pic_next1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main + 1]
        self.path_pic_next2 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main + 2]
        # 填充label53的边缘

        self.pic_previous2 = self.fill(self.path_pic_previous2, self.ui.label_51.width() / self.ui.label_51.height())
        self.ui.label_51.setPixmap(QPixmap(self.pic_previous2))
        self.ui.label_56.setText(self.names_all_pics[self.index_main - 2])

        self.pic_previous1 = self.fill(self.path_pic_previous1, self.ui.label_52.width() / self.ui.label_52.height())
        self.ui.label_52.setPixmap(QPixmap(self.pic_previous1))
        self.ui.label_57.setText(self.names_all_pics[self.index_main - 1])

        self.pic_main = self.fill(self.path_pic_main, self.ui.label_53.width() / self.ui.label_53.height())
        self.ui.label_53.setPixmap(QPixmap.fromImage(self.pic_main))
        self.ui.label_58.setText(self.names_all_pics[self.index_main])

        self.pic_next1 = self.fill(self.path_pic_next1, self.ui.label_54.width() / self.ui.label_54.height())
        self.ui.label_54.setPixmap(QPixmap(self.pic_next1))
        self.ui.label_59.setText(self.names_all_pics[self.index_main + 1])

        self.pic_next2 = self.fill(self.path_pic_next2, self.ui.label_55.width() / self.ui.label_55.height())
        self.ui.label_55.setPixmap(QPixmap(self.pic_next2))
        self.ui.label_60.setText(self.names_all_pics[self.index_main + 2])

    def fill(self, path, ratio):
        # 边缘填充函数
        pic = cv2.imread(path)
        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        k1 = pic.shape[1] / pic.shape[0]  # 图片的长宽比
        k2 = ratio  # label的长宽比
        if k1 >= k2:
            # 假如图片的长宽比大于等于label的长宽比，填充宽度
            a = int(((pic.shape[0] * k1 / k2) - pic.shape[0]) / 2)  # 计算填充量并均分
            pic_mian = cv2.copyMakeBorder(pic, a, a, 0, 0, cv2.BORDER_CONSTANT, value=[240, 240, 240])  # 填充颜色rgb[240, 240, 240]
            image_height, image_width, image_depth = pic_mian.shape
            saved_img_show = QImage(pic_mian.data, image_width, image_height, image_width * image_depth,
                                    QImage.Format_RGB888)
        else:
            # 假如图片的长宽比小于label的长宽比，填充长度
            b = int(((pic.shape[1] * k2 / k1) - pic.shape[1]) / 2)  # 计算填充量并均分
            pic_mian = cv2.copyMakeBorder(pic, 0, 0, b, b, cv2.BORDER_CONSTANT, value=[240, 240, 240])
            image_height, image_width, image_depth = pic_mian.shape
            saved_img_show = QImage(pic_mian.data, image_width, image_height, image_width * image_depth,
                                    QImage.Format_RGB888)
        return saved_img_show


if __name__ == "__main__":
    app = QApplication([])
    select = Select()
    select.show()
    app.exec_()

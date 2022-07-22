# BrowsePicture_PyQt5

![效果预览](https://github.com/MikeMiller0401/BrowsePicture_PyQt5/blob/main/Windows.png)

---

# ENGLISH

## Synopsis
 - This project is a picture tourer interface written in Python and draws the GUI using PyQt5
 - This is my first time developing a GUI and I am not proficient enough in the use of Python and PyQt
 - This project only supports images in jpg format, using the Python version of 3.6.12
 
## Project Introduction
### 1.Function 
 The focus of this project is to implement the functionality of the three buttons:
 ```python
self.ui.button_52.clicked.connect(self.select_pic)

self.ui.button_53.clicked.connect(self.next_pic)

self.ui.button_51.clicked.connect(self.previous_pic)
```
These function correspond to different methods:
```python
def select_pic(self):
  ...
def next_pic(self):
  ...
def previous_pic(self):
  ...
```
### 2、Special circumstances
There are five situations that you will encounter when visiting:
 1. situation_1：Tour to the penultimate album, there are only four pictures
 2. situation_2：Tour to the penultimate one, there are only three pictures
 3. situation_3：The tour reaches the first positive number, and there are only three pictures
 4. situation_4：The tour reaches the second positive number, with only four pictures
 5. situation_normal：Normal situation, five pictures

There are minor differences in the process for these five situations, and the solution for the first case is as follows:

```python
def situation_1(self):
    # In this case, only the path of four pictures is required, the main graph path is synthesized in the main function, and the path of the other three graphs is synthesized in this function
    self.path_pic_previous2 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 2]
    self.path_pic_previous1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 1]
    self.path_pic_next1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main + 1]
    self.ui.label_51.setPixmap(QPixmap(self.path_pic_previous2))
    self.ui.label_56.setText(self.names_all_pics[self.index_main - 2])
    self.ui.label_52.setPixmap(QPixmap(self.path_pic_previous1))
    self.ui.label_57.setText(self.names_all_pics[self.index_main - 1])
    self.ui.label_53.setPixmap(QPixmap(self.path_pic_main))
    self.ui.label_58.setText(self.names_all_pics[self.index_main])
    self.ui.label_54.setPixmap(QPixmap(self.path_pic_next1))
    self.ui.label_59.setText(self.names_all_pics[self.index_main + 1])
    self.ui.label_55.setPixmap(QPixmap(""))
    self.ui.label_60.setText("")
```

### 3、Prevent the program from crashing

 1. Prevent the program from crashing by clicking on the "Previous" or "Next" button when the user has not selected an image
 2. Prevent the user from canceling halfway through the selection of the picture and causing the program to crash
 3. Prevent users from clicking on the "Previous" or "Next" buttons while visiting the first or last image and causing a crash

The corresponding solution is as follows:

 1. Add a variable to check if the select_pic function has been run:

```python
def __init__(self):
	# Variable used to check if a file is selected to prevent a crash by clicking "Next" or "Previous" without selecting a file
	self.variable_of_chick = 0
	...
def select_pic(self):
    # "Select File" function
    self.variable_of_chick = 1 # The file has been selected, set to 1
        ...
def next_pic(self):
    # "Next" function
    if self.variable_of_chick == 1:# Checks whether a file has been selected
       print("next")
       ...
```

 2. Check if the self.path_pic_main is empty:

```python
 def select_pic(self):
        # "Select File" function
        self.variable_of_chick = 1 # The file has been selected, set to 1
        self.path_pic_main = QFileDialog.getOpenFileName(self, "Select Image", ".","Images (*.jpg)")[0] # Select jpg image
        If self.path_pic_main:# Determines if the path is empty to prevent crashes due to cancellations in the middle
        	position_of_key = self.path_pic_main.rfind("/") # look for the position of the keyword '/' from the back to the front
```

 3. Disable the corresponding button at the beginning and end:

```python
def situation_2(self):
	...
    self.ui.button_53.setDisabled(True) # Disable the next button when touring to the last one
```


---

# CHINESE

## 提要

 - 本项目是一个使用Python编写的图片游览器界面，并使用到PyQt5来绘制GUI
 - 这是我第一次开发GUI，对Python和PyQt的使用还不够熟练，如果有疑问我会尽量解答
 - 本项目仅支持jpg格式的图片，使用的Python版本为3.6.1
 
## 项目简介
### 1、功能
 本项目的重点在于实现三个按钮的功能：

```python
self.ui.button_52.clicked.connect(self.select_pic)

self.ui.button_53.clicked.connect(self.next_pic)

self.ui.button_51.clicked.connect(self.previous_pic)
```
这些功能对应不同的方法
```python
def select_pic(self): #选择图片
  ...
def next_pic(self): #下一张图片
  ...
def previous_pic(self): #上一张图片
  ...
```
### 2、特殊情况
在游览时会遇到五种情况：
 1. situation_1：游览到倒数第二张，只有四张图
 2. situation_2：游览到倒数第一张，只有三张图
 3. situation_3：游览到正数第一张，只有三张图
 4. situation_4：游览到正数第二张，只有四张图
 5. situation_normal：正常情况，五张图

这五种情况所对应的流程存在细小的差别，第一种情况的解决方案如下：

```python
def situation_1(self):
    # 这种情况只需要四张图片的路径，主图路径在主函数合成，其他三张图的路径在本函数进行合成
    self.path_pic_previous2 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 2]
    self.path_pic_previous1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main - 1]
    self.path_pic_next1 = self.path_of_pic_folder + '/' + self.names_all_pics[self.index_main + 1]
    self.ui.label_51.setPixmap(QPixmap(self.path_pic_previous2))  # 给label传入图片
    self.ui.label_56.setText(self.names_all_pics[self.index_main - 2])  # 给label传入图片的文件名
    self.ui.label_52.setPixmap(QPixmap(self.path_pic_previous1))
    self.ui.label_57.setText(self.names_all_pics[self.index_main - 1])
    self.ui.label_53.setPixmap(QPixmap(self.path_pic_main))
    self.ui.label_58.setText(self.names_all_pics[self.index_main])
    self.ui.label_54.setPixmap(QPixmap(self.path_pic_next1))
    self.ui.label_59.setText(self.names_all_pics[self.index_main + 1])
    self.ui.label_55.setPixmap(QPixmap(""))  # 给lab传入空图片
    self.ui.label_60.setText("")  # 给lab传入空字符
```

### 3、防止崩溃

 1. 防止在用户未选择图片时点击“上一张”或“下一张”按钮导致程序崩溃
 2. 防止用户在选择图片时中途取消导致程序崩溃
 3. 防止用户在游览到第一张或者最后一张图片时仍然点击“上一张”或“下一张”按钮导致崩溃

对应的解决方案如下：

 1. 加入一个变量来检查是否select_pic函数是否运行过：

```python
def __init__(self):
	# 用于检查是否选择了文件的变量，防止未选择文件就点击“下一张或“上一张”而崩溃
	self.variable_of_chick = 0
	...
def select_pic(self):
    # “选择文件”函数
    self.variable_of_chick = 1  # 已经选择文件，置1
        ...
def next_pic(self):
    # “下一张”函数
    if self.variable_of_chick == 1:  # 检查是否选择过文件
       print("next")
       ...
```

 2. 检查self.path_pic_main是不是为空：

```python
 def select_pic(self):
        # “选择文件”函数
        self.variable_of_chick = 1  # 已经选择文件，置1
        self.path_pic_main = QFileDialog.getOpenFileName(self, "选择图片", ".", "Images (*.jpg)")[0]  # 选择jpg图片
        if self.path_pic_main:  # 判断路径是否为空，防止因中途取消而崩溃
        	position_of_key = self.path_pic_main.rfind("/")  # 从后往前寻找关键字'/'的位置
```

 3. 在头尾处禁用对应的按钮：

```python
def situation_2(self):
	...
    self.ui.button_53.setDisabled(True)  # 游览到最后一张时时禁用下一张按钮
```

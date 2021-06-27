from tkinter import filedialog
from tkinter import *
import cv2
from PIL import Image, ImageTk
import FER
import dlib

er1 = ''
detector = dlib.get_frontal_face_detector()  # 使用特征提取器get_frontal_face_detector
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # dlib的68点模型，使用作者训练好的特征预测器

class face_emotion():
	def __init__(self):

		self.window = Tk()
		self.window.title('人脸情绪识别')
		self.window.geometry("940x540+90+100")  # geometry(长*宽，+左边距（-右边距），+上边距（-下边距）），尺寸
		self.createFirstPage()
		mainloop()  # 无实效作痛

	def createFirstPage(self):
		self.page1 = Frame(self.window)
		self.page1.pack()
		Label(self.page1, text='人脸情绪识别系统', font=('华文行楷', 55),fg='violet').pack(side=TOP)
		image = Image.open("11.png") # 随便使用一张图片 不要太大
		photo = ImageTk.PhotoImage(image = image)
		self.data1 = Label(self.page1,image = photo)
		self.data1.image = photo
		self.data1.pack(side=LEFT,padx=5, pady=5)
		# relief控件属性凸起
		self.button11 = Button(self.page1, width=25, height=2, text=" 开始检测（开启摄像头） ", bg='Tomato', font=("Heiti SC",22),relief='raise',command = self.face_emotion_recognize)
		self.button11.pack(side=TOP, padx=40, pady =30)  # padx外部间隔
		self.button12 = Button(self.page1, width=25, height=2, text="开始检测（检测图片）", bg='LightSkyBlue', font=("Heiti SC",22), relief='raise', command = self.face_emotion_file)
		self.button12.pack(side=TOP, padx=40, pady =30)
		self.button13 = Button(self.page1, width=25, height=2, text="退出系统", bg='PaleGreen', font=("Heiti SC",22), relief='raise',command = self.quitMain)
		self.button13.pack(side=TOP, padx=40, pady =30)

	def face_emotion_recognize(self):
		self.camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # 开启摄像头
		self.camera.set(3, 480)
		self.page1.pack_forget()  # 去除上一个窗口
		self.page2 = Frame(self.window)
		self.page2.pack()
		Label(self.page2, text='人脸情绪识别系统', font=('华文行楷', 55),fg='violet').pack(side=TOP)
		self.data2 = Label(self.page2)
		self.data2.pack(padx=5, pady=5,side=LEFT)
		self.entry = Entry(self.page2, font=('Heiti SC', 32), width=15)  # 文本框
		self.entry.pack(side=TOP,pady=50)  # 文本框
		self.button21 = Button(self.page2, width=10, height=1, text="返回", bg='PaleGreen', font=("Heiti SC", 30), relief='raise', command=self.backFirst)
		self.button21.pack(side=TOP, padx=25, pady=120)
		self.video_loop(self.data2)


	def video_loop(self, panela):
		flag, im_rd = self.camera.read()  # 从摄像头读取照片
		if flag == True:
			im_rd = cv2.flip(im_rd, 180)  # 镜像
		line_brow_x = []
		line_brow_y = []
		if flag:
			# er 为识别的表情的字符串
			im_rd, er = FER.start(line_brow_x, line_brow_y, im_rd, detector, predictor)
			global er1
			if er1 != er:
				er1=er
				self.entry.delete(0, END)
				self.entry.insert(0, er1)  # 显示表情
			cv2image = cv2.cvtColor(im_rd, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
			current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象
			imgtk = ImageTk.PhotoImage(image=current_image)
			panela.imgtk = imgtk
			panela.config(image=imgtk)
			self.window.after(1, lambda: self.video_loop(panela))

	def face_emotion_file(self):
		self.page1.pack_forget()  # 去除上一个窗口
		self.page3 = Frame(self.window)
		self.page3.pack()
		Label(self.page3, text='人脸情绪识别系统', font=('华文行楷', 55), fg='violet').pack(side=TOP)
		self.page4 = Frame(self.window, width=450, height=450, relief=SUNKEN)
		self.page4.pack(side=LEFT,padx=1, pady=1)
		self.canvas = Canvas(self.page4,width=450, height=450)
		self.canvas.pack(side=LEFT,padx=1, pady=1)
		self.page5=Frame(self.window)
		self.page5.pack(side=RIGHT,fill='y',padx=1, pady=1)
		self.entry = Entry(self.page5, font=('Heiti SC', 32), width=15)  # 文本框
		self.entry.pack(pady=20)  # 文本框
		self.button31=Button(self.page5,width=20, height=2,text='选择本地图片', bg='LightSkyBlue',font=("Heiti SC", 22),relief='raise',
							 command=self.printcoords)
		self.button31.pack(side=TOP, padx=40, pady=45)
		self.button32 = Button(self.page5, width=20, height=2, text="返回", bg='PaleGreen', font=("Heiti SC", 22),
							  relief='raise', command=self.backFirst_file)
		self.button32.pack(side=TOP, padx=40, pady=60)



	def printcoords(self):
		global File
		line_brow_x = []
		line_brow_y = []
		self.File = filedialog.askopenfilename(parent=self.page3, initialdir="C:/", title='选择一张图片')
		#im_rd = Image.open(self.File)
		im_rd = cv2.imread(self.File)
		try:
			im_rd = cv2.resize(im_rd, dsize=(450,450))  # 缩放
			# er 为识别的表情的字符串
			im_rd,er = FER.start(line_brow_x, line_brow_y, im_rd, detector, predictor)
			global er2
			er2 = er
			im_rd = cv2.resize(im_rd, dsize=(450,450))
			current_image = Image.fromarray(im_rd)
			self.filename = ImageTk.PhotoImage(image=current_image)
			self.canvas.image = self.filename  # <--- keep reference of your image
			self.canvas.create_image(0, 0, anchor='nw', image=self.filename)
			self.entry.delete(0,END)
			self.entry.insert(0, er2)  # 显示表情
		except Exception as e:
			if 'Assertion failed' in str(e):
				er2 = '路径中有中文，请更改后使用'
				self.entry.insert(0, er2)  # 显示表情
			else:
				print(e)



	def backFirst(self):
		self.page2.pack_forget()
		self.page1.pack()
		# 释放摄像头资源
		self.camera.release()
		cv2.destroyAllWindows()

	def backFirst_file(self):
		self.page3.pack_forget()
		self.page4.pack_forget()
		self.page5.pack_forget()
		self.page1.pack()

	def quitMain(self):
		sys.exit(0)


if __name__ == '__main__':
	face = face_emotion()


	# 嘴巴下
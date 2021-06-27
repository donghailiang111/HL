import joblib
import cv2  # 图像处理的库OpenCv

def face_pd(im_rd,a,b,c,d,dd,e):

    cld = joblib.load("knn.m")#调用已经训练好的模型
    #  cld = joblib.load("新最后最后最后六围2knn.m")

    x = [[a, b, c, dd, e]]
    # 存储特征值
    # a-嘴巴宽度与识别框宽度之比
    # b-嘴巴高度与识别框高度之比
    # c-眉毛高度占比
    # dd-眉毛距离占比
    # e-眼睛睁开程度
    kll = int(cld.predict(x))#用训练好的KNN模型对获取的特征值进行分析分类，返回分类后的标签
    #根据标签判断当前表情，并在图像上输出
    emo=['angry','sadness','nature','nature','happy','nature','surprise']
    cv2.putText(im_rd, emo[kll-1], (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2, 4)

    return emo[kll-1]
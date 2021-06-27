import numpy as np              #数据处理的库numpy
import cv2                      #图像处理的库OpenCv
import face_pd
def start(line_brow_x,line_brow_y,im_rd,detector,predictor):                    #开始运行

    k = cv2.waitKey(1)
    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
    # 使用人脸检测器检测每一帧图像中的+人脸。并返回人脸数rects
    faces = detector(img_gray, 0)

    # 待会要显示在屏幕上的字体
    font = cv2.FONT_HERSHEY_SIMPLEX
    er = '未检测到人脸'
    # 如果检测到人脸
    if (len(faces) != 0):

        # 对每个人脸都标出68个特征点
        for i in range(len(faces)):
            # enumerate方法同时返回数据对象的索引和数据，k为索引，d为faces中的对象
            for k, d in enumerate(faces):
                # 用红色矩形框出人脸
                cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))
                # 计算人脸热别框边长
                face_width = d.right() - d.left()

                # 使用预测器得到68点数据的坐标
                shape = predictor(im_rd, d)
                # 圆圈显示每个特征点
                for i in range(68):
                    cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (0, 255, 0), -1, 8)
                    # cv2.putText(im_rd, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    #            (255, 255, 255))

                    # 分析任意n点的位置关系来作为表情识别的依据
                    mouth_width = (shape.part(54).x - shape.part(48).x) / face_width  # 嘴巴咧开程度

                    mouth_higth = (shape.part(67).y - shape.part(61).y + (shape.part(66).y - shape.part(62).y) + (
                                shape.part(65).y - shape.part(63).y)) / (3 * face_width)  # 嘴巴张开程度

                    a = round(mouth_width, 10)
                    b = round(mouth_higth, 10)
                    # 外圈
                    mouth_higth_w = (shape.part(58).y - shape.part(50).y + (shape.part(57).y - shape.part(51).y) + (
                                shape.part(56).y - shape.part(52).y)) / (3 * face_width)
                    mouth_xia_ = ((shape.part(57).y - shape.part(48).y) + (shape.part(57).y - shape.part(54).y)) / (
                            face_width * 2)
                    # 通过两个眉毛上的10个特征点，分析挑眉程度和皱眉程度
                    brow_sum = 0  # 高度之和
                    frown_sum = 0  # 两边眉毛距离之和
                    for j in range(17, 20):
                        brow_sum += (shape.part(j).y - d.top()) + (shape.part(j + 5).y - d.top())
                        frown_sum += shape.part(j + 5).x - shape.part(j).x
                        line_brow_x.append(shape.part(j).x)
                        line_brow_y.append(shape.part(j).y)

                    # self.brow_k, self.brow_d = self.fit_slr(line_brow_x, line_brow_y)  # 计算眉毛的倾斜程度
                    tempx = np.array(line_brow_x)
                    tempy = np.array(line_brow_y)
                    z1 = np.polyfit(tempx, tempy, 1)  # 拟合成一次直线
                    brow_k = -round(z1[0], 3)  # 拟合出曲线的斜率和实际眉毛的倾斜方向是相反的

                    brow_height = (brow_sum / 10) / face_width  # 眉毛高度占比
                    brow_width = (frown_sum / 5) / face_width  # 眉毛距离占比
                    c = round(brow_height, 10)
                    dd = round(brow_width, 310)
                    # 眼睛睁开程度
                    eye_sum = (shape.part(41).y - shape.part(37).y + shape.part(40).y - shape.part(38).y +
                               shape.part(47).y - shape.part(43).y + shape.part(46).y - shape.part(44).y)
                    eye_hight = (eye_sum / 4) / face_width
                    e = round(eye_hight, 10)
                    # 眼睛长度
                    eye_long = (shape.part(39).y - shape.part(36).y + shape.part(45).y - shape.part(42).y) / (
                            face_width * 2)


                    er = face_pd.face_pd(im_rd, a, b, c, faces[k], dd, e)


        # 标出人脸数
        cv2.putText(im_rd, "Faces: " + str(len(faces)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
    return im_rd, er
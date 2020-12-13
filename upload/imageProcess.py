from cv2 import cv2


imgFile = ''
img = cv2.imread('test02.jpg')


#二值化和灰度化处理
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray.jpg',gray)
ret, binary = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
cv2.imwrite('b.jpg',binary)
#开运算，先腐蚀再膨胀
binary = cv2.erode(binary, None, iterations=1)
cv2.imwrite('b2.jpg',binary)
binary = cv2.dilate(binary, None, iterations=1)
cv2.imwrite('b3.jpg',binary)

test, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.imwrite('book.jpg',test )
#print(contours)
i = 0
min_num = 10000
max_num = 270 * 400
for contour in contours[1:]:

    x, y, w, h = cv2.boundingRect(contour)
    if (w * h) > min_num:
        if (w * h) < max_num:
            #将全部轮廓画在图上
            out = cv2.rectangle(img,(x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.imwrite('first_result.jpg',out)
            i = i + 1
            source = img
            [height, width, pixels] = img.shape  # 提取原始图像数据
            savimg = source[0:height, x:(x + w)] #切割图像
            cv2.imwrite('book{0}.jpg'.format(i), savimg)
            num_book = i
            print('图片已存')
            
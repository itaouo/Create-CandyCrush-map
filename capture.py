import cv2 as cv
import numpy as np

# capture image

def rescaleImage(image, scale = 0.5): # scale
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(image, dimensions, interpolation = cv.INTER_AREA)

def captureImage(img_name):
    img = cv.imread(img_name)
    if img is None:
        print("fail to load image" + img_name)
        return None
    return img

def drawTarget(image, target_img, x, y):
    w = target_img.shape[1]
    h = target_img.shape[0]
    cv.rectangle(image, (x, y), (x + w, y + h),(0, 255, 255), 5)
    return image

def displayImage(image):
    cv.imshow("image", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def detectImage(target_img, reference_img, threshold = .80):
    result = cv.matchTemplate(target_img, reference_img, cv.TM_CCOEFF_NORMED)
    yloc, xloc = np.where(result >= threshold)
    return zip(xloc, yloc)

def checkLegalPosition(zip_position):
    new_yloc = []
    new_xloc = []
    for (x, y) in zip_position:
        is_repeat = 0
        is_out_of_bound = 1
        for(new_x,new_y) in zip(new_xloc, new_yloc):
            if(abs(x-new_x) <= 30 and abs(y-new_y) <= 30):
                is_repeat = 1
        if(568 < x < 1350 and 168 < y < 962):
            is_out_of_bound = 0
        if is_repeat == 0 and is_out_of_bound == 0:
            new_yloc.append(y)
            new_xloc.append(x)
    return zip(new_xloc, new_yloc)

def checkColor(zip_position, reference_img):
    new_yloc = []
    new_xloc = []
    lower_color = np.array([70, 50, 120])
    upper_color = np.array([140, 190, 255])
    hsv_image = cv.cvtColor(reference_img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_image, lower_color, upper_color)
    for (x, y) in zip_position:
        if mask[y+20, x+20] <= 0:
            new_yloc.append(y)
            new_xloc.append(x)
    return zip(new_xloc, new_yloc)

def writeData(path, data):
    with open(path + ".txt", "w", encoding="utf-8") as file:
        for row in data:
            line = " ".join(map(str, row))
            file.write(line + "\n")

def main():
    candy_list = [0,1,2,3,4,10,11,12,13,14,22,23,30,31,32,33,-11]
    for i in range(1,11):
        all_data = []
        all_img = captureImage("assets/map/" + str(i) + ".png")
        for j in candy_list:
            img = captureImage("assets/candy/" + str(j) + ".png")
            reference_img = captureImage("assets/map/" + str(i) + ".png")
            result_pos = detectImage(img, reference_img)
            result_pos = checkLegalPosition(result_pos)
            result_pos = checkColor(result_pos, reference_img)
            for (x, y) in result_pos:
                all_img = drawTarget(all_img, img, x, y)
                all_data.append([y, x, j])
        cv.imwrite("outputs/map_images/" + str(i) + ".png", all_img)
        writeData("outputs/data/" + str(i), all_data)
        # displayImage(rescaleImage(all_img))
        

main()
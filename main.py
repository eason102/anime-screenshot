from ast import Break
import os
import cv2
import numpy as np
import time
import glob
from pynput.keyboard import Key, Controller
from pynput.keyboard import Key, Listener
import tkinter as tk
from tkinter import filedialog
from functools import reduce
from PIL import Image
#監控鍵盤動作離開迴圈
#檢測播放器標題

#歡迎訊息與使用者設定
def main():
    keyboard = Controller()
    root = tk.Tk()
    root.withdraw()
    welcome = input('歡迎使用超強動畫截圖~~請輸入y開始，離開請按n:')
    user_time = input('請問要幾秒截一張:')
    user_time = float(user_time)
    print('請於下一個畫面選擇儲存截圖的資料夾!')

    if welcome == 'y':
        shots_path = filedialog.askdirectory()
        print('截圖資料夾路徑為:', shots_path)
        time.sleep(2)
        print('倒數五秒請開好動畫謝謝')
        time.sleep(5)
    elif welcome == 'n':
        Break


    shots_count = 0
    delete_count = 0
    #定時截圖並且讀出最新的兩張圖
    while True: 
        keyboard.press(Key.ctrl.value)
        keyboard.press('e')
        keyboard.release('e')
        keyboard.release(Key.ctrl.value)
        shots_count = shots_count + 1
        time.sleep(user_time)

        lists = []
        shots = shots_path
        shots2 = shots_path
        for file in os.listdir(shots):
            if file.endswith(".jpg"):
                lists.append(file)                                          #列出目錄的下所有文件和文件夾保存到lists
        lists.sort(key=lambda fn:os.path.getmtime(shots + "\\" + fn))       #按時間排序
        shot_1 = os.path.join(shots2, lists[-1])    #最新                   #獲取最新的文件保存到file_new
        shot_2 = os.path.join(shots2, lists[-2])    #第二新
        print(shot_1, shot_2)

        #圖片相似度辨識
        # 計算圖片的局部哈希值--pHash
        def phash(img):
            """
            :param img: 圖片
            :return: 返回圖片的局部hash值
            """
            img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
            avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
            hash_value=reduce(lambda x, y: x | (y[1] << y[0]), enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())), 0)
            print(hash_value)
            return hash_value


        # 計算漢明距離:
        def hamming_distance(a, b):
            """
            :param a: 圖片1的hash值
            :param b: 圖片2的hash值
            :return: 返回兩個圖片hash值的漢明距離
            """
            hm_distance=bin(a ^ b).count('1')
            print(hm_distance)
            return hm_distance


        # 計算兩個圖片是否相似:
        def is_imgs_similar(img1,img2):
            """
            :param img1: 圖片1
            :param img2: 圖片2
            :return:  True 圖片相似  False 圖片不相似
            """
            return True if hamming_distance(phash(img1),phash(img2)) <= 5 else False


        if __name__ == '__main__':

            # 讀取圖片
            sensitive_pic = Image.open(shot_1)
            target_pic = Image.open(shot_2)

            # 比較圖片相似度
            result=is_imgs_similar(target_pic, sensitive_pic)

            print(result)
            print('目前為止截了:', shots_count, '張', '刪除了:', delete_count, '張相似截圖')
        

        if result == True:
            os.remove(shot_2)
            delete_count = delete_count + 1
    
main()
import numpy as np
import cv2

def main1():
    import re
    # 提示用户输入图片路径
    while True:
        path = input("请输入图片地址：").replace("\\", "/").strip('"')
        if re.search('[\u4e00-\u9fa5]', path):
            print("输入不能包含中文，请重新输入！")
        else:
            break
    img = cv2.imread(path)
    height, width, channels = img.shape
    bgr_values = np.array([img[y, x] for y in range(img.shape[0]) for x in range(img.shape[1])])
    name = input("请输入要添加的水印：")
    message = "11111111" + "".join(format(ord(c), '08b') for c in name)
    messages = (message * (height * width * 3 // len(message) + 1))[:height * width * 3]
    arr = np.array([int(c) for c in messages])
    arr_2d = arr.reshape((height * width, 3))
    # 比较两个数组中对应数字的奇偶性
    cond = (arr_2d % 2 == bgr_values % 2)
    # 若b中为奇数，a中为偶数，则a中数加1
    bgr_values[~cond & (arr_2d % 2 == 1)] += 1
    # 若b中为偶数，a中为奇数，则a中减1
    bgr_values[~cond & (arr_2d % 2 == 0)] -= 1
    # 生成 bgr 像素值数组
    bgr_array = np.array(bgr_values)
    # 转换为图片格式并设置高度和宽度
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:, :, :] = bgr_array.reshape(height, width, 3)
    # 保存图片
    new_path = "C:/Users/wuwuy/Desktop/new.png"
    cv2.imwrite(new_path, img)
    print('成功，图在桌面，名为"new.png"')

def main2():
    import re
    # 提示用户输入图片路径
    while True:
        path = input("请输入图片地址：").replace("\\", "/").strip('"')
        if re.search('[\u4e00-\u9fa5]', path):
            print("输入不能包含中文，请重新输入！")
        else:
            break
    img = cv2.imread(path)
    height, width, channels = img.shape
    arr = np.array([img[y, x] for y in range(img.shape[0]) for x in range(img.shape[1])])
    arr = arr % 2
    arr = arr.reshape(-1)
    re = arr.nbytes // (8 * arr.itemsize)

    for i in range(1):
        b = arr[i:8 * (re - 1) + i]
        b_2 = b.reshape(((re - 1), 8))
        b_10 = np.packbits(b_2, axis=1)
        b_1 = b_10.ravel()
        mask1 = (b_1 > 126) & (b_1 < 255)
        b_0 = np.delete(b_1, np.where(mask1))
        mask2 = (b_0 >= 0) & (b_0 < 32)
        b_0 = np.delete(b_0, np.where(mask2))
        if ((b_0 == 255).sum() >= 2) and ((b_0 != 255).any()):
            b_0[b_0 == 255] = 124
            # 创建bool索引数组
            mask = b_0 == 124
            # 使用np.split函数切割原数组
            pieces = np.split(b_0, np.where(mask)[0] + 1)
            # 找到子数组的最大长度
            max_len = max(len(row) for row in pieces)
            # 填充到相同长度
            padded_arr = np.array(
                [np.pad(row, (0, max_len - len(row)), 'constant', constant_values=124) for row in pieces])
            # 获取子数组和其出现次数
            unique_arr, counts = np.unique(padded_arr, axis=0, return_counts=True)
            # 找到出现次数大于1的子数组
            mask = counts > 1
            multi_occurrence_arr = unique_arr[mask]
            # 打印符合要求的子数组
            if len(multi_occurrence_arr) == 0:
                print('')
            else:
                max_count = np.max(counts)
                mask = counts == max_count
                max_occurrence_arr = unique_arr[mask]
                # 如果有多个最大值，则打印所有符合要求的子数组
                if len(max_occurrence_arr) > 1:
                    for a in max_occurrence_arr:
                        if not np.all(a == 124):
                            a = a[:-1]
                            string = ''.join(map(chr, a.astype(int)))
                            string = string.replace("|", "")
                            print(string)

                else:
                    if not np.all(max_occurrence_arr[0] == 124):
                        a = max_occurrence_arr[0][:-1]
                        string = ''.join(map(chr, a.astype(int)))
                        string = string.replace("|", "")
                        print(string)

while True:
    symbol = input("请输入+(加印)-(解印)q(退出)：")
    if symbol == "+":
        main1()
    elif symbol == "-":
        main2()
    elif symbol == "q":
        break
    else:
        # 输入错误
        print("输入错误，请重新输入")

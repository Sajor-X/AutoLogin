import ddddocr

from PIL import Image, ImageDraw
from urllib import request

from captcha.util import Base64Util


class Verify(object):
    def __init__(self):
        self.util = Base64Util()
        self.ocr = ddddocr.DdddOcr(old=True)

    def download_file(self, uri, path=None):
        """
        下载网络资源并保存至本地
        :param uri: 资源路径
        :param path: 保存地址
        :return: path
        """
        return request.urlretrieve(uri, path)[0]

    def binarization(self, threshold=240):
        """
        图片二值化
        :param threshold: 阈值
        :return: 图片数组
        """
        return [0 if _ < threshold else 1 for _ in range(256)]

    def get_pixel(self, image, x, y, threshold, dots_num):
        """
        获取该像素点颜色，返回修改后的颜色

        :param image: 图片
        :param x: x坐标
        :param y: y坐标
        :param threshold: 阈值
        :param dots_num: 邻接点数
        :return: 该点最终颜色
        """
        pixel = image.getpixel((x, y))

        # 与阈值比较
        pixel = True if pixel >= threshold else False

        near_dots = 0
        next_step = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        for _x, _y in next_step:
            if pixel == (image.getpixel((x + _x, y + _y)) >= threshold):
                near_dots += 1
        return 1 if near_dots < dots_num else None

    def clear_noise(self, image, threshold, dots_num, count):
        """
        降噪
        :param image: 图片
        :param threshold: 阈值
        :param dots_num: 临界点数
        :param count: 降噪次数
        :return:
        """
        draw = ImageDraw.Draw(image)

        for _ in range(0, count):
            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    color = self.get_pixel(image, x, y, threshold, dots_num)
                    if color is not None:
                        # 1. 白  0. 黑
                        draw.point((x, y), color)

    def denoising_ocr(self, file, threshold=240, count=1):
        """
        处理
        :param file:
        :param threshold: 阈值
        :param count: 轮数
        :return:
        """
        # 灰度
        image = Image.open(file).convert('L')
        # 二值化
        image = image.point(self.binarization(threshold), '1')
        # 降噪
        self.clear_noise(image, 1, 4, count)
        image = image.resize((image.width * 2, image.height * 2), Image.ANTIALIAS)

        image.save("captcha_denoising.png")
        with open("captcha_denoising.png", 'rb') as f:
            image = f.read()
        result = self.ocr.classification(image)
        # result = tesserocr.image_to_text(image)
        return result.replace(" ", "")[:4]

    def save_file(self, url, file_name="captcha.png"):
        if url:
            request.urlretrieve(url, file_name)
        with open(file_name, 'rb') as f:
            image = f.read()
            result = self.ocr.classification(image)
        return result.replace(" ", "")[:4]

    def get_captcha_code(self, url, file_name="captcha.png"):
        opener = request.build_opener()
        opener.addheaders = ([("User-Agent",
                               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36")])
        request.install_opener(opener)
        file = request.urlretrieve(url, file_name)[0]
        return self.denoising_ocr(file)

    def get_code(self, base64_code):
        file = self.util.decode_base64_file(base64_code, "none.png")
        return self.denoising_ocr(file)

    def get_file(self, base64_code):
        return self.util.decode_base64_file(base64_code, "none.png")


if __name__ == '__main__':
    v = Verify()
    # code = v.get_captcha_code("http://erpapi.test.zxdns.com/api/kcone/auth/captcha?1609512337985&ticket=0.7072632701797432")
    code = v.denoising_ocr("captcha.png")
    print(code)

    code = v.denoising_ocr("test.png", 120, 0)
    print(code)


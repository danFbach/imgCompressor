from PIL import Image
import os


class img_compress(object):

    @staticmethod
    def get_image_dir():
        return input("Enter Images Directory: ")

    @staticmethod
    def get_dimensions(img_type, dim_type):
        dmns = input("Please enter preferred " + dim_type + " for " + img_type + ": ")
        try:
            dmns_int = int(dmns)
            return dmns_int
        except ValueError:
            print("Invalid input, please enter only Numbers.")
            return  img_compress.get_dimensions(img_type, dim_type)

    @staticmethod
    def ask_dim(img_type, dim_type, default_dim):
        ans = input("Do you want to use a custom " + dim_type + " (Y/N)? Default " + dim_type + " for " + img_type + ": " + str(default_dim))
        if ans.lower() == 'y':
            return img_compress.get_dimensions(img_type, dim_type)
        elif ans.lower() == 'n':
            return default_dim
        else:
            print("Invalid input.")
            return img_compress.ask_dim(img_type, dim_type, default_dim)

    @staticmethod
    def check_dir(home_dir, dir):
        if not os.path.exists(home_dir + "/" + dir):
            os.makedirs(home_dir + "/"  + dir)
            os.chmod(home_dir + "/"  + dir, 0o777)
        return home_dir + "/"  + dir + '/'

    @staticmethod
    def compress_and_short(old_image, path, dimensions):
        img0 = Image.open(path + "/" + old_image)
        img1 = Image.open(path + "/" + old_image)
        width, height = img0.size
        print(old_image)
        fn, f_ext = os.path.splitext(old_image)
        # MAKE FULL
        new_path = img_compress.check_dir(path, "/full/")
        img0.save(new_path +"{}{}".format(fn, f_ext), quality=90)
        # MAKE SHORT
        new_path = img_compress.check_dir(path, "/short/")
        short_size, transform_size, ratio_size, dimensions = img_compress.get_short_data(old_image, height, width, dimensions)
        img2= img1.resize(ratio_size, Image.ANTIALIAS)
        img3 = img2.transform(short_size, Image.EXTENT, transform_size)
        img3.save(new_path + "{}{}".format(fn, f_ext), quality=90)
        return dimensions


    @staticmethod
    def get_short_data(img, height, width, dimensions):
        new_width = 0
        if("Full" in img):
            new_width = dimensions['f_width']
            width_ratio = new_width / width
        elif("Tab" in img):
            new_width = dimensions['t_width']
            width_ratio = new_width / width
        elif("Mob" in img):
            new_width = dimensions['m_width']
            width_ratio = new_width / width
        ratio_height = int(height * width_ratio)
        short_size = (new_width, dimensions['s_height'])
        ratio_size = new_width, ratio_height
        transform_size = (0, 0, new_width , dimensions['s_height'])
        return short_size, transform_size, ratio_size, dimensions

    @staticmethod
    def get_files(image_dir):
        images = os.listdir(image_dir)
        return images

    @staticmethod
    def make_new_images(dir, imgs, dimensions):
        dimensions['s_height'] = img_compress.ask_dim("all cropped images", "crop height", dimensions['s_height'])
        dimensions['f_width'] = img_compress.ask_dim("Full Size", "width", dimensions['f_width'])
        dimensions['t_width'] = img_compress.ask_dim("Tablet", "width", dimensions['t_width'])
        dimensions['m_width'] = img_compress.ask_dim("Mobile", "width", dimensions['m_width'])
        for img in imgs:
            dimensions = img_compress.compress_and_short(img, dir, dimensions)

dimensions = {"f_width": 1200, "t_width": 700, "m_width": 320, "s_height": 1200}
dir = img_compress.get_image_dir()
img_pack = img_compress.get_files(dir)
img_compress.make_new_images(dir ,img_pack, dimensions)
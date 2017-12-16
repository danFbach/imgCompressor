from PIL import Image
from sys import argv
import os


class img_compress(object):

    @staticmethod
    def get_image_dir():
        new_dir = input("Enter Images Directory: ")
        if not os.path.exists(new_dir) and not os.path.basename(new_dir):
            return img_compress.get_image_dir()
        else:
            return new_dir

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
    def make_dir(home_dir, dir):
        if not os.path.exists(home_dir + "/" + dir):
            os.makedirs(home_dir + "/"  + dir)
            os.chmod(home_dir + "/"  + dir, 0o777)
        return home_dir + "/"  + dir + '/'

    @staticmethod
    def compress_img(original_image, path, new_dir):
        fn, f_ext = os.path.splitext(original_image)
        img0 = Image.open(path + "/" + original_image)
        new_path = img_compress.make_dir(path, '/' + new_dir + '/')
        img0.save(new_path +"{}{}".format(fn, f_ext), quality=85)
        print('Compressed ' + original_image)


    @staticmethod
    def resize_and_crop(old_image, path, dimensions, new_dir):
        img1 = Image.open(path + "/" + old_image)
        width, height = img1.size
        fn, f_ext = os.path.splitext(old_image)
        # MAKE SHORT
        new_path = img_compress.make_dir(path, new_dir)
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
        else:
            new_width = dimensions['w']
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
    def make_new_images(dir, imgs, dimensions, new_dir):
        dimensions['s_height'] = img_compress.ask_dim("all cropped images", "crop height", dimensions['s_height'])
        dimensions['f_width'] = img_compress.ask_dim("Full Size", "width", dimensions['f_width'])
        dimensions['t_width'] = img_compress.ask_dim("Tablet", "width", dimensions['t_width'])
        dimensions['m_width'] = img_compress.ask_dim("Mobile", "width", dimensions['m_width'])
        for img in imgs:
            dimensions = img_compress.resize_and_crop(img, dir, dimensions, new_dir)
            print('Cropped ' + img)

    @staticmethod
    def make_new_image(dir, img, dimensions, new_dir):
        dimensions['s_height'] = img_compress.ask_dim("all cropped images", "crop height", dimensions['s_height'])
        dimensions = img_compress.resize_and_crop(img, dir, dimensions, new_dir)
        print('Cropped ' + img)

    @staticmethod
    def get_opts(argv):
        opts = {}  # Empty dictionary to store key-value pairs.
        cmds = ["", ""]
        while argv:  # While there are arguments left to parse...
            if argv[0][0] == '-' and argv[0][1] == '-':
                cmds.insert(0, (argv[0]))
                break
            if argv[0][0] == '-':  # Found a "-name value" pair.
                opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
            argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
            # print(argv[0])
        return opts, cmds

    @staticmethod
    def use_opts(myargs, cmds):
        print(cmds)
        print(myargs)
        dir = ''
        dimensions = {"f_width": 1200, "t_width": 700, "m_width": 320, "s_height": 1200, 'gen_height': 1000, 'gen_width': 1000}
        if '--help' in cmds:
            br='\n\r'
            print(  'Python Image Utility v0.1   -   Author: danFbach' + br + br +
                    '       -d dir' + br +
                    '               Direcory with image files.' + br +
                    '               dir = Directory.' + br +
                    '       -i file' + br +
                    '               Image file.' + br +
                    '               file = path to file, including filename.' + br +
                    '       -c dir' + br +
                    '               Compress file(s).' + br +
                    '               dir = output folder as sub-directory of input directory.' + br +
                    '       -cropped dir'+ br +
                    '               Crop image(s).' + br +
                    '               dir = output folder as sub-directory of input directory.')
        # if '-i' not in myargs and '-d' not in myargs:
        #     dir = img_compress.get_image_dir()
        #     img_pack = ()
        #     if not os.path.basename():
        #         img_pack = img_compress.get_files(dir)
        #     else:
        #         if '-c' in myargs:
        #             img_compress.compress_img(os.path.basename(myargs['-i']), os.path.dirname(myargs['-i']), myargs['-c'])
        #         if '-cropped' in myargs:
        #             img_compress.make_new_images(os.path.dirname(dir), os.path.basename(dir), dimensions, myargs['-cropped'])
        if '-d' in myargs:
            dir = myargs['-d']
            img_pack = img_compress.get_files(dir)
            if '-c' in myargs:
                for img in img_pack:
                    img_compress.compress_img(img, dir, myargs['-c'])
            if '-cropped' in myargs:
                img_compress.make_new_images(dir, img_pack, dimensions, myargs['-cropped'])
        elif '-i' in myargs and '-c' in myargs:
            img_compress.compress_img(os.path.basename(myargs['-i']), os.path.dirname(myargs['-i']), myargs['-c'])
            print('Compressed ' + os.path.basename(myargs['-i']))


opts, cmds = img_compress.get_opts(argv)
img_compress.use_opts(opts, cmds)
# dir = img_compress.get_image_dir()
# img_pack = img_compress.get_files(dir)
# img_compress.make_new_images(dir ,img_pack, dimensions)


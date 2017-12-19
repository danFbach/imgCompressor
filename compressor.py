from PIL import Image
from sys import argv
import os


class img_compress(object):
    allowedft = ['.bmp', '.gif', '.jpeg', '.png', '.tiff']
    @staticmethod
    def get_image_dir():
        new_dir = input("Enter directory for multiple images or a location for a single image.")
        if not os.path.exists(new_dir) and not os.path.basename(new_dir):
            print('Invalid directory or location.')
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
    def compress_img(original_image, path, new_dir, filetype):
        f_name, f_ext = os.path.splitext(original_image)
        print(f_ext)
        print(filetype)
        if filetype is '':
            filetype = f_ext
        img0 = Image.open(path + "/" + original_image)
        new_path = img_compress.make_dir(path, '/' + new_dir + '/')
        img_compress.save_new_image(img0, f_name, filetype, new_path)
        # if filetype == '.png':
        #     img0.save(new_path +"{}{}".format(fn, filetype), optimize=True)
        # elif filetype is '.jpg':
        #     img0.save(new_path +"{}{}".format(fn, filetype), quality=85)
        print('Compressed: ' + f_name + filetype)

    @staticmethod
    def resize_percent(img, path, percent, ext):
        percentage = int(percent) / 100
        save_path = img_compress.make_dir(path, 'resize')
        img0 = Image.open(path + '/' + img)
        f_name, f_ext = os.path.splitext(img)
        width, height = img0.size
        if ext is "":
            ext = f_ext
        f_name, f_ext = os.path.splitext(img)
        new_width = int(width * percentage)
        new_height = int(height * percentage)
        new_size = new_width, new_height
        img00 = img0.resize(new_size, Image.ANTIALIAS)
        print(ext + "   " + save_path)
        img_compress.save_new_image(img00, f_name, ext, save_path)
        print('Resized: ' + f_name + ext + ' to ' + percent + '%.')

    @staticmethod
    def save_new_image(img, f_name, new_ext, path):
        if new_ext == 'png':
            img.save(path + "{}{}".format(f_name, new_ext), optimize=True)
        elif new_ext == '.jpeg':
            img.save(path +"{}{}".format(f_name, new_ext), quality=85)

    @staticmethod
    def resize_and_crop(original_image, path, dimensions, new_dir, filetype):
        img1 = Image.open(path + "/" + original_image)
        width, height = img1.size
        f_name, f_ext = os.path.splitext(original_image)
        if filetype is "":
            filetype = f_ext
        new_path = img_compress.make_dir(path, new_dir)
        short_size, transform_size, ratio_size, dimensions = img_compress.get_short_data(original_image, height, width, dimensions)
        img2= img1.resize(ratio_size, Image.ANTIALIAS)
        img3 = img2.transform(short_size, Image.EXTENT, transform_size)
        # img3.save(new_path + "{}{}".format(f_name, filetype), optimize=True)
        img_compress.save_new_image(img3, f_name, filetype, new_path)
        print('Cropped: ' + f_name + filetype)
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
        short_size = new_width, dimensions['s_height']
        ratio_size = new_width, ratio_height
        transform_size = (0, 0, new_width , dimensions['s_height'])
        return short_size, transform_size, ratio_size, dimensions

    @staticmethod
    def get_files(image_dir):
        images = os.listdir(image_dir)
        return images

    @staticmethod
    def run_one(img, dimensions, actions):
        new_ft = ''
        if '-ft' in actions:
            if actions['-ft'] in img_compress.allowedft:
                new_ft = actions['-ft']
            else:
                print('You chose an invalid filetype. Files will be compressed to original format.')
        if '-cm' in actions:
            img_compress.compress_img(os.path.basename(img), os.path.dirname(img), actions['-cm'], new_ft)
        if '-cr' in actions:
            pass


    @staticmethod
    def run_multi(dir, dimensions, actions):
        new_ft = ""
        img_pack = img_compress.get_files(actions['-d'])
        if '-ft' in actions:
            if actions['-ft'] in img_compress.allowedft:
                new_ft = actions['-ft']
            else:
                print('You chose an invalid filetype. Files will be compressed to original format.')
        if '-cm' in actions:
            for img in img_pack:
                img_compress.compress_img(img, dir, actions['-cm'], new_ft)
        if '-cr' in actions:
            img_compress.make_new_images(dir, img_pack, dimensions, actions['-cr'])
        if '-rp' in actions:
            for img in img_pack:
                img_compress.resize_percent(img, dir, actions['-rp'], new_ft)

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
        while argv:
            if len(argv) == 1:
                opts[argv[0]] = ''
            else:
                if argv[0][0] == '-':
                    opts[argv[0]] = argv[1]
            argv = argv[1:]
        return opts, cmds

    @staticmethod
    def use_opts(myargs, cmds):
        dimensions = {"f_width": 1200, "t_width": 700, "m_width": 320, "gen_height": 1000, 'gen_width': 1000}
        if '-help' in myargs:
            br='\n\r'
            print(  'Python Image Utility v0.1   -   Author: danFbach' + br + br +
                    '       -d dir' + br +
                    '               Direcory with image files. If unset, you will be asked.' + br +
                    '               dir = Directory.' + br +
                    '       -i file' + br +
                    '               Image file. If unset, you will be asked.' + br +
                    '               file = path to file, including filename.' + br +
                    '       -cm dir' + br +
                    '               Compress file(s).' + br +
                    '               dir = output folder as sub-directory of input directory.' + br +
                    '       -cr dir'+ br +
                    '               Crop image(s).' + br +
                    '               dir = output folder as sub-directory of input directory.' +br+
                    '       -rp percent' +br+
                    '               Resize percent.'+br+
                    '               percent = integer between 1 and 100. No % symbol.'+br+
                    '       -ft type' +br+
                    '               Sets new filetype. If left unset, will just use original'+br+
                    '               type=filetype (options: .jpeg, .png)'+br)
                    # '               type=filetype (options: bmp, gif, jpeg, png, tiff)'+br)
        elif '-help' not in myargs:
            if '-i' not in myargs and '-d' not in myargs:
                dir = img_compress.get_image_dir()
                if not os.path.basename(dir):
                    img_compress.run_multi(dir, dimensions, myargs)
                else:
                    img_compress.run_one(dir, dimensions, myargs)
            if '-d' in myargs:
                img_compress.run_multi(myargs['-d'], dimensions, myargs)
            elif '-i' in myargs:
                img_compress.run_one(myargs['-i'], dimensions, myargs)


opts, cmds = img_compress.get_opts(argv)
img_compress.use_opts(opts, cmds)
# dir = img_compress.get_image_dir()
# img_pack = img_compress.get_files(dir)
# img_compress.make_new_images(dir ,img_pack, dimensions)


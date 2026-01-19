from PIL import Image
import sys
import os
import time

if __name__ == '__main__':
    factor = False
    print('Convert image for OLED 128x64')
    route = os.path.dirname(os.path.abspath(__file__))
    folder_i = os.path.join(route, 'image')
    files = os.listdir(folder_i)
    if len(files) == 0:
        print(f'Add image file to image folder')
        time.sleep(3)
        sys.exit()
    elif len(files) > 1:
        print(f'Only one file is required')
        time.sleep(3)
        sys.exit()

    img = Image.open(os.path.join(folder_i, files[0]))

    if '.bmp' not in files[0]:  # in case it is not a BMP file, it is converted
        img_mono = img.convert('L')
        img_binaria = img_mono.point(lambda p: 255 if p > 128 else 0)
        img_binaria.save(os.path.join(route, 'bmp_image.bmp'), format='BMP')
        img = Image.open(os.path.join(route, 'bmp_image.bmp'))

    if factor:  # change the image size
        w, h = img.size
        print(f'Image of width {w} and height {h}')
        factor = 64 / h
        img_p = img.resize((int(w*factor), int(h*factor)))
        width, height = img_p.size
        print(f'New image of width {width} and height {height}')
    else:
        width, height = img.size

    content = ''
    print(f'#define LOGO_HEIGHT {height}')
    content = content + f'#define LOGO_HEIGHT {height}\n'
    print(f'#define LOGO_WIDTH {width}')
    content = content + f'#define LOGO_WIDTH {width}\n'

    if width % 8 != 0:
        compensate = 8 - (width % 8)
    else:
        compensate = 0

    n_width = width + compensate
    img_n = img.resize((n_width, height))

    img_binary = img_n.convert("1")  # convert to gray scale and binary
    pixels = list(img_binary.getdata())  # get values for pixels, 1 and 0

    print('static const unsigned char PROGMEM logo_bmp[] =')
    content = content + f'static const unsigned char PROGMEM logo_bmp[] =\n'
    for i, pix in enumerate(pixels):
        if i % 8 == 0:
            if i == 0:
                print('{')
                content = content + '{\n'
            else:
                print(', ', end='')
                content = content + ', '

        if i % n_width == 0:
            if i != 0:
                print()
                content = content + '\n'

        if i % 8 == 0:
            print('0b', end='')
            content = content + '0b'

        if pix == 255:
            print(0, end='')
            content = content + '0'
        else:
            print(1, end='')
            content = content + '1'
    print('\n};')
    content = content + '\n};'
    folder_c = os.path.join(route, 'ImageOLED')  # creates h file in this route
    with open(os.path.join(folder_c, 'image_code.h'), 'w') as f:
        f.write(content)
    print('File image_code.h created successfully')
    input('Press enter to exit...')

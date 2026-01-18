from PIL import Image
import os, sys

if __name__ == '__main__':
    factor = False
    print('Convert image for OLED 128x64')
    route = os.getcwd()
    files = os.listdir(route + '/image/')
    if len(files) == 0:
        print(f'Add image file to image folder')
        sys.exit()
    elif len(files) > 1:
        print(f'Only one file is required')
        sys.exit()

    img = Image.open(route + '/image/' + files[0])
    if factor:
        w, h = img.size
        print(f'Image of width {w} and height {h}')
        factor = 64 / h
        print(f'El factor es de {factor}')
        img_p = img.resize((int(w*factor), int(h*factor)))
        width, height = img_p.size
        print(f'New image of width {width} and height {height}')
    else:
        width, height = img.size

    if width > 128:
        print(f'Image width larger than expected: {width}, it must be below 128')
    elif height > 64:
        print(f'Image height larger than expected: {height}, it must be below 64')

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

    img_binaria = img_n.convert("1")  # convert to gray scale and binary

    # Obtener los valores (0 para negro, 1 para blanco)
    pixels = list(img_binaria.getdata())

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

    with open(route + '/ImageOLED/image_code.h', 'w') as f:
        f.write(content)
    print('File image_code.h created successfully')
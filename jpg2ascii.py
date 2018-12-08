from PIL import Image
import numpy as np


def ascii_from_image(file_name, screen_width=100, charslist=' `\'.-/ilnmoILO', wcf=7 / 4):
    chars = np.asarray(list(charslist))

    image = file_name

    f, GCF, WCF = image, 1, wcf

    img = Image.open(f)
    width = img.size[0]
    height = img.size[1]
    screen_height = screen_width * height / width / WCF
    S = (int(screen_width), int(screen_height))
    img = np.asarray(img.resize(S)).copy()
    if len(np.shape(img)) == 3:
        img = np.sum(img, axis=2)
    img -= img.min()
    img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)

    return "\n".join(("".join(r) for r in chars[img.astype(int)]))


if __name__ == "__main__":
    print(ascii_from_image('res/telochka.jpg'))

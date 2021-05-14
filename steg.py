from PIL import Image
import click

class Steganography:

    @staticmethod
    def int_to_bin(rgb):
        r, g, b = rgb
        return (format(r,'08b'), format(g,'08b'), format(b,'08b'))

    @staticmethod
    def bin_to_int(rgb):
        r, g, b = rgb
        return (int(str(r), 2), int(str(g), 2), int(str(b), 2))

    @staticmethod
    def bin_merge(rgb1, rgb2):
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        return (int(str(r1)[:4] + str(r2)[:4]), int(str(g1)[:4] + str(g2)[:4]), int(str(b1)[:4] + str(b2)[:4]))

    @staticmethod
    def hide(mask, secret):
        mask, secret = Image.open(mask), Image.open(secret) 
        mask = mask.resize(secret.size)

        if secret.size[0] > mask.size[0] or secret.size[1] > mask.size[1]:
            raise ValueError('Secret image should not be larger than its mask')

        pix_mask = mask.load()
        pix_secret = secret.load()

        out = Image.new(mask.mode, mask.size)
        pix_out = out.load()

        for i in range(mask.size[0]):
            for e in range(mask.size[1]):
                rgb1 = Steganography.int_to_bin(pix_mask[i, e])
                rgb2 = Steganography.int_to_bin((0,0,0))

                if i < secret.size[0] and e < secret.size[1]:
                    rgb2 = Steganography.int_to_bin(pix_secret[i, e])

                rgb = Steganography.bin_merge(rgb1, rgb2)

                pix_out[i, e] = Steganography.bin_to_int(rgb)
        
        return out

    @staticmethod
    def reveal(img):
        img = Image.open(img)
        pix_img = img.load()

        out = Image.new(img.mode, img.size)
        pix_out = out.load()

        size = img.size

        for i in range(img.size[0]):
            for e in range(img.size[1]):
                r, g, b = Steganography.int_to_bin(pix_img[i, e])

                rgb = (r[4:] + '0000', g[4:] + '0000', b[4:] + '0000')

                pix_out[i, e] = Steganography.bin_to_int(rgb)

                if pix_out[i, e] != (0, 0, 0):
                    size = (i + 1, e + 1)

        out = out.crop((0, 0, size[0], size[1]))
        
        return out

@click.group()
def cli():
    pass

@cli.command()
@click.option('--mask', required=True, type=str, help='Image that will hide secret image')
@click.option('--secret', required=True, type=str, help='Image that will be hidden')
@click.option('--output', required=True, type=str, help='New image')
def hide(mask, secret, output):
    a = Steganography.hide(mask, secret)
    a.save(output + '.png')

@cli.command()
@click.option('--secret', required=True, type=str, help='Image that will be "decoded"')
@click.option('--output', required=True, type=str, help='New Image')
def reveal(secret, output):
    if secret[-4:] != '.png':
        print('Image must be a PNG')
        return
    
    a = Steganography.reveal(secret)
    a.save(output + '.png')

if __name__ == '__main__':
    cli()

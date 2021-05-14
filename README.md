# Steganography

05/13/2021

According to Wikipedia, [steganography](https://en.wikipedia.org/wiki/Steganography) is the practice of hiding one message in another. This technique has been used during a variety of instances throughout history, even dating back to 440 BC in Greece. This project is an implementation of a steganography method called "least significant bits" (LSB) to hide one image within another.

## Hide a secret image

First, the RGB values of each pixel in a mask image and secret image will be converted to 8-bit binary digits:

![download](https://user-images.githubusercontent.com/71541167/118223579-78a14280-b436-11eb-9847-7be2a64dc910.png)

Next, the first four, or most significant bits, will be taken out of corresponding pixels from each image. The four bits of the mask image will be place at the first four place values of a corresponding pixel of a new image. The four bits of the secret image will be placed at the last four place values, or the least significant bits, of the corresponding pixel:

![68747470733a2f2f63646e2d696d616765732d312e6d656469756d2e636f6d2f6d61782f323030302f312a6b704461306a74366674536365346234445141324d512e706e67](https://user-images.githubusercontent.com/71541167/118224031-33314500-b437-11eb-872d-6526fc8f1541.png)

Lastly, the binary digits of each pixel will be turned back into RGB values to create a final image that holds the secret message.

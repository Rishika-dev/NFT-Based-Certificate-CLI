from generateCertificate import generateQR
from PIL import Image

img = generateQR("test")
img.save("test.png")
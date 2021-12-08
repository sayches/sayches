import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def check_image_exists(image):
    check = False
    try:
        check = True if image.size else False
    except:
        pass
    return check


def resize_image(image):
    check = check_image_exists(image)
    if check:
        imageTemproary = Image.open(image)
        if imageTemproary.mode in ("RGBA", "P"):
            imageTemproary = imageTemproary.convert("RGB")
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((300, 300))
        imageTemproaryResized.save(outputIoStream, format='JPEG', quality=70)
        outputIoStream.seek(0)
        resized_image = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                             "%s.jpg" % image.name.split('.')[0], 'image/jpeg',
                                             sys.getsizeof(outputIoStream), None)
        return resized_image
    return image

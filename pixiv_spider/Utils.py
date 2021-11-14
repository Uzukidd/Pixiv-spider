import imageio
import zipfile
import io

def zip2gif(zip:bytes, durations:list) -> bytes :
    images = []
    for image, name in extract_zip(zip) :
        images.append(imageio.imread(image))
    
    return imageio.mimsave(imageio.RETURN_BYTES, images, duration = durations, format = ".gif")

def extract_zip(zip:bytes) -> bytes:
    buffer = io.BytesIO(initial_bytes = zip)
    with zipfile.ZipFile(file = buffer) as zip_file :
        for file_name in zip_file.namelist() :
            with zip_file.open(file_name) as s :
                yield (s.read(), file_name)
                
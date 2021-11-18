import os
from typing import List

from pygame import image, surface

def listdir_clean(path: str) -> List[str]:
   files = os.listdir(path)
   files = sorted(files)
   return list(filter(lambda x:x!='.DS_Store', files))

def pygame_load_images_list(path: str) -> List[surface.Surface]:
    file_list = listdir_clean(path)
    return [ image.load(os.path.join(path, file)) for file in file_list]

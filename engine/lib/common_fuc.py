import os
from typing import List

def listdir_clean(path: str) -> List[str]:
   files = os.listdir(path)
   return list(filter(lambda x:x!='.DS_Store', files))

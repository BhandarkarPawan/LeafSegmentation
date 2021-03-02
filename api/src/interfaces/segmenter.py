import numpy as np 
from abc import ABC, abstractmethod 
from typing import Dict 

class Segmenter(ABC):

    @abstractmethod
    def run(self, image: np.ndarray) -> Dict:
        raise NotImplementedError("You should implement this!")
    
import cv2
import numpy as np
import albumentations as A
from torchvision import transforms


class Compose(object):
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, item):
        item_ = item.copy()
        for t in self.transforms:
            item_ = t(item_)
        return item_


class Resize(object):
    def __init__(self, size=(320, 32)):
        self.size = size

    def __call__(self, item):
        item['image'] = cv2.resize(item['image'], self.size)
        return item


class Normalize(object):
    def __init__(self, mean=(0.5, 0.5, 0.5), std=(0.25, 0.25, 0.25)):
        self.mean = np.asarray(mean).reshape((1, 1, 3)).astype(np.float32)
        self.std = np.asarray(std).reshape((1, 1, 3)).astype(np.float32)

    def __call__(self, item):
        item["image"] = (item["image"] - self.mean) / self.std
        return item

    
class TransformByKeys(object):
    def __init__(self, transform, name='image'):
        self.transform = transform
        self.name = name
        
    def __call__(self, sample):
        transform = self.transform(sample)
        sample[self.name] = transform[self.name]
        return sample
        
        
def get_train_transforms(image_size):
    augmenter =  A.Compose([
                    A.Blur(p=0.05),
                    A.ColorJitter(p=0.05),
                    A.RandomBrightnessContrast(p=0.05),
                    A.Downscale(p=0.05),
                    A.ShiftScaleRotate(p=0.05),
                    A.Rotate([-25, 25], p=0.05)
    ])
    
    return Compose([
        TransformByKeys(lambda sample: augmenter(image=sample['image'])),
        Normalize(),
        Resize(size=image_size)
    ])


def get_val_transforms(image_size):
    return Compose([
        Normalize(),
        Resize(size=image_size),
    ])

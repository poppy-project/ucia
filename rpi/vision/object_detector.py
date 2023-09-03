from collections import namedtuple

from .yolo_model import YoloModel


VisualObject = namedtuple('VisualObject',
                          ('label', 'center', 'box', 'confidence'))


def detect_objects(img, render=False):
    yolo_img, res = YoloModel.detect_objects(img)

    if render:
        img[:] = yolo_img[:]

    boxes, scores, classes = res

    height, width, _ = img.shape

    found_obj = []
    for (box, score, cls) in zip(boxes, scores, classes):
        label = YoloModel.get_class_name(cls)

        (ly, lx, ry, rx) = box
        center = ((lx + 0.5 * (rx - lx)), (ly + 0.5 * (ry - ly)))

        obj = VisualObject(label, center, box, score)
        found_obj.append(obj)

    return found_obj

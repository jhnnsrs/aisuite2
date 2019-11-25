from structures.roi import LineROI
from structures.settings import Settings
from structures.stage import Stage
from structures.transformation import RectangleTransformation


def transformROItoRectangle(roi: LineROI, stage: Stage, settings: Settings):
    import logic.transformations as transformations
    image, boxwidths, pixelwidths, boxes = transformations.translateImageFromLine(stage.image, roi.vertices, settings.scale)
    transformation = RectangleTransformation()
    transformation.stagekey = stage.key
    transformation.roikey = roi.key
    transformation.key = roi.key
    transformation.image = image
    transformation.boxwidths = boxwidths
    transformation.pixelwidths = pixelwidths
    transformation.boxes = boxes
    transformation.colour = roi.colour
    transformation.method = "LineRoi to RectangularTransformation v1.0"

    return transformation
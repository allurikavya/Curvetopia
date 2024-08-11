import time

def fill_curve(self):
    import cv2
    import numpy as np
    image = self.imageToCv(self.image)
    h, w = image.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    seed_point = (w//2, h//2)
    color = (self.fill_color.red(), self.fill_color.green(), self.fill_color.blue())
    for i in range(100):
        modified_image = image.copy()
        _, _, mask, _ = cv2.floodFill(modified_image, mask, seed_point, color, (5,)*3, (5,)*3, flags=cv2.FLOODFILL_MASK_ONLY | (i << 8))
        self.image = self.cvToQImage(modified_image)
        self.update()
        time.sleep(0.05)  # Slow down the filling for animation effect

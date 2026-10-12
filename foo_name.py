import pygame

def resize_image(path, target_height: int):
    image = pygame.image.load(path).convert_alpha() # load image
    rect = image.get_bounding_rect() # get rect without backgorund

    if rect.width == 0 or rect.height == 0:
        raise ValueError(f"Image is empty {path}")

    image = image.subsurface(rect).copy() # Clear image and copy
    scale = target_height / image.get_height()

    nw = round(image.get_width() * scale)
    nh = round(image.get_height() * scale)

    return pygame.transform.smoothscale(image, (nw, nh))
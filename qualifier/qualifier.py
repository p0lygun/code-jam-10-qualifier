"""Code jam Qualifier."""

from pathlib import Path


import numpy as np
from PIL import Image


def valid_input(
    image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]
) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders,
    and `ordering` must use each input tile exactly once.

    """
    if image_size[0] % tile_size[0] != 0 or image_size[1] % tile_size[1] != 0:
        return False

    if not len(set(ordering)) == len(ordering):  # check for duplicates
        return False

    tiles = (image_size[0] * image_size[1]) / (tile_size[0] * tile_size[1])

    if not tiles.is_integer():  #  check if tiles is an integer
        return False

    if tiles != len(ordering):
        return False

    return True


def rearrange_tiles(
    image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str
) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    if not Path(image_path).exists():
        raise ValueError("The image path does not exist")

    image = np.array(Image.open(image_path))
    image_size = image.shape[:2]

    if not valid_input(image_size, tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")
    
    unscrambled_array = np.zeros(image.shape, dtype=np.uint8)
    m = max(image_size)
    rows = m // tile_size[1]
    columns = m // tile_size[0]

    
    # print(f"\n\nimage: {out_path}")
    # print(f"image_size: {image_size}, tile_size: {tile_size}")
    # print(f"columns: {columns}, rows: {rows}")

    for index, tile_index in enumerate(ordering):
        r = (index // rows) * tile_size[1]
        c = (index % columns) * tile_size[0]

        image_r = (tile_index // rows) * tile_size[1]
        image_c = (tile_index % columns) * tile_size[0]

        unscrambled_array[
            r : r + tile_size[0],
            c : c + tile_size[1],
        ] = image[
            image_r : image_r + tile_size[0],
            image_c : image_c + tile_size[1],
        ]


    img = Image.fromarray(unscrambled_array)
    img.save(f"{out_path}")


if __name__ == "__main__":
    from tests import TestInfo
    images = [
            TestInfo("images/pydis_logo_scrambled.png", (512, 512), (256, 256), "images/pydis_logo_order.txt",
                     "pydis_logo_unscrambled.png"),
            
            TestInfo("images/great_wave_scrambled.png", (1104, 1600), (16, 16), "images/great_wave_order.txt",
                     "great_wave_unscrambled.png"),
            
            TestInfo("images/secret_image1_scrambled.png", (800, 600), (20, 20), "images/secret_image1_order.txt",
                     "secret_image1_unscrambled.png"),
            
            TestInfo("images/secret_image2_scrambled.png", (800, 600), (20, 20), "images/secret_image2_order.txt",
                     "secret_image2_unscrambled.png")
    ]    


    for t in images:
        rearrange_tiles(
            image_path=t.scrambled_image_path,
            tile_size=t.tile_size,
            ordering=t.ordering,
            out_path=t.unscrambled_image_path,
        )

from PIL import Image

image = Image.open("tropical_bird.jpg")
width, height = image.size
pixels = image.load()


def find_closest_plattete_color(color):
    factor = 1
    return round((factor * color) // 255) * (255 // factor)


def dither_pixel(pixel_x, pixel_y, errors, fraction):
    r, g, b = pixels[pixel_x, pixel_y]
    error_r, error_g, error_b = errors
    r += round(error_r * fraction)
    g += round(error_g * fraction)
    b += round(error_b * fraction)
    return r, g, b


for row in range(height):
    for col in range(width):
        curr_r, curr_g, curr_b = pixels[col, row]
        new_r, new_g, new_b = (
            find_closest_plattete_color(curr_r),
            find_closest_plattete_color(curr_g),
            find_closest_plattete_color(curr_b),
        )
        errors = (curr_r - new_r, curr_g - new_g, curr_b - new_b)
        pixels[col, row] = (new_r, new_g, new_b)
        if col + 1 < width:
            pixels[col + 1, row] = dither_pixel(col + 1, row, errors, 7 / 16)

        if col + 1 < width and row + 1 < height:
            pixels[col + 1, row + 1] = dither_pixel(col + 1, row + 1, errors, 1 / 16)

        if row + 1 < height:
            pixels[col, row + 1] = dither_pixel(col, row + 1, errors, 5 / 16)

        if col - 1 > -1 and row + 1 < height:
            pixels[col - 1, row + 1] = dither_pixel(col - 1, row + 1, errors, 3 / 16)


image.save("result.jpg")

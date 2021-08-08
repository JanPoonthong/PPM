def save_as_ppm(width, height, pixels: hex, file_name):
    buffer = []
    with open(f"{file_name}.ppm", "w") as file:
        file.write(f"P3\n{width} {height} 255\n")
        for y in range(height):
            for x in range(width):
                pixel = pixels[y * width + x]
                buffer.append(f"{pixel >> 8 * 2 & 0xFF} ")
                buffer.append(f"{pixel >> 8 * 1 & 0xFF} ")
                buffer.append(f"{pixel >> 8 * 0 & 0xFF}  ")
        file.writelines(buffer)
    print(f"Saved {file_name}.ppm")


def circle(width, height, pixels, foreground, background):
    cx = width // 2
    cy = height // 2
    r = 100
    for y in range(height):
        for x in range(width):
            if ((x - cx) * (x - cx) + (y - cy) * (y - cy)) <= r * r:
                pixels[y * width + x] = foreground
            else:
                pixels[y * width + x] = background
    save_as_ppm(width, height, pixels, "circle")


def four_dimensional(width, height, pixels):
    for y in range(height):
        for x in range(width):
            pixels[y * width + x] = (x * y) * 0x010101
    save_as_ppm(width, height, pixels, "four_dimensional")


def wee_wee(width, height, pixels):
    for y in range(height):
        for x in range(width):
            pixels[y * width + x] = (
                ((x < 160) * (x > 96) * (y < 196) * (y > 64))
                + (((x - 128) * (x - 128) + (y - 64) * (y - 64)) < 32 * 32)
                + (((x - 96) * (x - 96) + (y - 196) * (y - 196)) < 32 * 32)
                + (((x - 160) * (x - 160) + (y - 196) * (y - 196)) < 32 * 32)
                > 0
            ) * 0x634D84
    save_as_ppm(width, height, pixels, "wee_wee")


def wee_wee_with_head(width, height, pixels):
    for y in range(height):
        for x in range(width):
            pixels[y * width + x] = (
                ((x < 160) * (x > 96) * (y < 196) * (y > 64))
                + (((x - 128) * (x - 128) + (y - 64) * (y - 64)) < 48 * 48)
                + (((x - 96) * (x - 96) + (y - 196) * (y - 196)) < 32 * 32)
                + (((x - 160) * (x - 160) + (y - 196) * (y - 196)) < 32 * 32)
                > 0
            ) * 0x634D84
    save_as_ppm(width, height, pixels, "wee_wee_with_head")


def checker_pattern(
    pixels: hex, height, width, tile_size, background, foreground
):
    for y in range(height):
        for x in range(width):
            if (x // tile_size + y // tile_size) % 2 == 0:
                pixels[y * width + x] = background
            else:
                pixels[y * width + x] = foreground
    save_as_ppm(width, height, pixels, "checker")


def stripes_pattern(
    pixels: hex, height, width, tile_size, background, foreground
):
    for y in range(height):
        for x in range(width):
            pixels[y * width + x] = (
                background if ((x + y) // tile_size) % 2 == 0 else foreground
            )
    save_as_ppm(width, height, pixels, "stripes")


def main():
    width = 256
    height = 256
    COLOR = 0x00FF00
    pixels = [COLOR] * (width * height)
    FOREGROUND = 0x634D84
    BACKGROUND = 0x000000
    checker_pattern(pixels, width, height, 10, FOREGROUND, BACKGROUND)
    stripes_pattern(pixels, width, height, 10, FOREGROUND, BACKGROUND)
    wee_wee(width, height, pixels)
    wee_wee_with_head(width, height, pixels)
    four_dimensional(width, height, pixels)
    circle(width, height, pixels, FOREGROUND, BACKGROUND)


main()

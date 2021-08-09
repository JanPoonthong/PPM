def save_as_ppm(width, height, pixels: hex, file_name):
    buffer = bytearray()
    for y in range(height):
        for x in range(width):
            pixel = pixels[y * width + x]
            buffer += bytes(
                [
                    pixel >> 8 * 2 & 0xFF,
                    pixel >> 8 * 1 & 0xFF,
                    pixel >> 8 * 0 & 0xFF,
                ]
            )
    with open(f"{file_name}.ppm", "wb") as file:
        file.write(bytes(f"P6\n{width} {height} 255\n", "ascii"))
        file.write(buffer)
    print(f"Saved {file_name}.ppm")


def hollow_circle(width, height, pixels, foreground):
    r = width // 2
    cx = width // 2
    cy = height // 2
    x = 0
    y = r

    while x <= y:
        px = x + cx
        py = y + cy
        for b in range(height):
            for a in range(width):
                if a == px and b == py:
                    dx = px
                    dy = py
                    pixels[dy * width + dx] = foreground
                    pixels[dx * width + dy] = foreground

                    pixels[(height - dy) * width + dx] = foreground
                    pixels[dx * width + (height - dy)] = foreground

                    pixels[dy * width + (width - dx)] = foreground
                    pixels[(width - dx) * width + dy] = foreground

                    pixels[(height - dy) * width + (width - dx)] = foreground
                    pixels[(width - dx) * width + (height - dy)] = foreground
        x += 1
        if x * x + y * y > r * r:
            y -= 1

    save_as_ppm(width, height, pixels, "hollow")


def circle(width, height, pixels, foreground, background):
    cx = width // 2
    cy = height // 2
    r = cx / 2
    for y in range(height):
        for x in range(width):
            if (
                (x + 0.5 - cx) * (x + 0.5 - cx)
                + (y + 0.5 - cy) * (y + 0.5 - cy)
            ) <= r * r:
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
    color = 0x000000
    pixels = [color] * width * height
    foreground = 0x634D84
    background = 0x000000
    hollow_circle(width, height, pixels, foreground)
    checker_pattern(pixels, width, height, width // 16, foreground, background)
    stripes_pattern(pixels, width, height, width // 16, foreground, background)
    wee_wee(width, height, pixels)
    wee_wee_with_head(width, height, pixels)
    four_dimensional(width, height, pixels)
    circle(width, height, pixels, foreground, background)


main()

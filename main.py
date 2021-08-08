def save_as_ppm(width, height, pixels: hex):
    with open("output.ppm", "w") as file:
        file.write(f"P3\n{width} {height} 255\n")
        for y in range(height):
            for x in range(width):
                pixel = pixels[y * width + x]
                color = (f'{pixel >> 8 * 2 & 0xFF} ', 
                         f'{pixel >> 8 * 1 & 0xFF} ', 
                         f'{pixel >> 8 * 0 & 0xFF}  ')
                file.writelines(color)


def main():
    WIDTH = 200
    HEIGHT = 200
    COLOR = 0xFF0000
    pixels = [COLOR] * (WIDTH * HEIGHT)
    save_as_ppm(WIDTH, HEIGHT, pixels)

main()

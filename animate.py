from PIL import Image, ImageDraw, ImageFont

START = (10, 13)
END = (10, 3)

PIXEL_SIZE = 40
SIZE = 20
INDEX_MAX = PIXEL_SIZE * SIZE
PIXEL_MAX = INDEX_MAX + PIXEL_SIZE * 2
MAX_SIZE = PIXEL_MAX + PIXEL_SIZE
OFFSET = PIXEL_SIZE
TEXT_OFFSET = OFFSET * 0.5

BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (252, 47, 20)
GREEN = (132, 252, 20)
BLUE = (36, 22, 240)
WHITE = (255, 255, 255)

FONT = ImageFont.truetype('res/Arial.ttf', 16)


def draw_pixel(graph_draw: ImageDraw, pos: tuple, color: tuple, swap: bool):
    if swap:
        graph_draw.rectangle([(pos[1], pos[0]), (pos[1] + PIXEL_SIZE, pos[0] + PIXEL_SIZE)], fill=color, outline=BLACK)
    else:
        graph_draw.rectangle([pos, (pos[0] + PIXEL_SIZE, pos[1] + PIXEL_SIZE)], fill=color, outline=BLACK)


def resize(px):
    return px * PIXEL_SIZE + OFFSET


def text_box(graph_draw: ImageDraw, text: str):
    graph_draw.rectangle((PIXEL_MAX + OFFSET, OFFSET, PIXEL_MAX + int(MAX_SIZE / 3), PIXEL_MAX), outline=BLACK,
                         fill=WHITE)

    graph_draw.text((PIXEL_MAX + OFFSET * 2, OFFSET * 2), text, font=FONT, fill=BLACK)


def plot_pixels(image: Image, graph_draw: ImageDraw, x1, y1, x2, y2, dx: int, dy: int, images: list, swap :bool):
    pk = 2 * dy - dx
    x_dir_flag = x1 < x2
    y_dir_flag = y1 < y2

    text = f'Current Co-ordinate:\n' \
           f'({x1}, {y1})\n' \
           f'Decision Parameter: -\n\n' \
           f'Co-ordinates:\n' \
           f'({x1}, {y1})'

    text_box(graph_draw, text)

    points = []

    for i in range(0, dx + 1):
        draw_pixel(graph_draw, (resize(x1), resize(y1)), BLUE, swap)
        points.append((x1, y1))

        text = f'Current Co-ordinate:\n' \
               f'({x1}, {y1})\n' \
               f'Decision Parameter: {pk}\n'

        text += f'It is negative.\n' \
                f'Red pixel will be plotted.\n\n' if pk < 0 else f'It is positive.\n' \
                                                                 f'Green pixel will be plotted.\n\n'

        text += f'Co-ordinates:\n'

        for point in points:
            text += f'{point}\n'

        text_box(graph_draw, text)

        images.append(image.copy())
        x1_old = x1
        y1_old = y1
        flag = False

        if x_dir_flag:
            x1 += 1
        else:
            x1 -= 1

        if pk < 0:
            pk = pk + 2 * dy
        else:
            flag = True
            if y_dir_flag:
                y1 += 1
            else:
                y1 -= 1
            pk = pk + 2 * dy - 2 * dx

        if i < dx:
            x_next = x1_old + 1 if x_dir_flag else x1_old - 1

            copy = image.copy()
            copy_draw = ImageDraw.Draw(copy)
            draw_pixel(copy_draw, (resize(x_next), resize(y1_old)), RED, swap)
            draw_pixel(copy_draw, (resize(x_next), resize(y1_old + 1 if y_dir_flag else y1_old - 1)), GREEN, swap)
            images.append(copy)

            copy = image.copy()
            copy_draw = ImageDraw.Draw(copy)

            if flag:
                draw_pixel(copy_draw, (resize(x_next), resize(y1_old + 1 if y_dir_flag else y1_old - 1)), GREEN, swap)
            else:
                draw_pixel(copy_draw, (resize(x_next), resize(y1_old)), RED, swap)

            images.append(copy)


def get_index_string(n):
    index = int(n / PIXEL_SIZE)
    index_string = str(index)

    if index < 10:
        index_string = f'  {index_string}'

    return index_string


def graph(graph_draw: ImageDraw):
    for y in range(0, PIXEL_MAX, PIXEL_SIZE):
        graph_draw.line([(OFFSET, y + OFFSET), (PIXEL_MAX, y + OFFSET)], fill=BLACK, width=0)

        if y <= INDEX_MAX:
            graph_draw.text((TEXT_OFFSET, y + OFFSET), get_index_string(y), font=FONT, fill=BLACK)

    for x in range(0, PIXEL_MAX, PIXEL_SIZE):
        graph_draw.line([(x + OFFSET, OFFSET), (x + OFFSET, PIXEL_MAX)], fill=BLACK, width=0)

        if x <= INDEX_MAX:
            graph_draw.text((x + OFFSET, TEXT_OFFSET), get_index_string(x), font=FONT, fill=BLACK)


def get_pos(pos):
    return resize(pos[0]) + PIXEL_SIZE * 0.5, resize(pos[1]) + PIXEL_SIZE * 0.5


def generate_animation(start: tuple, end: tuple, path: str):
    image = Image.new('RGB', (int(MAX_SIZE * 4 / 3), MAX_SIZE), 'white')
    image_draw = ImageDraw.Draw(image)

    graph(image_draw)

    text = f'Current Co-ordinate:\n' \
           f'(-, -)\n' \
           f'Decision Parameter: -'

    text_box(image_draw, text)
    image_draw.line([get_pos(start), get_pos(end)], fill=GRAY, width=3)

    dx = abs(end[0] - start[0])
    dy = abs(end[1] - start[1])

    images = [image.copy()]

    slope = 1 if dx == 0 else dy/dx

    if slope < 1:
        plot_pixels(image, image_draw, start[0], start[1], end[0], end[1], dx, dy, images, False)
    else:
        plot_pixels(image, image_draw, start[1], start[0], end[1], end[0], dy, dx, images, True)

    duration = len(images) * 32
    images[0].save(path, save_all=True, append_images=images[1:], optimize=False, duration=duration)


if __name__ == '__main__':
    generate_animation(START, END, 'out/anim.gif')

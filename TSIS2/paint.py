
import pygame
import math
from datetime import datetime

pygame.init()

# Window settings
WIDTH = 1100
HEIGHT = 760

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 180, 0)
YELLOW = (255, 220, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (80, 80, 80)

# Canvas settings
CANVAS_X = 20
CANVAS_Y = 120
CANVAS_WIDTH = 1060
CANVAS_HEIGHT = 620

canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

# Fonts
font = pygame.font.SysFont("Arial", 18)
text_font = pygame.font.SysFont("Arial", 25)

# Tools
tools = [
    "Pencil",
    "Line",
    "Rectangle",
    "Circle",
    "Square",
    "Eraser",
    "Right Triangle",
    "Equilateral Triangle",
    "Rhombus",
    "Fill",
    "Text",
    "Picker"
]

current_tool = "Pencil"
current_color = BLACK
brush_size = 5

colors = [BLACK, RED, BLUE, GREEN, YELLOW]

# Drawing variables
drawing = False
start_pos = None
last_pos = None
end_pos = None

# Text variables
text_active = False
text_input = ""
text_position = None

# Button settings
button_width = 100
button_height = 38


# Draw shapes
def draw_shape(surface, tool, start, end, color, size, offset=(0, 0)):

    x1, y1 = start
    x2, y2 = end

    ox, oy = offset

    x1 += ox
    y1 += oy
    x2 += ox
    y2 += oy

    if tool == "Line":
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), size)

    elif tool == "Rectangle":
        rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )
        pygame.draw.rect(surface, color, rect, size)

    elif tool == "Circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))

        if radius > 0:
            pygame.draw.circle(surface, color, (x1, y1), radius, size)

    elif tool == "Square":
        side = max(abs(x2 - x1), abs(y2 - y1))

        sign_x = 1 if x2 >= x1 else -1
        sign_y = 1 if y2 >= y1 else -1

        x2 = x1 + side * sign_x
        y2 = y1 + side * sign_y

        rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            side,
            side
        )

        pygame.draw.rect(surface, color, rect, size)

    elif tool == "Right Triangle":
        points = [
            (x1, y1),
            (x1, y2),
            (x2, y2)
        ]

        pygame.draw.polygon(surface, color, points, size)

    elif tool == "Equilateral Triangle":
        side = abs(x2 - x1)
        height = side * math.sqrt(3) / 2

        middle_x = (x1 + x2) // 2
        bottom_y = max(y1, y2)

        points = [
            (middle_x, int(bottom_y - height)),
            (min(x1, x2), bottom_y),
            (max(x1, x2), bottom_y)
        ]

        pygame.draw.polygon(surface, color, points, size)

    elif tool == "Rhombus":
        middle_x = (x1 + x2) // 2
        middle_y = (y1 + y2) // 2

        points = [
            (middle_x, y1),
            (x2, middle_y),
            (middle_x, y2),
            (x1, middle_y)
        ]

        pygame.draw.polygon(surface, color, points, size)


# Flood fill
def flood_fill(surface, position, new_color):

    x, y = position

    if x < 0 or x >= CANVAS_WIDTH:
        return

    if y < 0 or y >= CANVAS_HEIGHT:
        return

    old_color = surface.get_at((x, y))[:3]

    if old_color == new_color:
        return

    points = [(x, y)]

    while points:
        x, y = points.pop()

        if x < 0 or x >= CANVAS_WIDTH:
            continue

        if y < 0 or y >= CANVAS_HEIGHT:
            continue

        if surface.get_at((x, y))[:3] != old_color:
            continue

        surface.set_at((x, y), new_color)

        points.append((x + 1, y))
        points.append((x - 1, y))
        points.append((x, y + 1))
        points.append((x, y - 1))


# Draw toolbar
def draw_toolbar():

    screen.fill(GRAY)

    for i, tool in enumerate(tools):

        row = i // 6
        col = i % 6

        x = 20 + col * 105
        y = 10 + row * 48

        if current_tool == tool:
            button_color = (150, 180, 220)
        else:
            button_color = WHITE

        pygame.draw.rect(
            screen,
            button_color,
            (x, y, button_width, button_height)
        )

        pygame.draw.rect(
            screen,
            DARK_GRAY,
            (x, y, button_width, button_height),
            2
        )

        label = font.render(tool, True, BLACK)

        screen.blit(
            label,
            (x + 5, y + 10)
        )

    # Color palette
    color_label = font.render("Colors:", True, BLACK)
    screen.blit(color_label, (660, 15))

    for i, color in enumerate(colors):

        x = 735 + i * 55

        pygame.draw.rect(
            screen,
            color,
            (x, 12, 40, 30)
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (x, 12, 40, 30),
            2
        )

    # Brush size information
    size_text = font.render(
        "Brush: " + str(brush_size) + " px   (1 / 2 / 3)",
        True,
        BLACK
    )

    screen.blit(size_text, (660, 65))


# Main loop
running = True
clock = pygame.time.Clock()

while running:

    draw_toolbar()

    # Display canvas
    screen.blit(canvas, (CANVAS_X, CANVAS_Y))

    pygame.draw.rect(
        screen,
        BLACK,
        (CANVAS_X, CANVAS_Y, CANVAS_WIDTH, CANVAS_HEIGHT),
        2
    )

    for event in pygame.event.get():

        # Quit
        if event.type == pygame.QUIT:
            running = False

        # Mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            # Toolbar clicks
            if mouse_y < 110:

                if mouse_y < 48:
                    row = 0
                else:
                    row = 1

                col = (mouse_x - 20) // 105

                if 0 <= col < 6:
                    index = row * 6 + col

                    if 0 <= index < len(tools):
                        current_tool = tools[index]

                # Color selection
                if 735 <= mouse_x <= 1000 and mouse_y < 48:

                    for i, color in enumerate(colors):

                        x = 735 + i * 55

                        if x <= mouse_x <= x + 40:
                            current_color = color

            # Canvas clicks
            elif (
                CANVAS_X < mouse_x < CANVAS_X + CANVAS_WIDTH
                and CANVAS_Y < mouse_y < CANVAS_Y + CANVAS_HEIGHT
            ):

                x = mouse_x - CANVAS_X
                y = mouse_y - CANVAS_Y

                if current_tool == "Fill":

                    flood_fill(canvas, (x, y), current_color)

                elif current_tool == "Picker":

                    current_color = canvas.get_at((x, y))[:3]

                elif current_tool == "Text":

                    text_active = True
                    text_input = ""
                    text_position = (x, y)

                else:

                    drawing = True
                    start_pos = (x, y)
                    last_pos = (x, y)
                    end_pos = (x, y)

                    if current_tool == "Pencil":
                        pygame.draw.circle(
                            canvas,
                            current_color,
                            (x, y),
                            max(1, brush_size // 2)
                        )

                    elif current_tool == "Eraser":
                        pygame.draw.circle(
                            canvas,
                            WHITE,
                            (x, y),
                            max(1, brush_size // 2)
                        )

        # Mouse movement
        if event.type == pygame.MOUSEMOTION:

            if drawing:

                mouse_x, mouse_y = event.pos

                if (
                    CANVAS_X <= mouse_x < CANVAS_X + CANVAS_WIDTH
                    and CANVAS_Y <= mouse_y < CANVAS_Y + CANVAS_HEIGHT
                ):

                    x = mouse_x - CANVAS_X
                    y = mouse_y - CANVAS_Y

                    end_pos = (x, y)

                    if current_tool == "Pencil":

                        pygame.draw.line(
                            canvas,
                            current_color,
                            last_pos,
                            end_pos,
                            brush_size
                        )

                    elif current_tool == "Eraser":

                        pygame.draw.line(
                            canvas,
                            WHITE,
                            last_pos,
                            end_pos,
                            brush_size
                        )

                    last_pos = end_pos

        # Mouse button released
        if event.type == pygame.MOUSEBUTTONUP:

            if drawing:

                mouse_x, mouse_y = event.pos

                x = max(0, min(CANVAS_WIDTH - 1, mouse_x - CANVAS_X))
                y = max(0, min(CANVAS_HEIGHT - 1, mouse_y - CANVAS_Y))

                end_pos = (x, y)

                if current_tool not in ["Pencil", "Eraser"]:

                    draw_shape(
                        canvas,
                        current_tool,
                        start_pos,
                        end_pos,
                        current_color,
                        brush_size
                    )

                drawing = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN:

            # Save canvas with Ctrl + S
            if (
                event.key == pygame.K_s
                and pygame.key.get_mods() & pygame.KMOD_CTRL
            ):

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                filename = "paint_" + timestamp + ".png"

                pygame.image.save(canvas, filename)

                print("Canvas saved:", filename)

            # Brush sizes
            if event.key == pygame.K_1:
                brush_size = 2

            if event.key == pygame.K_2:
                brush_size = 5

            if event.key == pygame.K_3:
                brush_size = 10

            # Text tool
            if text_active:

                if event.key == pygame.K_RETURN:

                    text_surface = text_font.render(
                        text_input,
                        True,
                        current_color
                    )

                    canvas.blit(
                        text_surface,
                        text_position
                    )

                    text_active = False
                    text_input = ""

                elif event.key == pygame.K_ESCAPE:

                    text_active = False
                    text_input = ""

                elif event.key == pygame.K_BACKSPACE:

                    text_input = text_input[:-1]

                else:

                    if event.unicode.isprintable():
                        text_input += event.unicode

    # Live shape preview
    if drawing and current_tool not in ["Pencil", "Eraser"]:

        if end_pos is not None:

            draw_shape(
                screen,
                current_tool,
                start_pos,
                end_pos,
                current_color,
                brush_size,
                (CANVAS_X, CANVAS_Y)
            )

    # Text preview
    if text_active and text_position is not None:

        preview = text_font.render(
            text_input + "|",
            True,
            current_color
        )

        screen.blit(
            preview,
            (
                CANVAS_X + text_position[0],
                CANVAS_Y + text_position[1]
            )
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import arcade

import math

from pyglet.math import Vec2


def collides_with_point(rect: arcade.XYWH,
                        point: tuple[float | int, float | int] | Vec2,
                        angle: float = 0):
    position = Vec2(*point) if not isinstance(point, Vec2) else point
    local_x = position.x - rect.x
    local_y = position.y - rect.y

    angle_rad = math.radians(angle)
    rotated_x = local_x * math.cos(angle_rad) - local_y * math.sin(angle_rad)
    rotated_y = local_x * math.sin(angle_rad) + local_y * math.cos(angle_rad)

    return (
            -rect.width / 2 <= rotated_x <= rect.width / 2 and
            -rect.height / 2 <= rotated_y <= rect.height / 2
    )


def calculate_perspective_scale(y, rows, base_scale=0.8, perspective_factor=0.7):
    scale_reduction = (10 - rows) * 0.1
    normalized_y = y / (rows - 1) if rows > 1 else 0
    return base_scale - (base_scale - scale_reduction) * (normalized_y ** perspective_factor)


def hex_to_rgb(hex_str):
    if hex_str is None:
        return None
    return tuple(int(hex_str[i:i + 2], 16) for i in (1, 3, 5))


def calculate_bezier(points, t):
    n = len(points) - 1
    x, y = 0.0, 0.0

    for i, (px, py) in enumerate(points):
        coeff = bernstein_polynomial(n, i, t)
        x += px * coeff
        y += py * coeff

    return x, y


def bernstein_polynomial(n, i, t):
    return math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

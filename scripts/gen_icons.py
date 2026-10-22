import os
import struct
import zlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write_png(path: str, w: int, h: int, rgb: tuple[int, int, int]) -> None:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack('>I', len(data)) + tag + data + struct.pack(
            '>I', zlib.crc32(tag + data) & 0xffffffff
        )

    raw = b''
    r, g, b = rgb
    for y in range(h):
        raw += b'\x00'
        for x in range(w):
            cx, cy = w / 2, h / 2
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d < w * 0.38:
                raw += bytes([255, 255, 255])
            else:
                raw += bytes([r, g, b])
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    data = (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', ihdr)
        + chunk(b'IDAT', zlib.compress(raw, 9))
        + chunk(b'IEND', b'')
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)
    print('wrote', path)


def main() -> None:
    paths = [
        (os.path.join(BASE, 'entry', 'src', 'main', 'resources', 'base', 'media', 'startIcon.png'), 128, (47, 107, 255)),
        (os.path.join(BASE, 'entry', 'src', 'main', 'resources', 'base', 'media', 'foreground.png'), 128, (47, 107, 255)),
        (os.path.join(BASE, 'entry', 'src', 'main', 'resources', 'base', 'media', 'background.png'), 128, (242, 247, 255)),
        (os.path.join(BASE, 'AppScope', 'resources', 'base', 'media', 'app_icon.png'), 128, (47, 107, 255)),
    ]
    for path, size, color in paths:
        write_png(path, size, size, color)

    layered = os.path.join(BASE, 'entry', 'src', 'main', 'resources', 'base', 'media', 'layered_image.json')
    with open(layered, 'w', encoding='utf-8') as f:
        f.write(
            '{\n'
            '  "layered-image": {\n'
            '    "background": "$media:background",\n'
            '    "foreground": "$media:foreground"\n'
            '  }\n'
            '}\n'
        )
    print('wrote', layered)


if __name__ == '__main__':
    main()

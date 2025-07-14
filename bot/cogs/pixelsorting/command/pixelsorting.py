# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import colorsys
import itertools
import random
from io import BytesIO
from typing import List, Optional, Tuple, TYPE_CHECKING

from aiohttp_client_cache import CachedSession
from PIL import Image, ImageFilter, ImageOps
from PIL.ImageFile import ImageFile

from bot.ext import commands, Context
from bot.translations import Response

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class PixelSortCmd(commands.CustomComponent):
    def __init__(self, bot: Gorenmu) -> None:
        self.bot = bot

    cooldown_rate = 1
    cooldown_per = 10
    cooldown_key = commands.BucketType.user

    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None: ...

    @commands.Component.guard()
    def guards_component(self, ctx: commands.Context) -> bool:  # NOQA
        return True

    @commands.base_decorator("PixelSorting")
    @commands.command(name="pixelsorting", aliases=["pxs"])
    async def pixel_sorting(self, ctx: Context, *, args) -> Response:
        translations = ctx.user.translations.PixelSorting
        extract = ctx.bot.StringTools.extract_and_remove_all_fields
        rest, tipos = extract(args, "type", ["sum"])
        rest, crop = extract(rest, "crop")
        rest, is_random = extract(rest, "rand", ["false"])
        rest, intensity = extract(rest, "inte", ["50"])  # NOQA
        rest, direction = extract(rest, "dire", ["vertical"])
        rest, mask_mode = extract(rest, "maskmode", ["none"])  # NOQA
        rest, mask_image = extract(rest, "maskimage", ["none"])  # NOQA
        rest, mask_threshold = extract(rest, "maskthreshold", ["128"])  # NOQA
        urls = ctx.bot.StringTools.urls_extract(rest)
        if not urls:
            return translations.no_url.format_response(ctx, sucess=False)
        session = ctx.bot.SessionsCaches.PixelSortingCachedSession.session
        images = await request_images(urls=urls, session=session)
        if type(images) is str:
            return translations.invalid_content_type.format_response(ctx, sucess=False)
        if mask_image != "none":
            url = ctx.bot.StringTools.urls_extract(mask_image[0])
            mask_image = await request_images(urls=url, session=session) if url else images
        timeout = ctx.bot.TimeTools.Timeout(300)
        try:
            async with timeout:
                manipulated = await manipulate(
                    images=images,
                    tipos=tipos,
                    intensity=int(intensity[0]),
                    direction=direction[0],
                    crop=crop,
                    rand=is_random[0],
                    mask_mode=mask_mode[0],
                    mask_image=mask_image[0],
                    mask_threshold=int(mask_threshold[0]),
                )
        except timeout.error:
            return translations.took_too_long.format_response(ctx, timeout.timeout, sucess=False)
        if isinstance(manipulated, Response):
            return manipulated
        upload = await ctx.bot.UploadThings.upload_file(
            manipulated.getvalue(), "image/png", session=session, filename="manipulated.png"
        )
        shortened = await ctx.bot.UploadThings.shortener(url=upload, session=session, tags=["Gorenmu", "PixelSorting"])
        return translations.image.format_response(ctx, shortened)


async def setup(bot: Gorenmu) -> None:
    await bot.add_component(PixelSortCmd(bot))


async def teardown(bot: Gorenmu) -> None: ...  # NOQA


async def request_images(urls: str, session: CachedSession) -> List[ImageFile] | str:
    images = []
    max_width = 1920
    max_height = 1080
    for url in urls:
        response = await session.get(url)
        if not response.content_type.startswith("image/") and len(urls) == 1:
            return response.content_type
        elif response.content_type.startswith("image/"):
            img = Image.open(BytesIO(await response.read())).convert("RGBA")
            w, h = img.size
            if w > max_width or h > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            images.append(img)
    return images or "error"


async def manipulate(
    images: List[ImageFile],
    tipos: List[str],
    intensity: int,
    direction: str = "global",
    crop: list[str] = None,
    rand: str = None,
    mask_mode: str = None,  # 'none' | 'external' | 'internal'
    mask_image: Optional[Image.Image] = None,
    mask_threshold: int = 128,
) -> BytesIO | Response:
    positions = None
    manipulated_amount = 0
    manipulated = images
    buffer = BytesIO()
    types = [
        "red",
        "green",
        "blue",
        "sum",
        "rgb",
        "rgba",
        "hue",
        "saturation",
        "value",
        "lightness",
        "luma",
        "chroma",
        "dist_white",
        "dist_black",
        "random",
    ]

    if crop:
        manipulated, positions = await cut(images=manipulated, size=crop[0])
    if mask_mode == "external" and not mask_image:
        mask_image = images[0]

    rand = rand != "false"
    for tipo in tipos:
        if tipo.lower() in types:
            manipulated = await sorting(
                images=manipulated,
                mode=tipo.lower(),
                rand=rand,
                direction=direction,
                intensity=intensity,
                mask_mode=mask_mode,
                mask_image=mask_image,
                mask_threshold=mask_threshold,
            )
            manipulated_amount += 1
            await asyncio.sleep(0)
    if crop:
        reconstructed = [Image.new(img.mode, img.size) for img in images]
        for tile, (img_idx, x, y) in zip(manipulated, positions):
            reconstructed[img_idx].paste(tile, (x, y))
        reconstructed[0].save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    manipulated[0].save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


async def cut(images: List[ImageFile], size: str) -> Tuple[List[ImageFile], List[Tuple[int, int, int]]]:
    tiles: List[ImageFile] = []
    positions: List[Tuple[int, int, int]] = []

    for img_idx, image in enumerate(images):
        w_step, h_step = size.split("px:")
        w = max(50, int(w_step.replace("px", "")))
        h = max(50, int(h_step.replace("px", "")))
        img_w, img_h = image.size

        for x, y in itertools.product(range(0, img_w, w), range(0, img_h, h)):
            right = min(x + w, img_w)
            bottom = min(y + h, img_h)

            chunk = image.crop((x, y, right, bottom))
            tiles.append(chunk)
            positions.append((img_idx, x, y))

    return tiles, positions


async def sorting(
    images: List[ImageFile],
    mode: str,
    rand: bool,
    direction: str,
    intensity: int,
    mask_mode: str | None,
    mask_image: Optional[Image],
    mask_threshold: int,
) -> List[ImageFile]:
    result = []
    for image in images:
        img_rgba = image.convert("RGBA")
        w, h = img_rgba.size
        flat_pixels = list(img_rgba.getdata())  # NOQA

        if mask_mode == "external":
            mask = mask_image.convert("L").resize((w, h))
        elif mask_mode == "internal":
            gray = img_rgba.convert("L")
            edges = gray.filter(ImageFilter.FIND_EDGES)
            mask = ImageOps.equalize(edges)
        else:
            mask = Image.new("L", (w, h), 255)

        mask_data = list(mask.getdata())  # NOQA

        def should_sort(i: int) -> bool:
            return mask_data[i] >= mask_threshold

        async def random_segment_sort(seq, idxs):  # NOQA
            if random.randint(0, 100) <= intensity:
                return seq
            to_sort = [(seq[i], i) for i in idxs if should_sort(i)]  # NOQA
            if not to_sort:
                return seq
            pixels_only, positions = zip(*to_sort)  # NOQA
            sorted_pixels = await quick_sort(list(pixels_only), mode=mode)  # NOQA
            seq = list(seq)  # NOQA
            for pos, px in zip(positions, sorted_pixels):  # NOQA
                seq[pos] = px
            return seq

        sorted_img = Image.new("RGBA", (w, h))
        if not rand:
            if direction == "global":
                idxs = list(range(w * h))  # NOQA
                to_sort = [(flat_pixels[i], i) for i in idxs if should_sort(i)]
                pixels_only, positions = zip(*to_sort) if to_sort else ([], [])
                sorted_pixels = await quick_sort(list(pixels_only), mode) if pixels_only else []
                new_flat = flat_pixels[:]
                for pos, px in zip(positions, sorted_pixels):
                    new_flat[pos] = px
                sorted_img.putdata(new_flat)

            elif direction == "horizontal":
                rows = [flat_pixels[i * w : (i + 1) * w] for i in range(h)]
                tasks = []
                for row_i, row in enumerate(rows):
                    await asyncio.sleep(0)
                    base = row_i * w

                    to_sort = [(row[j], j) for j in range(w) if should_sort(base + j)]
                    pixels_only, rel_positions = zip(*to_sort) if to_sort else ([], ())

                    async def sort_row(pixels, rel_pos, original_row):
                        await asyncio.sleep(0)
                        sorted_p = await quick_sort(list(pixels), mode) if pixels else []
                        new_row = list(original_row)
                        for rel_idx, px in zip(rel_pos, sorted_p):  # NOQA
                            new_row[rel_idx] = px
                        return new_row

                    tasks.append(sort_row(pixels_only, rel_positions, row))

                sorted_rows = await asyncio.gather(*tasks)
                sorted_img.putdata([px for row in sorted_rows for px in row])

            else:  # vertical
                rows = [flat_pixels[i * w : (i + 1) * w] for i in range(h)]
                cols = list(zip(*rows))
                tasks = []
                for col_j, col in enumerate(cols):
                    await asyncio.sleep(0)
                    idxs = [r * w + col_j for r in range(h)]  # NOQA
                    to_sort = [(col[r], idxs[r]) for r in range(h) if should_sort(idxs[r])]
                    pixels_only, positions = zip(*to_sort) if to_sort else ([], [])

                    async def sort_col(pixels, pos):  # NOQA
                        await asyncio.sleep(0)
                        sorted_p = await quick_sort(list(pixels), mode) if pixels else []
                        new_col = list(col)
                        for p, px in zip(pos, sorted_p):  # NOQA
                            new_col[p // w] = px
                        return new_col

                    tasks.append(sort_col(pixels_only, positions))
                sorted_cols = await asyncio.gather(*tasks)
                transposed = list(zip(*sorted_cols))
                sorted_img.putdata([px for row in transposed for px in row])

        else:
            if mask_mode == "external":
                mask = mask_image.convert("L").resize((w, h))
            elif mask_mode == "internal":
                gray = img_rgba.convert("L")
                edges = gray.filter(ImageFilter.FIND_EDGES)
                mask = ImageOps.equalize(edges)
            else:
                mask = Image.new("L", (w, h), 255)
            mask_data = list(mask.getdata())  # NOQA

            def should_sort(i: int) -> bool:
                return mask_data[i] >= mask_threshold

            if direction == "global":
                seq = flat_pixels
                idxs = list(range(w * h))  # NOQA
                new_flat = await random_segment_sort(seq, idxs)
                sorted_img.putdata(new_flat)

            elif direction == "horizontal":
                rows = [flat_pixels[i * w : (i + 1) * w] for i in range(h)]
                tasks = []

                for row_i, row in enumerate(rows):
                    base = row_i * w

                    async def process_row(row=row):  # NOQA
                        # aplica intensidade e filtro de máscara
                        if random.randint(0, 100) > intensity:
                            return row

                        start = random.randint(0, w - 3)
                        end = random.randint(start + 1, w - 1)
                        to_sort = [(row[x], x) for x in range(start, end) if should_sort(base + x)]  # NOQA

                        if not to_sort:
                            return row

                        pixels_only, rel_xs = zip(*to_sort)  # NOQA
                        sorted_seg = await quick_sort(list(pixels_only), mode="sum")

                        new_row = list(row)
                        for rel_x, px in zip(rel_xs, sorted_seg):  # NOQA
                            new_row[rel_x] = px
                        return new_row

                    tasks.append(process_row())

                sorted_rows = await asyncio.gather(*tasks)
                sorted_img.putdata([px for row in sorted_rows for px in row])

            else:  # vertical
                rows = [flat_pixels[i * w : (i + 1) * w] for i in range(h)]
                cols = list(zip(*rows))
                tasks = []

                for col_j, col in enumerate(cols):
                    idxs = [r * w + col_j for r in range(h)]

                    async def process_col(col=col, idxs=idxs):  # NOQA
                        if random.randint(0, 100) > intensity:
                            return col

                        start = random.randint(0, h - 3)
                        end = random.randint(start + 1, h - 1)
                        to_sort = [(col[y], y) for y in range(start, end) if should_sort(idxs[y])]  # NOQA

                        if not to_sort:
                            return col

                        pixels_only, rel_ys = zip(*to_sort)  # NOQA
                        sorted_seg = await quick_sort(list(pixels_only), mode="sum")

                        new_col = list(col)
                        for rel_y, px in zip(rel_ys, sorted_seg):  # NOQA
                            new_col[rel_y] = px
                        return new_col

                    tasks.append(process_col())

                sorted_cols = await asyncio.gather(*tasks)
                transposed = list(zip(*sorted_cols))
                sorted_img.putdata([px for row in transposed for px in row])

        result.append(sorted_img)
    return result


async def quick_sort(pixels, mode="RGB"):
    key_funcs = {
        "red": lambda p: p[0],
        "green": lambda p: p[1],
        "blue": lambda p: p[2],
        "alpha": lambda p: p[3] if len(p) > 3 else 0,
        "rgb": lambda p: p[0] + p[1] + p[2],
        "rgba": lambda p: p[0] + p[1] + p[2] + (p[3] if len(p) > 3 else 0),
        "sum": lambda p: p[0] + p[1] + p[2] + (p[3] if len(p) > 3 else 0),
        "hue": lambda p: colorsys.rgb_to_hsv(*[v / 255 for v in p[:3]])[0],
        "saturation": lambda p: colorsys.rgb_to_hsv(*[v / 255 for v in p[:3]])[1],
        "value": lambda p: colorsys.rgb_to_hsv(*[v / 255 for v in p[:3]])[2],
        "lightness": lambda p: colorsys.rgb_to_hls(*[v / 255 for v in p[:3]])[1],
        "luma": lambda p: 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2],
        "chroma": lambda p: max(p[:3]) - min(p[:3]),
        "dist_white": lambda p: sum((255 - v) ** 2 for v in p[:3]) ** 0.5,
        "dist_black": lambda p: (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** 0.5,
    }
    await asyncio.sleep(0)
    key = key_funcs[mode]
    pixels.sort(key=key)
    return pixels


async def random_sort_pixels(
    images: List[Image.Image],
    intensity: int,
    mask_image: Image.Image,
    mask_mode: str = "external",  # 'external' | 'internal' | 'none'
    mask_threshold: int = 128,  # 0–255
) -> List[Image.Image]:
    intensity = max(0, min(intensity, 100))

    def build_mask(img, mode):  # NOQA
        w, h = img.size  # NOQA
        if mode == "external":
            m = mask_image.convert("L").resize((w, h))
        elif mode == "internal":
            gray = img.convert("L")
            edges = gray.filter(ImageFilter.FIND_EDGES)
            m = ImageOps.equalize(edges)
        else:  # 'none'
            m = Image.new("L", (w, h), 255)
        return list(m.getdata())  # NOQA

    result = []
    for img in images:
        img_rgba = img.convert("RGBA")
        w, h = img_rgba.size
        pixels = img_rgba.load()

        mask_data = build_mask(img_rgba, mask_mode)

        sorted_img = Image.new("RGBA", (w, h))
        sorted_pixels = sorted_img.load()
        line_tasks = []

        for y in range(h):
            await asyncio.sleep(0)
            if random.randint(0, 100) > intensity:

                async def copy_line(y=y):  # NOQA
                    return [pixels[x, y] for x in range(w)]  # NOQA

                line_tasks.append(copy_line())
                continue

            start = random.randint(0, w - 3)
            end = random.randint(start + 1, w - 1)  # NOQA

            to_sort = []
            for x in range(start, end):
                idx = y * w + x
                if mask_data[idx] >= mask_threshold:
                    to_sort.append((pixels[x, y], x))

            if not to_sort:

                async def copy_line_nosort(y=y):  # NOQA
                    return [pixels[x, y] for x in range(w)]  # NOQA

                line_tasks.append(copy_line_nosort())
                continue

            pixels_only, xs = zip(*to_sort)

            async def sort_and_rebuild(pixels_list, xs, y=y):  # NOQA
                sorted_seg = await quick_sort(list(pixels_list), mode="sum")
                new_line = []
                seg_i = 0
                for x in range(w):  # NOQA
                    if x in xs:
                        new_line.append(sorted_seg[seg_i])
                        seg_i += 1
                    else:
                        new_line.append(pixels[x, y])
                return new_line

            line_tasks.append(sort_and_rebuild(pixels_only, xs))

        sorted_rows = await asyncio.gather(*line_tasks)
        for y, row in enumerate(sorted_rows):
            for x, px in enumerate(row):
                await asyncio.sleep(0)
                sorted_pixels[x, y] = px

        result.append(sorted_img)

    return result

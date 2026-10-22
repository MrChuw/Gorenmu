import asyncio
import random
from collections.abc import Callable
from io import BytesIO
from typing import TYPE_CHECKING

import numpy as np
import numpy.typing as npt
from aiohttp_client_cache import CachedSession
from PIL import Image, ImageFilter, ImageOps

from bot.ext import Context, Response, commands
from bot.utils import SessionsCaches, StringTools, TimeTools, UploadThings

from .translations import Translations

if TYPE_CHECKING:
    from bot.bot import Gorenmu


class PixelSortCmd(commands.CustomComponent):
    def __init__(self, bot: "Gorenmu") -> None:
        self.bot = bot
        self.translations: Translations = Translations(bot, self)
        self.StringTools: StringTools = StringTools()
        self.SessionsCaches: SessionsCaches = SessionsCaches(bot)
        self.UploadThings: UploadThings = UploadThings(bot)
        self.TimeTools: TimeTools = TimeTools()

    @commands.command(name="pixelsorting", aliases=["pxs"])
    async def pixel_sorting(self, ctx: Context, *, args: str) -> Response:  # NOQA
        translations = self.translations.PixelSorting
        extract = self.StringTools.extract_and_remove_all_fields

        rest, tipos        = extract(args,  "type",          ["sum"])
        rest, crop         = extract(rest,  "crop")
        rest, is_random    = extract(rest,  "rand",          ["false"])
        rest, intensity    = extract(rest,  "inte",          ["50"])  # NOQA
        rest, direction    = extract(rest,  "dire",          ["vertical"])
        rest, mask_mode    = extract(rest,  "maskmode",      ["none"])  # NOQA
        rest, mask_image_arg = extract(rest, "maskimage",    ["none"])  # NOQA
        rest, mask_threshold = extract(rest, "maskthreshold", ["128"])  # NOQA

        urls = self.StringTools.urls_extract(rest)
        if not urls:
            return translations.no_url()

        session: CachedSession = self.SessionsCaches.PixelSorting.session
        images = await request_images(urls=urls, session=session)
        if isinstance(images, str):
            return translations.invalid_content_type()

        resolved_mask_image: Image.Image | None = None
        if mask_image_arg[0] != "none":
            url = self.StringTools.urls_extract(mask_image_arg[0])
            mask_res = await request_images(urls=url, session=session) if url else images
            if isinstance(mask_res, str):
                return translations.invalid_content_type()
            if isinstance(mask_res, list) and len(mask_res) > 0:
                resolved_mask_image = mask_res[0]

        timeout = self.TimeTools.Timeout.timeout(300)
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
                    mask_image=resolved_mask_image,
                    mask_threshold=int(mask_threshold[0]),
                )
        except timeout.error:
            return translations.took_too_long(timeout.duration() or 0)

        if isinstance(manipulated, Response):
            return manipulated
        if ctx.bot.mock:
            return manipulated.getvalue()  # ty: ignore[invalid-return-type] # noqa just for testing purposes.
        upload = await self.UploadThings.upload_file(
            manipulated.getvalue(),
            "image/png",
            session=session,
            filename="manipulated.png",
            url=self.bot.config.ApisConfig.feridinha_url.human_repr(),
            api_key={"token": self.bot.config.ApisConfig.feridinha_key},
        )
        shortened = await self.UploadThings.shortener(url=upload, session=session, tags=["PixelSorting"])
        if shortened:
            return translations.image(shortened)
        return translations.upload_error()


async def setup(bot: "Gorenmu") -> None:
    await bot.add_component(PixelSortCmd(bot))


async def teardown(bot: "Gorenmu") -> None: ...  # NOQA


# ---------------------------------------------------------------------------
# Image fetching
# ---------------------------------------------------------------------------

RGBA_Array = npt.NDArray[np.uint8]   # shape (H, W, 4)
Mask_Array = npt.NDArray[np.bool_]   # shape (H, W)

# Sorting-key functions receive a (N, 4) uint8 array and return a (N,) float64
KeyFn = Callable[[RGBA_Array], npt.NDArray[np.float64]]

# ---------------------------------------------------------------------------
# Key-function table (operates on 2-D slices of shape (N, 4))
# ---------------------------------------------------------------------------

def _key_red(p: RGBA_Array) -> npt.NDArray[np.float64]:
    return p[:, 0].astype(np.float64)

def _key_green(p: RGBA_Array) -> npt.NDArray[np.float64]:
    return p[:, 1].astype(np.float64)

def _key_blue(p: RGBA_Array) -> npt.NDArray[np.float64]:
    return p[:, 2].astype(np.float64)

def _key_rgb(p: RGBA_Array) -> npt.NDArray[np.float64]:
    return p[:, :3].astype(np.float64).sum(axis=1)

def _key_rgba(p: RGBA_Array) -> npt.NDArray[np.float64]:
    return p.astype(np.float64).sum(axis=1)

_key_sum = _key_rgba  # alias kept for the "sum" mode

def _key_hue(p: RGBA_Array) -> npt.NDArray[np.float64]:
    rgb = p[:, :3].astype(np.float64) / 255.0
    cmax = rgb.max(axis=1)
    cmin = rgb.min(axis=1)
    delta = cmax - cmin
    h = np.zeros(len(p), dtype=np.float64)
    m = delta != 0
    r, g, b = rgb[:, 0], rgb[:, 1], rgb[:, 2]
    # red max
    mr = m & (cmax == r)
    h[mr] = ((g[mr] - b[mr]) / delta[mr]) % 6
    # green max
    mg = m & (cmax == g)
    h[mg] = (b[mg] - r[mg]) / delta[mg] + 2
    # blue max
    mb = m & (cmax == b)
    h[mb] = (r[mb] - g[mb]) / delta[mb] + 4
    return h / 6.0

def _key_saturation(p: RGBA_Array) -> npt.NDArray[np.float64]:
    rgb = p[:, :3].astype(np.float64) / 255.0
    cmax = rgb.max(axis=1)
    cmin = rgb.min(axis=1)
    delta = cmax - cmin
    s = np.where(cmax != 0, delta / cmax, 0.0)
    return s

def _key_value(p: RGBA_Array) -> npt.NDArray[np.float64]:
    return p[:, :3].astype(np.float64).max(axis=1) / 255.0

def _key_lightness(p: RGBA_Array) -> npt.NDArray[np.float64]:
    rgb = p[:, :3].astype(np.float64) / 255.0
    return (rgb.max(axis=1) + rgb.min(axis=1)) / 2.0

def _key_luma(p: RGBA_Array) -> npt.NDArray[np.float64]:
    rgb = p[:, :3].astype(np.float64)
    return 0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2]

def _key_chroma(p: RGBA_Array) -> npt.NDArray[np.float64]:
    rgb = p[:, :3].astype(np.float64)
    return rgb.max(axis=1) - rgb.min(axis=1)

def _key_dist_white(p: RGBA_Array) -> npt.NDArray[np.float64]:
    diff = (255 - p[:, :3]).astype(np.float64)
    return np.sqrt((diff ** 2).sum(axis=1))

def _key_dist_black(p: RGBA_Array) -> npt.NDArray[np.float64]:
    rgb = p[:, :3].astype(np.float64)
    return np.sqrt((rgb ** 2).sum(axis=1))

def _key_random(p: RGBA_Array) -> npt.NDArray[np.float64]:
    return np.random.rand(len(p))

_KEY_FN: dict[str, KeyFn] = {
    "red":        _key_red,
    "green":      _key_green,
    "blue":       _key_blue,
    "rgb":        _key_rgb,
    "rgba":       _key_rgba,
    "sum":        _key_sum,
    "hue":        _key_hue,
    "saturation": _key_saturation,
    "value":      _key_value,
    "lightness":  _key_lightness,
    "luma":       _key_luma,
    "chroma":     _key_chroma,
    "dist_white": _key_dist_white,
    "dist_black": _key_dist_black,
    "random":     _key_random,
}

_VALID_TYPES: frozenset[str] = frozenset(_KEY_FN)


async def request_images(
    urls: list[str],
    session: CachedSession,
) -> list[Image.Image] | str:
    images: list[Image.Image] = []
    max_width = 1920
    max_height = 1080

    for url in urls:
        async with session.get(url) as response:
            content_type: str = response.content_type or ""
            if not content_type.startswith("image/"):
                if len(urls) == 1:
                    return content_type
                continue
            content = await response.read()
            img = Image.open(BytesIO(content)).convert("RGBA")
            w, h = img.size
            if w > max_width or h > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            images.append(img)

    return images


# ---------------------------------------------------------------------------
# Tile-cutting helper
# ---------------------------------------------------------------------------

async def cut(
    images: list[Image.Image],
    size: str,
) -> tuple[list[Image.Image], list[tuple[int, int, int]]]:
    import itertools

    tiles: list[Image.Image] = []
    positions: list[tuple[int, int, int]] = []

    w_step, h_step = size.split("px:")
    w = max(50, int(w_step.replace("px", "")))
    h = max(50, int(h_step.replace("px", "")))

    for img_idx, image in enumerate(images):
        img_w, img_h = image.size
        for x, y in itertools.product(range(0, img_w, w), range(0, img_h, h)):
            right  = min(x + w, img_w)
            bottom = min(y + h, img_h)
            tiles.append(image.crop((x, y, right, bottom)))
            positions.append((img_idx, x, y))

    return tiles, positions


# ---------------------------------------------------------------------------
# Mask builder
# ---------------------------------------------------------------------------

def _build_mask(
    img_rgba: Image.Image,
    mask_mode: str | None,
    mask_image: Image.Image | None,
    mask_threshold: int,
) -> Mask_Array:
    """Return a boolean (H, W) array – True where pixels should be sorted."""
    w, h = img_rgba.size
    if mask_mode == "external" and mask_image:
        m = mask_image.convert("L").resize((w, h))
    elif mask_mode == "internal":
        gray  = img_rgba.convert("L")
        edges = gray.filter(ImageFilter.FIND_EDGES)
        m     = ImageOps.equalize(edges)
    else:
        return np.ones((h, w), dtype=np.bool_)

    return np.asarray(m, dtype=np.uint8) >= mask_threshold


# ---------------------------------------------------------------------------
# Core sorting  (fully vectorised – no per-pixel Python loops)
# ---------------------------------------------------------------------------

def _sort_arr_by_mask(
    arr: RGBA_Array,
    mask: Mask_Array,
    key_fn: KeyFn,
) -> RGBA_Array:
    """Sort *all* unmasked pixels globally by key, return a new array."""
    out   = arr.copy()
    flat  = arr.reshape(-1, 4)
    m_flat = mask.ravel()
    idxs  = np.where(m_flat)[0]
    if idxs.size == 0:
        return out
    pixels = flat[idxs]                         # (N, 4)
    order  = np.argsort(key_fn(pixels), kind="stable")
    flat_out = out.reshape(-1, 4)
    flat_out[idxs] = pixels[order]
    return out


def _sort_rows(
    arr: RGBA_Array,
    mask: Mask_Array,
    key_fn: KeyFn,
) -> RGBA_Array:
    """Sort each row's unmasked pixels, preserving their column positions."""
    out = arr.copy()
    h, w = arr.shape[:2]
    for r in range(h):
        m_row  = mask[r]                        # (W,)
        idxs   = np.where(m_row)[0]
        if idxs.size == 0:
            continue
        pixels = arr[r, idxs]                   # (N, 4)
        order  = np.argsort(key_fn(pixels), kind="stable")
        out[r, idxs] = pixels[order]
    return out


def _sort_cols(
    arr: RGBA_Array,
    mask: Mask_Array,
    key_fn: KeyFn,
) -> RGBA_Array:
    """Sort each column's unmasked pixels, preserving their row positions."""
    out = arr.copy()
    h, w = arr.shape[:2]
    for c in range(w):
        m_col  = mask[:, c]                     # (H,)
        idxs   = np.where(m_col)[0]
        if idxs.size == 0:
            continue
        pixels = arr[idxs, c]                   # (N, 4)
        order  = np.argsort(key_fn(pixels), kind="stable")
        out[idxs, c] = pixels[order]
    return out


# Random-segment variants ---------------------------------------------------

def _rand_sort_rows(
    arr: RGBA_Array,
    mask: Mask_Array,
    key_fn: KeyFn,
    intensity: int,
) -> RGBA_Array:
    out = arr.copy()
    h, w = arr.shape[:2]
    for r in range(h):
        if random.randint(0, 100) > intensity:
            continue
        start = random.randint(0, max(0, w - 3))
        end   = random.randint(start + 1, max(start + 1, w - 1))
        seg   = np.arange(start, end)
        m_seg = mask[r, seg]
        idxs  = seg[m_seg]
        if idxs.size == 0:
            continue
        pixels = arr[r, idxs]
        order  = np.argsort(key_fn(pixels), kind="stable")
        out[r, idxs] = pixels[order]
    return out


def _rand_sort_cols(
    arr: RGBA_Array,
    mask: Mask_Array,
    key_fn: KeyFn,
    intensity: int,
) -> RGBA_Array:
    out = arr.copy()
    h, w = arr.shape[:2]
    for c in range(w):
        if random.randint(0, 100) > intensity:
            continue
        start = random.randint(0, max(0, h - 3))
        end   = random.randint(start + 1, max(start + 1, h - 1))
        seg   = np.arange(start, end)
        m_seg = mask[seg, c]
        idxs  = seg[m_seg]
        if idxs.size == 0:
            continue
        pixels = arr[idxs, c]
        order  = np.argsort(key_fn(pixels), kind="stable")
        out[idxs, c] = pixels[order]
    return out


def _rand_sort_global(
    arr: RGBA_Array,
    mask: Mask_Array,
    key_fn: KeyFn,
    intensity: int,
) -> RGBA_Array:
    if random.randint(0, 100) > intensity:
        return arr.copy()
    return _sort_arr_by_mask(arr, mask, key_fn)


# ---------------------------------------------------------------------------
# sorting()  – async wrapper so the event loop stays yieldy between images
# ---------------------------------------------------------------------------

async def sorting(
    images: list[Image.Image],
    mode: str,
    rand: bool,
    direction: str,
    intensity: int,
    mask_mode: str | None,
    mask_image: Image.Image | None,
    mask_threshold: int,
) -> list[Image.Image]:
    key_fn: KeyFn = _KEY_FN.get(mode, _key_sum)
    result: list[Image.Image] = []

    for image in images:
        await asyncio.sleep(0)                  # yield between images

        img_rgba = image.convert("RGBA")
        arr: RGBA_Array = np.asarray(img_rgba, dtype=np.uint8).copy()
        mask = _build_mask(img_rgba, mask_mode, mask_image, mask_threshold)

        if rand:
            if direction == "global":
                out = _rand_sort_global(arr, mask, key_fn, intensity)
            elif direction == "horizontal":
                out = _rand_sort_rows(arr, mask, key_fn, intensity)
            else:  # vertical
                out = _rand_sort_cols(arr, mask, key_fn, intensity)
        else:
            if direction == "global":
                out = _sort_arr_by_mask(arr, mask, key_fn)
            elif direction == "horizontal":
                out = _sort_rows(arr, mask, key_fn)
            else:  # vertical
                out = _sort_cols(arr, mask, key_fn)

        result.append(Image.fromarray(out, "RGBA"))

    return result


# ---------------------------------------------------------------------------
# manipulate()
# ---------------------------------------------------------------------------

async def manipulate(
    images: list[Image.Image],
    tipos: list[str],
    intensity: int,
    direction: str = "global",
    crop: list[str] | None = None,
    rand: str | None = None,
    mask_mode: str | None = None,
    mask_image: Image.Image | None = None,
    mask_threshold: int = 128,
) -> BytesIO | Response:
    positions: list[tuple[int, int, int]] = []
    manipulated: list[Image.Image] = images

    if crop:
        manipulated, positions = await cut(images=manipulated, size=crop[0])
    if mask_mode == "external" and not mask_image:
        mask_image = images[0]

    is_rand = rand != "false"
    for tipo in tipos:
        if tipo.lower() in _VALID_TYPES:
            manipulated = await sorting(
                images=manipulated,
                mode=tipo.lower(),
                rand=is_rand,
                direction=direction,
                intensity=intensity,
                mask_mode=mask_mode,
                mask_image=mask_image,
                mask_threshold=mask_threshold,
            )

    buffer = BytesIO()
    if crop:
        reconstructed = [Image.new(img.mode, img.size) for img in images]
        for tile, (img_idx, x, y) in zip(manipulated, positions, strict=False):
            reconstructed[img_idx].paste(tile, (x, y))
        reconstructed[0].save(buffer, format="PNG")
    else:
        manipulated[0].save(buffer, format="PNG")

    buffer.seek(0)
    return buffer

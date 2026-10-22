from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Command used to make basic pixel sorting in images.",
            "To use: +pxs (url or shortened direct link)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Comando usado para aplicar pixel sorting básico em imagens.",
            "Como usar: +pxs (url ou link direto encurtado)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    only_link: ClassVar[list] = [
        pytest.param("en", "test_normal_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_normal_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_normal: ClassVar[list] = [
        pytest.param("en", "test_normal_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_normal_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_red: ClassVar[list] = [
        pytest.param("en", "test_red_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_red_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_green: ClassVar[list] = [
        pytest.param("en", "test_green_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_green_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_blue: ClassVar[list] = [
        pytest.param("en", "test_blue_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_blue_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_rgb: ClassVar[list] = [
        pytest.param("en", "test_type_rgb_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_rgb_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_rgba: ClassVar[list] = [
        pytest.param("en", "test_type_rgba_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_rgba_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_sum: ClassVar[list] = [
        pytest.param("en", "test_type_sum_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_sum_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_hue: ClassVar[list] = [
        pytest.param("en", "test_type_hue_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_hue_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_saturation: ClassVar[list] = [
        pytest.param("en", "test_type_saturation_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_saturation_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_value: ClassVar[list] = [
        pytest.param("en", "test_type_value_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_value_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_lightness: ClassVar[list] = [
        pytest.param("en", "test_type_lightness_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_lightness_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_luma: ClassVar[list] = [
        pytest.param("en", "test_type_luma_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_luma_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_chroma: ClassVar[list] = [
        pytest.param("en", "test_type_chroma_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_chroma_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_dist_white: ClassVar[list] = [
        pytest.param("en", "test_type_dist_white_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_dist_white_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_dist_black: ClassVar[list] = [
        pytest.param("en", "test_type_dist_black_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_dist_black_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_type_random: ClassVar[list] = [
        pytest.param("en", "test_type_random_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_type_random_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    # --- Parâmetros de Aleatoriedade ---
    only_rand_true: ClassVar[list] = [
        pytest.param("en", "test_rand_true_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_rand_true_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    # --- Parâmetros por Direção ---
    only_dire_global: ClassVar[list] = [
        pytest.param("en", "test_dire_global_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_dire_global_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_dire_horizontal: ClassVar[list] = [
        pytest.param("en", "test_dire_horizontal_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_dire_horizontal_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    only_dire_vertical: ClassVar[list] = [
        pytest.param("en", "test_dire_vertical_result.png", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "test_dire_vertical_result.png", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]


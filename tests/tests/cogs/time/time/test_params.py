from collections.abc import Iterable
from typing import ClassVar

import pytest

from bot.utils.timelength import English, Portuguese


def lang_params_date(
    *, expected_en: str, expected_pt: str, content: str, case_id: str, unit: list[str] | None = None
) -> Iterable:
    yield pytest.param(
        "en", expected_en, f"{content} {unit[0]}" if unit else content, marks=pytest.mark.en, id=f"en-{case_id}"
    )
    yield pytest.param(
        "pt_BR",
        expected_pt,
        f"{content} {unit[1]}" if unit else content,
        marks=pytest.mark.pt_BR,
        id=f"pt_BR-{case_id}",
    )


def lang_params(*, expected_en: str, expected_pt: str, unit: str) -> Iterable:
    time, unit_id = unit.split()
    en_scales = English().scales
    pt_scales = Portuguese().scales
    # es_scales = Spanish().scales
    en_scale = None
    pt_scale = None
    # es_scale = None

    for idx, scale in enumerate(en_scales):
        if unit_id in scale.terms:
            en_scale = scale.singular
            pt_scale = pt_scales[idx].singular
            # unit_es = es_scales[idx].singular

    yield pytest.param("en", expected_en, f"{time} {en_scale}", marks=pytest.mark.en, id=f"en-{en_scale}")
    yield pytest.param("pt_BR", expected_pt, f"{time} {pt_scale}", marks=pytest.mark.pt_BR, id=f"pt_BR-{pt_scale}")


def format_value(value: float, unit: str) -> str:
    if value >= 1:
        return str(int(value))
    result = f"{value:.4f}"
    if unit in {"week", "decades", "centuries"}:
        return "0.0" if result == "0.0000" else result
    return "0" if result == "0.0000" else result


def params_for_unit(*, unit_key: str, value: int) -> Iterable:
    en_scales = English().scales
    pt_scales = Portuguese().scales

    base_idx = next((idx for idx, scale in enumerate(en_scales) if scale.key == unit_key), None)
    assert base_idx is not None, f"Unit {unit_key!r} not found in scales"

    base_en = en_scales[base_idx]
    base_pt = pt_scales[base_idx]
    # base_es = es_scales[base_idx]

    for idx, target in enumerate(en_scales):
        if target.key in {"past", "now", "future", "raw"}:
            continue

        pt_target = pt_scales[idx]
        # es_target = es_scales[idx]

        factor = target.scale / base_en.scale
        raw = value * factor

        formatted = format_value(raw, base_en.singular)

        unit_en = base_en.singular if raw == 1 else base_en.plural
        # unit_pt = base_pt.singular if raw == 1 else base_pt.plural
        # unit_es = base_es.singular if raw == 1 else base_es.plural

        unit_pt = base_pt.singular if raw < 1 else base_pt.singular if raw == 1 else base_pt.plural

        if base_pt.singular == "dia" and formatted == "0" and pt_target.singular == "segundo":
            formatted = "0.0000"

        if base_pt.singular == "mes":
            unit_pt = "mês"

        yield pytest.param(
            "en",
            f"{formatted} {unit_en}",
            f"{base_en.singular} {value} {target.singular}",
            marks=pytest.mark.en,
            id=f"en-{target.singular}",
        )

        yield pytest.param(
            "pt_BR",
            f"{formatted} {unit_pt}",
            f"{base_pt.singular} {value} {pt_target.singular}",
            marks=pytest.mark.pt_BR,
            id=f"pt_BR-{pt_target.singular}",
        )

        # yield pytest.param(
        #     "es",
        #     f"{formatted} {unit_es}",
        #     f"{base_es.singular} {value} {es_target.singular}",
        #     marks=pytest.mark.es,
        #     id=f"es-{es_target.singular}",
        # )


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Converts units of time into other units, for example: Days to Hours, Seconds to Days, etc.",
            "To use: +time (final unit: seconds) (format to be transformed, e.g., 50h)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Converte unidades de tempo em outras unidades, exemplo: Dias em Horas, Segundos em Dias, etc.",
            "Para usar: +time (unidade final: segundos) (formato a ser transformado, ex: 50h)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    time_dates: ClassVar[list] = [
        *lang_params_date(
            case_id="same-date-same-hour",
            content="17:05:55 2020/12/25",
            expected_en="0 seconds",
            expected_pt="0 segundo",
        ),
        *lang_params_date(
            case_id="same-date-future", content="20:05:55 2020/12/25", expected_en="3 hours", expected_pt="3 horas"
        ),
        *lang_params_date(
            case_id="same-date-past",
            content="00:05:55 2020/12/25",
            expected_en="17 hours, 11 minutes and 50 seconds ago",
            expected_pt="há 17 horas, 11 minutos e 50 segundos",
        ),
        *lang_params_date(
            case_id="past-date-same-hour",
            content="17:05:55 2020/06/25",
            expected_en="6 months, 1 day, 10 hours, 11 minutes and 50 seconds ago",
            expected_pt="há 6 meses, 1 dia, 10 horas, 11 minutos e 50 segundos",
            unit=["past", "passado"],
        ),
        *lang_params_date(
            case_id="future-date-same-hour",
            content="17:05:55 2021/06/25",
            expected_en="5 months and 29 days",
            expected_pt="5 meses e 29 dias",
        ),
        *lang_params_date(
            case_id="really-far-past",
            content="17:05:55 1500/06/25",
            expected_en="520 years, 10 months, 6 days, 10 hours, 11 minutes and 50 seconds ago",
            expected_pt="há 520 anos, 10 meses, 6 dias, 10 horas, 11 minutos e 50 segundos",
            unit=["past", "passado"],
        ),
        *lang_params_date(
            case_id="really-far-future",
            content="17:05:55:43:234 3500/06/25",
            expected_en="1,480 years, 9 months, 25 days, 14 hours, 40 minutes and 59 seconds",
            expected_pt="1.480 anos, 9 meses, 25 dias, 14 horas, 40 minutos e 59 segundos",
        ),
    ]

    time: ClassVar[list] = [
        *lang_params(
            expected_en="2 minutes and 3.4568 seconds", expected_pt="2 minutos e 3.4568 segundos", unit="123456789 us"
        ),
        *lang_params(
            expected_en="1 day, 10 hours, 17 minutes and 36.7890 seconds",
            expected_pt="1 dia, 10 horas, 17 minutos e 36.7890 segundos",
            unit="123456789 ms",
        ),
        *lang_params(
            expected_en="3 years, 10 months, 28 days, 21 hours, 33 minutes and 9 seconds",
            expected_pt="3 anos, 10 meses, 28 dias, 21 horas, 33 minutos e 9 segundos",
            unit="123456789 s",
        ),
        *lang_params(
            expected_en="234 years, 10 months, 18 days, 21 hours and 9 minutes",
            expected_pt="234 anos, 10 meses, 18 dias, 21 horas e 9 minutos",
            unit="123456789 m",
        ),
        *lang_params(
            expected_en="14 years, 1 month and 3 days", expected_pt="14 anos, 1 mês e 3 dias", unit="123456 h"
        ),
        *lang_params(
            expected_en="338 years, 2 months and 25 days", expected_pt="338 anos, 2 meses e 25 dias", unit="123456 d"
        ),
        *lang_params(
            expected_en="236 years, 9 months and 0 days", expected_pt="236 anos, 9 meses e 0 dia", unit="12345 w"
        ),
        *lang_params(
            expected_en="1,014 years, 7 months and 26 days",
            expected_pt="1.014 anos, 7 meses e 26 dias",
            unit="12345 mo",
        ),
        *lang_params(expected_en="1,234 years", expected_pt="1.234 anos", unit="1234 y"),
        *lang_params(expected_en="1,230 years", expected_pt="1.230 anos", unit="123 dec"),
        *lang_params(expected_en="1,200 years", expected_pt="1.200 anos", unit="12 c"),
    ]

    only_date: ClassVar[list] = [
        pytest.param(
            "en", "1,480 years, 5 months, 21 days, 19 hours, 6 minutes and 17 seconds", marks=pytest.mark.en, id="en"
        ),
        pytest.param(
            "pt_BR",
            "1.480 anos, 5 meses, 21 dias, 19 horas, 6 minutos e 17 segundos",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    # microsecond = [
    #     *params_for_unit(
    #         unit_key="microsecond",
    #         value=1,
    #     ),
    # ]
    #
    # millisecond = [
    #     *params_for_unit(
    #         unit_key="millisecond",
    #         value=1,
    #     ),
    # ]
    #
    # second = [
    #     *params_for_unit(
    #             unit_key="second",
    #             value=1,
    #     ),
    # ]
    #
    # minute = [
    #     *params_for_unit(
    #             unit_key="minute",
    #             value=1
    #     ),
    # ]
    #
    # hour = [
    #     *params_for_unit(
    #             unit_key="hour",
    #             value=1
    #             ),
    # ]
    #
    # day = [
    #     *params_for_unit(
    #             unit_key="day",
    #             value=1
    #     ),
    # ]
    #
    # week = [
    #     *params_for_unit(
    #             unit_key="week",
    #             value=1
    #     )
    # ]
    #
    # month = [
    #     *params_for_unit(
    #             unit_key="month",
    #             value=1
    #     )
    # ]
    #
    # year = [
    #     *params_for_unit(
    #             unit_key="year",
    #             value=1
    #     )
    # ]
    #
    # decade = [
    #     *params_for_unit(
    #             unit_key="decade",
    #             value=1
    #     )
    # ]
    #
    # century = [
    #     *params_for_unit(
    #             unit_key="century",
    #             value=1
    #     )
    # ]

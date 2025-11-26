import re


class Asserter:
    @staticmethod
    def assert_string(
        response: str,
        expected: str | None = None,
        re_expected: str | None = None,
        strict: bool = False,
    ):
        helper = f"Expected {(expected or re_expected)!r}, got: {response!r}"
        if re_expected:
            assert re.search(re_expected, response), f"Expected pattern {re_expected!r}, got: {response!r}"
        elif expected is not None:
            if strict:
                assert response == expected, helper
            else:
                assert expected in response, helper
        else:
            raise ValueError("You must provide either `expected` or `expected_regex`.")

    @staticmethod
    def assert_number(
        response: str | int | float,
        expected: int | float | None = None,
        strict: bool = False,
        tolerance: float | None = None,
    ):
        if expected is None:
            raise ValueError("You must provide an expected number.")

        try:
            actual = float(response)
        except (ValueError, TypeError) as e:
            raise AssertionError(f"Response {response!r} is not a valid number.") from e

        helper = f"Expected {expected!r}, got: {actual!r}"

        if strict:
            assert actual == expected, helper
        elif tolerance is not None:
            assert abs(actual - expected) <= tolerance, f"{helper} (tolerance={tolerance})"
        else:
            assert round(actual, 6) == round(expected, 6), helper

    @staticmethod
    def assert_instance(obj, expected_type):
        assert isinstance(obj, expected_type), (
            f"Expected instance of {expected_type.__name__}, got {type(obj).__name__}: {obj!r}"
        )

    @staticmethod
    def assert_boolean(value, expected: bool):
        assert isinstance(expected, bool), (
            f"Expected value for 'expected' must be a bool, got {type(expected).__name__}"
        )
        assert isinstance(value, bool), f"Value must be a bool, got {type(value).__name__}: {value!r}"
        assert value is expected, f"Expected boolean {expected!r}, got {value!r}"

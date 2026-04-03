import sys
import atexit
from typing import Iterable

# NOTE: Add more feature soon. Uoc, Mika.
class ColorPicker:
    """
    Lightweight ANSI color utility.

    Design goals:
    - Zero dependency
    - Low overhead (just string formatting)
    - Safe fallback on invalid input
    - Usable like: color["#ff0000"]

    Note:
    This does NOT validate terminal capability (assumes ANSI support).
    """

    # ANSI control sequences (treated as constants)
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # High-intensity base colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'

    def __init__(self) -> None:
        """
        Register auto-reset to avoid leaking color state
        when the process exits unexpectedly.
        """
        atexit.register(self.reset)

    def reset(self) -> None:
        """
        Force reset terminal style.

        This is critical when:
        - Program crashes
        - User forgets to append END manually
        """
        sys.stdout.write(self.END)
        sys.stdout.flush()

    def __getitem__(self, hex_code: str) -> str:
        """
        Allow usage like:
            color["#ff0000"]

        Internally converts HEX → ANSI 24-bit color.
        Falls back to END on failure.
        """
        try:
            r, g, b = self._parse_hex(hex_code)
            return f'\033[38;2;{r};{g};{b}m'
        except ValueError:
            return self.END

    @staticmethod
    def _parse_hex(hex_code: str) -> tuple[int, int, int]:
        """
        Convert HEX string to RGB tuple.

        Supports:
            #rgb
            #rrggbb
            rgb
            rrggbb

        Raises:
            ValueError on invalid format
        """
        hex_code = hex_code.lstrip('#')

        # Expand shorthand (#abc → #aabbcc)
        if len(hex_code) == 3:
            hex_code = ''.join(c * 2 for c in hex_code)

        if len(hex_code) != 6:
            raise ValueError("Invalid HEX length")

        try:
            r = int(hex_code[0:2], 16)
            g = int(hex_code[2:4], 16)
            b = int(hex_code[4:6], 16)
        except ValueError as e:
            raise ValueError("Invalid HEX value") from e

        return r, g, b


# Global instance (intended for simple usage)
color = ColorPicker()


def cprint(text, styles: Iterable[str] | str = ColorPicker.END) -> None:
    """
    Print text with ANSI styling.

    Parameters:
        text   : Any printable object
        styles : Single style or iterable of styles

    Examples:
        cprint("Hello", color.RED)
        cprint("Bold Red", [color.RED, color.BOLD])
        cprint("Custom", color["#ff8800"])

    Implementation detail:
    - Avoids type errors by coercing input to str
    - Supports style composition via join
    """
    if isinstance(styles, str):
        style_str = styles
    else:
        style_str = ''.join(styles)

    sys.stdout.write(f"{style_str}{text}{color.END}\n")

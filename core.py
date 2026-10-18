import sys
import atexit

class ColorPicker:
    def __init__(self):
        self.END = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
        # Warna Dasar (High Intensity)
        self.red = '\033[91m'
        self.green = '\033[92m'
        self.yellow = '\033[93m'
        self.blue = '\033[94m'
        self.purple = '\033[95m'
        self.cyan = '\033[96m'
        
        # Auto-reset terminal saat script berhenti
        atexit.register(self.reset)

    def reset(self):
        sys.stdout.write(self.END)
        sys.stdout.flush()

    def __getitem__(self, hex_code):
        """Memungkinkan penggunaan: color['#ff0000']"""
        try:
            hex_code = hex_code.lstrip('#')
            if len(hex_code) == 3:
                hex_code = ''.join([c*2 for c in hex_code])
            r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
            return f'\033[38;2;{r};{g};{b}m'
        except Exception:
            return self.END

color = ColorPicker()

def cprint(text, style=color.END):
    """Fungsi utama untuk print berwarna"""
    # Pastikan teks dikonversi ke string agar tidak error jika inputnya angka/list
    print(f"{style}{text}{color.END}")

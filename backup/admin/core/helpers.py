def determine_kategori(diagnosa: str) -> str:
    text = (diagnosa or "").lower()
    if any(word in text for word in ["berat", "akut", "parah", "skizofrenia", "bipolar"]):
        return "Berisiko"
    if any(word in text for word in ["ringan", "minor"]):
        return "Memadai"
    return "Rendah"


def badge_color(kategori: str) -> str:
    k = (kategori or "").lower()
    if "berisiko" in k:
        return "#fecaca"  # merah muda
    if "memadai" in k:
        return "#bbf7d0"  # hijau muda
    return "#fef08a"      # kuning / default


def get_dummy_patients():
    return [
        ["Cell Content", "Gangguan Kecemasan", "Pelajar (SMA)", "Cell Content", {}],
        ["Cell Content", "Bipolar", "Pelajar (Mahasiswa)", "Cell Content", {}],
        ["Cell Content", "Anxiety", "Pekerja Kontrak", "Cell Content", {}],
        ["Cell Content", "OCD", "Pekerja Lepas", "Cell Content", {}],
        [
            "Cell Content",
            "Skizofrenia",
            "Sedang Mencari Pekerjaan",
            "Cell Content",
            {},
        ],
        ["Cell Content", "Gangguan tidur", "Pekerja Keras", "Cell Content", {}],
        ["Cell Content", "Insomnia", "Pelajar", "Cell Content", {}],
        ["Cell Content", "Moody", "Pelajar", "Cell Content", {}],
        ["Cell Content", "Gangguan makan", "Pekerja Tetap", "Cell Content", {}],
        ["Cell Content", "Depresi", "Pekerja Lepas", "Cell Content", {}],
    ]

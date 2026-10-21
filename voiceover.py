#!/usr/bin/env python3
"""
voiceover-studio: CLI & Generator Voice Over Bahasa Indonesia Natural HD.
Menggunakan arsitektur Edge Neural WebSocket terbaru (api.msedgeservices.com).
Diciptakan oleh Bagas Cihuy untuk ekosistem video, narasi, dan multimedia otonom.
"""
import argparse
import asyncio
import os
import sys
import tempfile
from pathlib import Path

import edge_tts

VOICES = {
    "gadis": "id-ID-GadisNeural",
    "ardi": "id-ID-ArdiNeural",
}
MAX_CHARS = 10000


async def synthesize(text: str, output: Path, voice: str, rate: int, pitch: int = 0) -> None:
    text_clean = text.strip()
    if not text_clean:
        raise ValueError("Teks tidak boleh kosong.")
    if len(text_clean) > MAX_CHARS:
        raise ValueError(f"Teks melebihi batas {MAX_CHARS} karakter (diterima: {len(text_clean)})")
    if output.suffix.lower() != ".mp3":
        output = output.with_suffix(".mp3")

    output.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"

    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".mp3", delete=False) as file:
            temp = Path(file.name)
            communicate = edge_tts.Communicate(
                text_clean,
                VOICES[voice],
                rate=rate_str,
                pitch=pitch_str
            )
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])

        if not temp.exists() or temp.stat().st_size < 1000:
            raise RuntimeError("Penyedia suara tidak mengembalikan stream audio yang valid.")

        os.replace(temp, output)
    finally:
        if temp and temp.exists():
            temp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="VoiceOver Studio ID — Generator Voice Over Natural Bahasa Indonesia HD"
    )
    parser.add_argument("text", nargs="?", help="Naskah voice over; jika kosong, membaca dari STDIN")
    parser.add_argument("-o", "--output", default="voiceover.mp3", type=Path, help="Nama berkas keluaran .mp3 (default: voiceover.mp3)")
    parser.add_argument(
        "--voice",
        choices=list(VOICES.keys()),
        default="gadis",
        help="Karakter suara: 'gadis' (santai/ramah) atau 'ardi' (formal/berwibawa)"
    )
    parser.add_argument(
        "--rate",
        type=int,
        default=0,
        help="Kecepatan bicara (-50 s/d +50 persen, default: 0)"
    )
    parser.add_argument(
        "--pitch",
        type=int,
        default=0,
        help="Tinggi nada suara dalam Hz (-50 s/d +50 Hz, default: 0)"
    )
    args = parser.parse_args()

    input_text = args.text if args.text is not None else sys.stdin.read(MAX_CHARS + 1)
    try:
        asyncio.run(synthesize(input_text, args.output, args.voice, args.rate, args.pitch))
        print(f"✅ Voice Over Berhasil Dibuat: {args.output.resolve()} ({os.path.getsize(args.output)} bytes)")
        return 0
    except Exception as exc:
        print(f"❌ Gagal: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

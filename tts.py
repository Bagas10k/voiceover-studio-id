#!/usr/bin/env python3
"""TTS Bahasa Indonesia: stream Edge Neural ke MP3 tanpa menahan audio di RAM."""
import argparse
import asyncio
import os
import sys
import tempfile
from pathlib import Path

import edge_tts

VOICES = {"gadis": "id-ID-GadisNeural", "ardi": "id-ID-ArdiNeural"}
MAX_CHARS = 5000


async def synthesize(text: str, output: Path, voice: str, rate: int) -> None:
    if not text.strip() or len(text) > MAX_CHARS:
        raise ValueError(f"Teks wajib diisi, maksimal {MAX_CHARS} karakter")
    if output.suffix.lower() != ".mp3":
        raise ValueError("Output harus berakhiran .mp3")
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".mp3", delete=False) as file:
            temp = Path(file.name)
            async for chunk in edge_tts.Communicate(text, VOICES[voice], rate=f"{rate:+d}%").stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
        if temp.stat().st_size < 1000:
            raise RuntimeError("Penyedia suara tidak mengembalikan audio yang valid")
        os.replace(temp, output)
    finally:
        if temp and temp.exists():
            temp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="TTS Indonesia natural berbasis Edge Neural")
    parser.add_argument("text", nargs="?", help="Teks yang dibacakan; jika kosong, baca stdin")
    parser.add_argument("-o", "--output", default="suara.mp3", type=Path)
    parser.add_argument("--voice", choices=VOICES, default="gadis")
    parser.add_argument("--rate", type=int, choices=range(-30, 31), metavar="-30..30", default=0)
    args = parser.parse_args()
    text = args.text if args.text is not None else sys.stdin.read(MAX_CHARS + 1)
    try:
        asyncio.run(synthesize(text, args.output, args.voice, args.rate))
    except (ValueError, OSError, RuntimeError, edge_tts.exceptions.EdgeTTSException) as exc:
        print(f"Gagal: {exc}", file=sys.stderr)
        return 1
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

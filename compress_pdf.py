import argparse
import pymupdf
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="无损压缩 PDF 并保留原件")
    parser.add_argument("input", type=Path, help="输入 PDF 的路径")
    source = parser.parse_args().input
    target = source.with_name(f"{source.stem}-compressed.pdf")

    if not source.is_file():
        parser.error(f"输入文件不存在：{source}")
    if target.exists():
        parser.error(f"输出文件已存在：{target}")

    with pymupdf.open(source) as doc:
        if not doc.is_pdf or doc.needs_pass:
            parser.error("请输入无需密码即可打开的 PDF 文件")
        doc.save(
            target,
            garbage=3,
            deflate=True,
            use_objstms=1,
            encryption=pymupdf.PDF_ENCRYPT_KEEP,
        )

    print(f"输出：{target}")
    print(f"体积：{source.stat().st_size:,} → {target.stat().st_size:,} 字节")


if __name__ == "__main__":
    main()
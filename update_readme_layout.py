#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


def _strip_comments(s: str) -> str:
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.DOTALL)
    s = re.sub(r"//.*?$", " ", s, flags=re.MULTILINE)
    return s


def _extract_layers(keymap_text: str):
    text = _strip_comments(keymap_text)

    def find_brace_block(src: str, open_brace_idx: int):
        depth = 0
        i = open_brace_idx
        while i < len(src):
            c = src[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return src[open_brace_idx + 1 : i], i
            i += 1
        raise ValueError("Unbalanced braces")

    def find_named_block(src: str, name: str):
        m = re.search(r"\b" + re.escape(name) + r"\s*\{", src)
        if not m:
            return None
        open_idx = src.find("{", m.start())
        body, close_idx = find_brace_block(src, open_idx)
        return body

    keymap_body = find_named_block(text, "keymap")
    if keymap_body is None:
        return []

    layers = []
    i = 0
    ident_pat = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\{")
    while i < len(keymap_body):
        m = ident_pat.search(keymap_body, i)
        if not m:
            break
        node = m.group(1)
        open_idx = keymap_body.find("{", m.start())
        body, close_idx = find_brace_block(keymap_body, open_idx)
        i = close_idx + 1

        label_m = re.search(r'label\s*=\s*"([^"]+)"\s*;', body)
        bindings_m = re.search(r"bindings\s*=\s*<(?P<bindings>.*?)>\s*;", body, flags=re.DOTALL)
        if not label_m or not bindings_m:
            continue

        label = label_m.group(1)
        bindings_raw = bindings_m.group("bindings")
        bindings = parse_bindings(bindings_raw)
        layers.append((node, label, bindings))

    return layers


def parse_bindings(bindings_raw: str):
    raw = _strip_comments(bindings_raw)
    raw = raw.replace("\n", " ")
    raw = raw.replace("\t", " ")
    raw = raw.replace(">", " ")
    raw = raw.replace("<", " ")

    tokens = [t for t in raw.split(" ") if t]

    bindings = []
    current = []
    for tok in tokens:
        if tok.startswith("&"):
            if current:
                bindings.append(current)
            current = [tok]
        else:
            if not current:
                # ignore garbage before first '&'
                continue
            current.append(tok)
    if current:
        bindings.append(current)

    return [format_binding(b) for b in bindings]


def format_binding(parts):
    if not parts:
        return ""

    b = parts[0]

    if b == "&kp" and len(parts) >= 2:
        return parts[1]

    if b == "&mo" and len(parts) >= 2:
        return f"MO({parts[1]})"

    if b == "&tog" and len(parts) >= 2:
        return f"TOG({parts[1]})"

    if b == "&mt" and len(parts) >= 3:
        return f"MT({parts[1]},{parts[2]})"

    if b == "&out" and len(parts) >= 2:
        return f"OUT({parts[1]})"

    if b == "&bt" and len(parts) >= 3:
        return f"BT({parts[1]},{parts[2]})"

    if b == "&trans":
        return "TRNS"

    # Fallback: keep it readable but compact
    return " ".join(parts).replace("&", "")


def _chunks(lst, n):
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def _format_md_table(rows, widths):
    def fmt_cell(cell: str, w: int) -> str:
        cell = cell or ""
        pad = w - len(cell)
        left = pad // 2
        right = pad - left
        return " " + (" " * left) + cell + (" " * right) + " "

    lines = []
    for r in rows:
        lines.append("|" + "|".join(fmt_cell(c, w) for c, w in zip(r, widths)) + "|")

    # Center alignment for all columns.
    # At least 3 dashes are recommended for markdown table separators.
    def sep_cell(w: int) -> str:
        # Use content width for readability; markdown doesn't require exact matching,
        # but this keeps the source nicely aligned.
        dashes = max(3, w)
        return " :" + ("-" * dashes) + ": "

    sep = "|" + "|".join(sep_cell(w) for w in widths) + "|"
    lines.insert(1, sep)
    return lines


def render_md_table(rows):
    if not rows:
        return []

    col_count = len(rows[0])
    widths = [0] * col_count
    for r in rows:
        if len(r) != col_count:
            raise ValueError("Inconsistent row width")
        for i, c in enumerate(r):
            c = c or ""
            widths[i] = max(widths[i], len(c))

    return _format_md_table(rows, widths)


def render_layer_table(label: str, bindings):
    # KOMETA uses 42 bindings in default layout:
    # - 3 rows * 12 keys, displayed as 14 columns (6 left + 2 empty center + 6 right)
    # - thumb row: 6 keys, displayed as 14 columns (4 empty left + 6 keys + 4 empty right)
    main_rows = 3
    main_cols = 12
    table_cols = 14
    thumb_cols = 6
    empty = ""

    out = []
    out.append(f"### {label}")

    if len(bindings) != main_rows * main_cols + thumb_cols:
        out.append("")
        out.append(f"_Warning: ожидается 42 клавиши, найдено {len(bindings)}. Печатаю списком._")
        out.append("")
        out.append("```")
        out.append("\n".join(bindings))
        out.append("```")
        out.append("")
        return "\n".join(out)

    main = bindings[: main_rows * main_cols]
    thumbs = bindings[main_rows * main_cols :]

    out.append("")
    main_rows_data = _chunks(main, main_cols)

    def expand_main_row(row12):
        left = row12[:6]
        right = row12[6:]
        return left + [empty, empty] + right

    thumb_row = ([empty] * 4) + thumbs + ([empty] * 4)
    all_rows = [expand_main_row(r) for r in main_rows_data] + [thumb_row]
    out.extend(render_md_table(all_rows))
    out.append("")

    return "\n".join(out)


def generate_layout_markdown(keymap_path: Path):
    keymap_text = keymap_path.read_text(encoding="utf-8")
    layers = _extract_layers(keymap_text)

    if not layers:
        return "_Не удалось найти слои/биндинги в keymap._\n"

    blocks = []
    for _node, label, bindings in layers:
        blocks.append(render_layer_table(label, bindings))

    return "\n".join(blocks).rstrip() + "\n"


def update_readme(readme_path: Path, keymap_path: Path):
    readme_lines = readme_path.read_text(encoding="utf-8").splitlines(True)

    heading_re = re.compile(r"^##\s+")
    layout_heading = "## Раскладка\n"

    try:
        start_idx = next(i for i, line in enumerate(readme_lines) if line.strip() == "## Раскладка")
    except StopIteration:
        if readme_lines and not readme_lines[-1].endswith("\n"):
            readme_lines[-1] += "\n"
        if readme_lines and readme_lines[-1].strip() != "":
            readme_lines.append("\n")
        readme_lines.append(layout_heading)
        start_idx = len(readme_lines) - 1

    end_idx = len(readme_lines)
    for i in range(start_idx + 1, len(readme_lines)):
        if heading_re.match(readme_lines[i]) and i != start_idx:
            end_idx = i
            break

    generated = generate_layout_markdown(keymap_path)
    replacement = ["\n", generated]

    new_lines = readme_lines[: start_idx + 1] + replacement + readme_lines[end_idx:]
    readme_path.write_text("".join(new_lines), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Update README layout tables from ZMK keymap")
    p.add_argument("--readme", default="readme.md", help="Path to README.md")
    p.add_argument("--keymap", default="config/kometa.keymap", help="Path to .keymap")
    args = p.parse_args()

    readme_path = Path(args.readme)
    keymap_path = Path(args.keymap)

    update_readme(readme_path, keymap_path)


if __name__ == "__main__":
    main()

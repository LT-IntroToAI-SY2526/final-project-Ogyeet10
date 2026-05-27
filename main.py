import html
import sys


def make_inline_text(text):
    text = html.escape(text)
    text = change_pairs(text, "**", "<strong>", "</strong>")
    text = change_pairs(text, "*", "<em>", "</em>")
    text = change_pairs(text, "`", "<code>", "</code>")
    return text


def change_pairs(text, marker, open_tag, close_tag):
    pieces = text.split(marker)

    if len(pieces) == 1:
        return text
    if (len(pieces) - 1) % 2 != 0:
        return text

    new_text = pieces[0]
    use_open_tag = True

    for piece in pieces[1:]:
        if use_open_tag:
            new_text += open_tag + piece
        else:
            new_text += close_tag + piece

        use_open_tag = not use_open_tag

    return new_text


def convert_markdown(markdown_text):
    html_lines = ["<!doctype html>", "<html>", "<body>"]
    in_list = False
    in_paragraph = False

    for line in markdown_text.splitlines():
        stripped = line.strip()

        if stripped == "":
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        if stripped.startswith("#"):
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if in_list:
                html_lines.append("</ul>")
                in_list = False

            level = 0
            for char in stripped:
                if char == "#" and level < 6:
                    level += 1
                else:
                    break

            heading_text = stripped[level:].strip()
            html_lines.append(f"<h{level}>" + make_inline_text(heading_text) + f"</h{level}>")
            continue

        if stripped.startswith("- "):
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if not in_list:
                html_lines.append("<ul>")
                in_list = True

            item_text = stripped[2:].strip()
            html_lines.append("<li>" + make_inline_text(item_text) + "</li>")
            continue

        if in_list:
            html_lines.append("</ul>")
            in_list = False

        if not in_paragraph:
            html_lines.append("<p>")
            in_paragraph = True

        html_lines.append(make_inline_text(stripped))

    if in_paragraph:
        html_lines.append("</p>")
    if in_list:
        html_lines.append("</ul>")

    html_lines.append("</body>")
    html_lines.append("</html>")
    return "\n".join(html_lines) + "\n"


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 main.py input.md output.html")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    html_text = convert_markdown(markdown_text)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_text)

    print("Converted " + input_file + " to " + output_file)


if __name__ == "__main__":
    main()

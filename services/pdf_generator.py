import re
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from io import BytesIO


def convert_inline_markdown(text: str) -> str:
    """
    Converts **bold** and *italic* into ReportLab-friendly tags.
    """

    # Bold
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Italic
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)

    return text


from io import BytesIO

def generate_pdf(content: str):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    h1 = styles["Heading1"]
    h2 = styles["Heading2"]
    h3 = styles["Heading3"]
    normal = styles["BodyText"]

    elements = []
    lines = content.split("\n")
    bullet_buffer = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("### "):
            elements.append(Paragraph(line[4:], h3))
            elements.append(Spacer(1, 0.2 * inch))

        elif line.startswith("## "):
            elements.append(Paragraph(line[3:], h2))
            elements.append(Spacer(1, 0.25 * inch))

        elif line.startswith("# "):
            elements.append(Paragraph(line[2:], h1))
            elements.append(Spacer(1, 0.3 * inch))

        elif line.startswith("- "):
            bullet_text = convert_inline_markdown(line[2:])
            bullet_buffer.append(ListItem(Paragraph(bullet_text, normal)))

        else:
            if bullet_buffer:
                elements.append(ListFlowable(bullet_buffer, bulletType="bullet"))
                elements.append(Spacer(1, 0.2 * inch))
                bullet_buffer = []

            paragraph_text = convert_inline_markdown(line)
            elements.append(Paragraph(paragraph_text, normal))
            elements.append(Spacer(1, 0.2 * inch))

    if bullet_buffer:
        elements.append(ListFlowable(bullet_buffer, bulletType="bullet"))

    doc.build(elements)

    buffer.seek(0)
    return buffer.getvalue()  
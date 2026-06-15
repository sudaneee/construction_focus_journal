import os
from pypdf import PdfReader

SRC = r"C:\Users\ismai\Downloads\cfjournal"
OUT = r"C:\Users\ismai\OneDrive\Desktop\Projects2026\ConstructionFocusJournal\import_data\text"

FILES = {
    "2021": [
        "1-002-.pdf",
        "2-009-.pdf",
        "3-015-.pdf",
        "4-021-.pdf",
        "5-031- .pdf",
        "6-032-.pdf",
        "7-034- .pdf",
        "8-039.pdf",
        "9-045-.pdf",
    ],
    "2022": [
        "2-016 .pdf",
        "3-020-.pdf",
        "4-033 .pdf",
        "5-035-.pdf",
        "6-037-.pdf",
        "7-042-.pdf",
        "8-046 -.pdf",
    ],
    "2023": [
        "1-004 - corrected Manuscript.pdf",
        "2-007 - corrected Manuscript.pdf",
        "3-012- corrected manuscript.pdf",
        "4-025 - Clean Copy_Evaluation_of the Interrelationships Among the Causes of Wall Cracks in Residential Building.pdf",
        "5-026- Mechanical Properties of Laterite Bricks Produced with Plastic Waste as Bi.pdf",
        "6-029_ corrected manuscript.pdf",
        "7-030- corrected Utilisation of Building Information Modelling Capabilities .pdf",
    ],
    "2024": [
        "1-006-  corrected.pdf",
        "2-010- corrected manuscript.pdf",
        "3-011 corrected manuscript .pdf",
        "4-017 corrected manuscript .pdf",
        "5-019- Final Corrected Manuscript.pdf",
        "6-022 - corrected 1st vetting manuscript.pdf",
        "7-023- final manuscript.pdf",
        "8-024 - Clean Copy_Evaluation_of_Change_Order_Factors_in_Building_Construction_Projects.pdf",
        "9-036 corrected.pdf",
        "10-040 corrected.pdf",
        "11-041 corrected manuscript.pdf",
    ],
}

os.makedirs(OUT, exist_ok=True)

for year, files in FILES.items():
    year_out = os.path.join(OUT, year)
    os.makedirs(year_out, exist_ok=True)
    for i, fname in enumerate(files, start=1):
        path = os.path.join(SRC, year, fname)
        reader = PdfReader(path)
        npages = len(reader.pages)
        # Only first 3 pages usually contain title/authors/abstract/keywords
        pages_to_read = min(npages, 3)
        text_parts = []
        for p in range(pages_to_read):
            text_parts.append(f"--- PAGE {p+1} ---\n" + reader.pages[p].extract_text())
        text = "\n".join(text_parts)
        out_name = f"{i:02d}_{fname.replace('/', '_')}.txt"
        with open(os.path.join(year_out, out_name), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"{year}/{fname}: {npages} pages -> {out_name}")

import pandas as pd
import re

# File Paths
input_path = "data/cleaned_output.csv"
excel_output_path = "outputs/new_cleaned_output.xlsx"
csv_output_path = "outputs/new_cleaned_output.csv"

# Load File
df = pd.read_csv(input_path)


# Prepare new columns
codes = ['DNA', 'PE', 'RC', 'RD', 'A', 'NC', 'WR', 'O']
for code in codes:
    df[code] = 0
df['Notes'] = ""

# Function to parse the codes and notes
def parse_basis(text):
    if pd.isna(text):
        return {code: 0 for code in codes} | {"Notes": ""}

    # Normalize
    norm = re.sub(r'[\n;/]+', ',', str(text))
    norm = re.sub(r'\s+', ' ', norm).strip()

    # Extract codes
    found_codes = set(re.findall(r'\b(?:' + '|'.join(codes) + r')\b', norm))
    output = {code: (1 if code in found_codes else 0) for code in codes}

    # Extract parenthetical content
    parentheticals = re.findall(r'\((.*?)\)', norm)

    # Remove parentheticals and codes from main string
    cleaned = norm
    for code in codes:
        cleaned = re.sub(rf'\b{code}\b', '', cleaned)
    cleaned = re.sub(r'\(.*?\)', '', cleaned)

    # Clean punctuation and whitespace
    cleaned = re.sub(r'[:,;()\-\[\]]+', ' ', cleaned)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()

    # Combine all note sources with punctuation
    notes_parts = parentheticals + ([cleaned] if cleaned else [])
    notes = '; '.join([part.strip() for part in notes_parts if part.strip()])

    output['Notes'] = notes
    return output

# Apply parsing to each row
column_name = 'Exoneration & release: Factual Basis of Exoneration (Note)'
parsed = df[column_name].apply(parse_basis).apply(pd.Series)
df.update(parsed)

# Save the output
df.to_excel(excel_output_path, index=False)
df.to_csv(csv_output_path, index=False, encoding='utf-8')

print("Done! Files saved to:")
print(f"  Excel → {excel_output_path}")
print(f"  CSV   → {csv_output_path}")

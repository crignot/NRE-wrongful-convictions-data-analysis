import pandas as pd
import re

# Load the file — change this to your actual file name
df = pd.read_excel("/Users/chiararignot/Documents/Factual_Basis_by_Simon_Cole.xlsx")


# Prepare new columns
codes = ['DNA', 'PE', 'RC', 'RD', 'A', 'NC', 'WR', 'O']
for code in codes:
    df[code] = 0
df['Notes'] = ""

# Function to parse the codes and notes
def parse_basis(text):
    if pd.isna(text):
        return {code: 0 for code in codes} | {"Notes": ""}

    # Normalize separators
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
parsed = df['Exoneration & release: Factual Basis of Exoneration (Note)'].apply(parse_basis).apply(pd.Series)
df.update(parsed)

# Save the output
df.to_excel("cleaned_output.xlsx", index=False)

print("✅ Done! Saved as 'cleaned_output.xlsx'")

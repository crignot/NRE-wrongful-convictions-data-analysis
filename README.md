# Exoneration Data Cleaning – Python Scripts

This repository contains Python scripts developed to clean and preprocess data from the **National Registry of Exonerations (NRE)**.  
Due to confidentiality, the raw datasets are not included here. These scripts are provided for transparency and reproducibility of the methods used.

---

## Repository Structure

```
exoneration-data-cleaning/
├─ NatRegCleaning_CR.py # Final cleaning pipeline (author: Chiara Rignot)
├─ oldcleaner.py # Deprecated early version of the cleaning script
└─ README.md
```

---

## Requirements

- **Python 3.8+**
- Libraries:
  - pandas
  - numpy
  - openpyxl (if processing Excel files)

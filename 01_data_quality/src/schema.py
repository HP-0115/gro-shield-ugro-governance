"""
schema.py
Defines the controlled vocabulary and structure for the synthetic
MSME loan dataset. This is the single source of truth other scripts
will import from, so values stay consistent across the whole module.
"""

INDIAN_STATES = [
    "Maharashtra", "Gujarat", "Tamil Nadu", "Karnataka", "Rajasthan",
    "Uttar Pradesh", "West Bengal", "Madhya Pradesh", "Delhi", "Punjab",
]

SECTORS = [
    "Textile & Apparel", "Food Processing", "Auto Components",
    "Pharma & Healthcare", "IT/ITES Services", "Retail Trade",
    "Construction Materials", "Agriculture Allied",
]

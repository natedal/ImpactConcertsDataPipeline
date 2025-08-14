"""
# iVoted
Takes voting or CVAP block‑level files from Redistricting Data Hub
and aggregates them to the city level.
"""

import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------
RESULTS_DIR = Path("code 2/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def _pad_geoid(series: pd.Series, colname: str = "geoid20") -> pd.Series:
    """Left‑pad to 15 chars (Census GEOID20 length)."""
    return series.astype(str).str.zfill(15).rename(colname)


# ---------------------------------------------------------------------
# 1. Voting + *new* Registration aggregation
# ---------------------------------------------------------------------
def agg_voter(block_data_file: str, corr_file: str, city_name: str) -> None:
    """
    Aggregate block‑level voting & registration fields to the city level.
    Saves {city}.csv in RESULTS_DIR.
    """

    # Read files
    block = pd.read_csv(block_data_file, dtype=str, encoding_errors="replace")
    corr = pd.read_csv(corr_file, dtype=str, encoding_errors="replace").iloc[1:]  # drop header row

    # ----- 1. Keep relevant columns -----
    vote_cols = [
        "g20201103_voted_all", "g20201103_voted_eur", "g20201103_voted_hisp",
        "g20201103_voted_aa", "g20201103_voted_esa", "g20201103_voted_oth",
        "g20201103_voted_unk"
    ]
    reg_cols = [
        "g20221108_reg_all", "g20221108_reg_eur", "g20221108_reg_hisp",
        "g20221108_reg_aa", "g20221108_reg_esa", "g20221108_reg_oth",
        "g20221108_reg_unk"
    ]
    keep_cols = ["geoid20"] + vote_cols + reg_cols
    block = block[keep_cols]

    # ----- 2. Build full GEOID20 in correlation table and pad -----
    corr_geoid = corr["county"] + corr["tract"].str[:4] + corr["tract"].str[5:] + corr["block"]
    corr["geoid20"] = _pad_geoid(corr_geoid)
    block["geoid20"] = _pad_geoid(block["geoid20"])

    # ----- 3. Merge & filter to target city -----
    merged = block.merge(corr, on="geoid20", how="inner")
    city = merged.loc[merged["PlaceName"] == city_name, vote_cols + reg_cols]

    # ----- 4. Aggregate -----
    city_sum = city.astype(float).sum()

    # ----- 5. Save -----
    out = RESULTS_DIR / f"{city_name}.csv"
    city_sum.to_csv(out, header=False)
    print(f"Saved → {out}")


# ---------------------------------------------------------------------
# 2. CVAP aggregation (unchanged except for small tidy‑ups)
# ---------------------------------------------------------------------
def agg_cvap(block_data_file: str, corr_file: str, city_name: str) -> None:
    """
    Aggregate CVAP block‑level file to the city level.
    Saves {city}_cvap.csv in RESULTS_DIR.
    """

    block = pd.read_csv(block_data_file, dtype=str, encoding_errors="replace")
    corr = pd.read_csv(corr_file, dtype=str, encoding_errors="replace").iloc[1:]

    corr_geoid = corr["county"] + corr["tract"].str[:4] + corr["tract"].str[5:] + corr["block"]
    corr["geoid20"] = _pad_geoid(corr_geoid)
    block["GEOID20"] = _pad_geoid(block["GEOID20"])

    merged = block.merge(corr, left_on="GEOID20", right_on="geoid20", how="inner")
    city = merged.loc[merged["PlaceName"] == city_name]

    cvap_cols = [
        "CVAP_TOT21", "CVAP_HSP21", "CVAP_WHT21", "CVAP_BLK21", "CVAP_AIA21",
        "CVAP_ASN21", "CVAP_NHP21", "CVAP_2OM21", "CVAP_BLW21", "CVAP_AIW21",
        "CVAP_ASW21", "CVAP_AIB21"
    ]
    city_sum = city[cvap_cols].astype(float).sum()

    out = RESULTS_DIR / f"{city_name}_cvap.csv"
    city_sum.to_csv(out, header=False)
    print(f"Saved → {out}")

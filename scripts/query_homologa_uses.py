"""Registered uses of active substances from Homologa (BigQuery), for GAP preset design.

Usage (any Python with google-cloud-bigquery and Application Default Credentials, e.g. the
EFM-DLT-pAIR virtualenv):

    python scripts/query_homologa_uses.py                      # DIMETHOATE and THIACLOPRID
    python scripts/query_homologa_uses.py --substance DELTAMETHRIN --max-gb 150
    python scripts/query_homologa_uses.py --countries DE FR IT ES --crop-filter apple
    python scripts/query_homologa_uses.py --dry-run

Reads `bcs-dfs-eng.homologa` at `use` grain (one row per registered use, product and crop),
joining de-duplicated English lookups as in EFM-DLT-pAIR/dlt_pair/sources/homologa_bigquery.py.
Billing project `bcs-reg-core-datasets`; the scan is capped with --max-gb (views report 0 bytes
on dry runs; a real scan of the use view needs more than 160 GB, about 1 to 2 USD). Results are written to
scripts/homologa/<stamp>_<substances>.csv and .parquet, and a summary (countries, products,
crops, dose and timing of orchard uses) is printed. An identical query within 24 h is served
from the BigQuery result cache free of charge.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(REPO_ROOT, "scripts", "homologa")
DATASET = "bcs-dfs-eng.homologa"
BILLING_PROJECT = "bcs-reg-core-datasets"


def english_lookup(table: str, code_col: str, name_col: str, lang_col: str = "language") -> str:
    return (
        f"(SELECT {code_col}, COALESCE(ANY_VALUE(IF(UPPER(CAST({lang_col} AS STRING)) LIKE 'EN%', {name_col}, NULL)), "
        f"ANY_VALUE({name_col})) AS {name_col} FROM `{DATASET}.{table}` GROUP BY {code_col})"
    )


def build_query(filter_countries: bool = False) -> str:
    """SQL at use grain. The country filter is only emitted when countries are given: an empty
    ARRAY parameter arrives as NULL in BigQuery, which would make the WHERE clause drop every row."""
    country_filter = "WHERE UPPER(country.ctry_abrev) IN UNNEST(@countries)" if filter_countries else ""
    crop_stage = english_lookup("crop_stage", "crop_stag_code", "crop_stag_name")
    time_app = english_lookup("time_application", "time_app_code", "time_app_name")
    method = english_lookup("application_method", "meth_code", "meth_name")
    dose_unit = english_lookup("dose_unit", "dose_unit_code", "dose_unit_name")
    country = (
        f"(SELECT ctry_code, ANY_VALUE(ctry_abrev) AS ctry_abrev, "
        f"COALESCE(ANY_VALUE(IF(UPPER(CAST(language AS STRING)) LIKE 'EN%', ctry_name, NULL)), ANY_VALUE(ctry_name)) AS ctry_name "
        f"FROM `{DATASET}.country` GROUP BY ctry_code)"
    )
    crop = (
        f"(SELECT crop_code, ANY_VALUE(crop_name) AS crop_name, ANY_VALUE(crop_name_latin) AS crop_name_latin, "
        f"ANY_VALUE(crop_eppo_code) AS crop_eppo_code, ANY_VALUE(crpg_name_eu) AS crpg_name_eu FROM `{DATASET}.crop` GROUP BY crop_code)"
    )
    crop_stage_original = (
        f"(SELECT crop_stag_orig_code, ctry_code, ANY_VALUE(crop_stag_orig_name_en) AS crop_stag_orig_name_en, "
        f"ANY_VALUE(bbch_from_code) AS bbch_from_code, ANY_VALUE(bbch_to_code) AS bbch_to_code "
        f"FROM `{DATASET}.crop_stage_original` GROUP BY crop_stag_orig_code, ctry_code)"
    )
    pest = (
        f"(SELECT pest_code, ANY_VALUE(pest_name) AS pest_name, ANY_VALUE(pest_eppo_code) AS pest_eppo_code "
        f"FROM `{DATASET}.pest` GROUP BY pest_code)"
    )
    product = (
        f"(SELECT prod_code, ctry_code, ANY_VALUE(num_regist) AS num_regist, ANY_VALUE(prod_orig_name_en) AS prod_orig_name_en, "
        f"ANY_VALUE(form_code) AS form_code, ANY_VALUE(date_regis) AS date_regis, ANY_VALUE(exp_date_p) AS exp_date_p "
        f"FROM `{DATASET}.product` GROUP BY prod_code, ctry_code)"
    )
    active = (
        f"(SELECT prod_code, ctry_code, acti_name, ANY_VALUE(cas_no) AS cas_no, ANY_VALUE(concentrat) AS concentrat, "
        f"ANY_VALUE(acti_unit_name) AS acti_unit_name FROM `{DATASET}.active_ingredient` "
        f"WHERE UPPER(acti_name) IN UNNEST(@active_substances) GROUP BY prod_code, ctry_code, acti_name)"
    )
    return f"""
SELECT
  u.use_id, u.ctry_code, country.ctry_abrev, country.ctry_name,
  u.prod_code, product.num_regist, product.prod_orig_name_en, product.form_code,
  product.date_regis AS prod_date_regis, product.exp_date_p AS prod_exp_date,
  active.acti_name, active.cas_no, active.concentrat, active.acti_unit_name,
  u.crop_code, crop.crop_name, crop.crop_name_latin, crop.crop_eppo_code, crop.crpg_name_eu,
  u.site_code, u.meth_code, method.meth_name,
  u.crop_stag_code, crop_stage.crop_stag_name,
  crop_stage_original.crop_stag_orig_name_en, crop_stage_original.bbch_from_code, crop_stage_original.bbch_to_code,
  u.time_app_code, time_app.time_app_name,
  u.pest_code, pest.pest_name, pest.pest_eppo_code,
  u.min_dose_r, u.max_dose_r, u.dose_unit_code, dose_unit.dose_unit_name,
  u.max_dose_season, u.max_dose_season_unit_code,
  u.max_treat_app, u.max_treat_season, u.inter_treat_min, u.inter_treat_max, u.inter_treat_unit_code, u.phi,
  u.type_regis_code, u.prof_amateur_code, u.date_regis AS use_date_regis, u.exp_date_r AS use_exp_date,
  CASE WHEN active.acti_unit_name = 'G/L' AND dose_unit.dose_unit_name = 'L/HA'
       THEN SAFE_CAST(active.concentrat AS FLOAT64) * SAFE_CAST(u.max_dose_r AS FLOAT64) / 1000
       WHEN active.acti_unit_name = 'G/KG' AND dose_unit.dose_unit_name = 'KG/HA'
       THEN SAFE_CAST(active.concentrat AS FLOAT64) * SAFE_CAST(u.max_dose_r AS FLOAT64) / 1000
       ELSE NULL END AS max_rate_kg_ai_ha
FROM `{DATASET}.use` AS u
JOIN {active} AS active ON active.prod_code = u.prod_code AND active.ctry_code = u.ctry_code
LEFT JOIN {product} AS product ON product.prod_code = u.prod_code AND product.ctry_code = u.ctry_code
LEFT JOIN {country} AS country ON country.ctry_code = u.ctry_code
LEFT JOIN {crop} AS crop ON crop.crop_code = u.crop_code
LEFT JOIN {crop_stage} AS crop_stage ON crop_stage.crop_stag_code = u.crop_stag_code
LEFT JOIN {crop_stage_original} AS crop_stage_original
  ON crop_stage_original.crop_stag_orig_code = u.crop_stag_orig_code AND crop_stage_original.ctry_code = u.ctry_code
LEFT JOIN {time_app} AS time_app ON time_app.time_app_code = u.time_app_code
LEFT JOIN {method} AS method ON method.meth_code = u.meth_code
LEFT JOIN {pest} AS pest ON pest.pest_code = u.pest_code
LEFT JOIN {dose_unit} AS dose_unit ON dose_unit.dose_unit_code = u.dose_unit_code
{country_filter}
"""


def summarize(frame, crop_filter: str) -> None:
    import pandas as pd

    pd.set_option("display.width", 200, "display.max_columns", 30, "display.max_colwidth", 40)
    today = dt.date.today().isoformat()
    exp = frame["use_exp_date"].astype("string")
    frame = frame.assign(valid=(exp.isna()) | (exp >= today))
    for substance, part in frame.groupby("acti_name"):
        print(f"\n===== {substance}: {len(part)} use rows, {part['use_id'].nunique()} use ids, "
              f"{part['ctry_abrev'].nunique()} countries, {part['prod_code'].nunique()} products, "
              f"{int(part['valid'].sum())} rows not expired")
        print("-- countries (rows, valid rows):")
        print(part.groupby("ctry_abrev")["valid"].agg(["size", "sum"]).sort_values("size", ascending=False).head(25).T.to_string())
        print("-- top crops:")
        print(part["crop_name"].value_counts().head(15).to_string())
        if crop_filter:
            sel = part[part["crop_name"].astype("string").str.contains(crop_filter, case=False, na=False)
                       | part["crpg_name_eu"].astype("string").str.contains(crop_filter, case=False, na=False)]
            print(f"-- '{crop_filter}' uses: {len(sel)} rows, {int(sel['valid'].sum())} not expired")
            cols = ["ctry_abrev", "prod_orig_name_en", "crop_name", "max_dose_r", "dose_unit_name", "max_rate_kg_ai_ha",
                    "max_treat_app", "inter_treat_min", "time_app_name", "crop_stag_name", "bbch_from_code", "bbch_to_code",
                    "phi", "use_exp_date"]
            print(sel.sort_values(["valid", "ctry_abrev"], ascending=[False, True])[cols].head(40).to_string(index=False))
            if sel["max_rate_kg_ai_ha"].notna().any():
                print("-- max rate kg a.i./ha (orchard uses):", sel["max_rate_kg_ai_ha"].describe().round(3).to_dict())
            if sel["max_treat_app"].notna().any():
                print("-- applications per season:", sel["max_treat_app"].astype(float).value_counts().sort_index().to_dict())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--substance", action="append", help="active substance name as in Homologa (repeatable)")
    parser.add_argument("--countries", nargs="*", default=[], help="ISO country abbreviations to keep (default all)")
    parser.add_argument("--crop-filter", default="apple|pome|orchard", help="regex on crop / EU crop group for the detail summary")
    parser.add_argument("--max-gb", type=float, default=300, help="maximum bytes billed in GB (default 300; the use view scans about 200 GB)")
    parser.add_argument("--project", default=BILLING_PROJECT)
    parser.add_argument("--dry-run", action="store_true", help="validate the query only (views report 0 bytes)")
    parser.add_argument("--summary-only", metavar="PARQUET", help="re-print the summary from a saved parquet file")
    args = parser.parse_args()
    substances = [s.upper() for s in (args.substance or ["DIMETHOATE", "THIACLOPRID"])]
    countries = [c.upper() for c in args.countries]

    import pandas as pd
    if args.summary_only:
        summarize(pd.read_parquet(args.summary_only), args.crop_filter)
        return 0

    from google.cloud import bigquery

    sql = build_query(filter_countries=bool(countries))
    client = bigquery.Client(project=args.project)
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("active_substances", "STRING", substances),
            bigquery.ArrayQueryParameter("countries", "STRING", countries),
        ],
        maximum_bytes_billed=int(args.max_gb * 1e9),
        use_query_cache=True,
        dry_run=args.dry_run,
    )
    started = dt.datetime.now()
    job = client.query(sql, job_config=job_config)
    if args.dry_run:
        print(f"dry run ok; reported bytes: {job.total_bytes_processed} (views usually report 0)")
        return 0
    result = job.result()
    frame = result.to_arrow().to_pandas()
    billed = job.total_bytes_billed or 0
    print(f"{len(frame)} rows in {(dt.datetime.now() - started).total_seconds():.0f} s, "
          f"{billed / 1e9:.1f} GB billed (cache hit: {job.cache_hit}), job {job.job_id}")

    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = started.strftime("%Y%m%d_%H%M%S")
    base = os.path.join(OUT_DIR, f"{stamp}_{'_'.join(s.lower() for s in substances)}")
    frame.to_parquet(base + ".parquet", index=False)
    frame.to_csv(base + ".csv", index=False)
    print(f"written: {base}.parquet / .csv")
    summarize(frame, args.crop_filter)
    return 0


if __name__ == "__main__":
    sys.exit(main())

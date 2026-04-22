import os
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite

from great_expectations.render.renderer import ValidationResultsPageRenderer
from great_expectations.render.view import DefaultJinjaPageView

# ----------------------------------------------------------------------------- 
# Connexion Postgres (Airbyte)
# -----------------------------------------------------------------------------
PG_CONN_STR = os.getenv(
    "PG_CONN_STR",
    "postgresql+psycopg2://airbyte:airbyte@postgres-airbyte:5432/airbyte",
)

DATASOURCE_NAME = "pg_airbyte"
OUTPUT_DIR = "/usr/src/app/gx/validation_docs"

STG_FILE = "stg_sales_data_validation.html"
FCT_FILE = "fct_sales_validation.html"


# -----------------------------------------------------------------------------
# Helper : rendre un résultat en HTML Data Docs
# -----------------------------------------------------------------------------
def render_validation_html(result, suite_name: str, output_filename: str) -> str:
    # utile pour le renderer
    result.meta["expectation_suite_name"] = suite_name

    renderer = ValidationResultsPageRenderer()
    document = renderer.render(result)

    html_str = DefaultJinjaPageView().render(document)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_str)

    return output_path


# -----------------------------------------------------------------------------
# Helper : page d'accueil custom
# -----------------------------------------------------------------------------
def build_homepage():
    index_path = os.path.join(OUTPUT_DIR, "index.html")

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Data Quality Dashboard - Great Expectations</title>
  <style>
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #0b2535;
      color: #f8f9fa;
      margin: 0;
      padding: 0;
    }}
    header {{
      padding: 20px 40px;
      background: #102a43;
      border-bottom: 1px solid #173d57;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    header h1 {{
      margin: 0;
      font-size: 22px;
    }}
    header span {{
      font-size: 13px;
      opacity: 0.8;
    }}
    main {{
      padding: 30px 40px 50px 40px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 24px;
      margin-top: 20px;
    }}
    .card {{
      background: #102a43;
      border-radius: 14px;
      padding: 18px 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.25);
      border: 1px solid #173d57;
    }}
    .card h2 {{
      margin: 0 0 4px 0;
      font-size: 18px;
    }}
    .card p {{
      margin: 4px 0;
      font-size: 13px;
      opacity: 0.9;
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 600;
      margin-top: 6px;
    }}
    .badge.stg {{
      background: rgba(46, 196, 182, 0.15);
      color: #2ec4b6;
    }}
    .badge.fct {{
      background: rgba(255, 159, 67, 0.15);
      color: #ff9f43;
    }}
    .btn {{
      display: inline-block;
      margin-top: 12px;
      padding: 8px 14px;
      border-radius: 999px;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      background: #2f80ed;
      color: white;
      border: none;
      cursor: pointer;
    }}
    .btn:hover {{
      background: #2563c3;
    }}
    footer {{
      padding: 12px 40px 20px 40px;
      font-size: 11px;
      opacity: 0.7;
      text-align: right;
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>Data Quality Dashboard</h1>
      <span>Great Expectations • Airbyte ➜ dbt ➜ Postgres</span>
    </div>
  </header>
  <main>
    <p>Choisissez un rapport de validation :</p>
    <div class="grid">
      <div class="card">
        <span class="badge stg">Staging</span>
        <h2>analytics.stg_sales_data</h2>
        <p>Données nettoyées en entrée de la fact table. Contrôle des nulls, quantités et prix.</p>
        <a class="btn" href="{STG_FILE}">🔍 Ouvrir le rapport</a>
      </div>
      <div class="card">
        <span class="badge fct">Fact table</span>
        <h2>analytics.fct_sales</h2>
        <p>Table de faits ventes (montants, marges, remises). Contrôles métier sur les montants.</p>
        <a class="btn" href="{FCT_FILE}">🔍 Ouvrir le rapport</a>
      </div>
    </div>
  </main>
  <footer>
    Généré automatiquement par Great Expectations dans le conteneur <code>gx</code>.
  </footer>
</body>
</html>
"""
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"🏠 Page d'accueil générée : {index_path}")


print("🚀 Lancement pipeline Great Expectations")

# -----------------------------------------------------------------------------
# 1. Contexte GX & datasource Postgres
# -----------------------------------------------------------------------------
context = gx.get_context()
print("📁 Type de contexte :", type(context))

try:
    context.data_sources.delete(DATASOURCE_NAME)
    print(f"🗑️ Ancien datasource supprimé : {DATASOURCE_NAME}")
except Exception:
    print("ℹ️ Aucun ancien datasource à supprimer")

datasource = context.data_sources.add_postgres(
    name=DATASOURCE_NAME,
    connection_string=PG_CONN_STR,
)
print(f"✅ Nouveau datasource créé : {DATASOURCE_NAME}")


# -----------------------------------------------------------------------------
# 2. Validation de analytics.stg_sales_data
# -----------------------------------------------------------------------------
def validate_stg_sales_data():
    schema_name = "analytics"
    table_name = "stg_sales_data"
    asset_name = "stg_sales_data_asset"
    suite_name = "stg_sales_data_suite"

    print("\n🔷 Validation de analytics.stg_sales_data")

    asset = datasource.add_table_asset(
        name=asset_name,
        table_name=table_name,
        schema_name=schema_name,
    )
    print(f"📦 Asset ajouté : {schema_name}.{table_name}")

    batch_request = asset.build_batch_request()
    print("📥 BatchRequest créé")

    try:
        context.suites.delete(suite_name)
        print(f"🗑️ Ancienne suite supprimée : {suite_name}")
    except Exception:
        print("ℹ️ Aucune suite existante à supprimer pour", suite_name)

    suite = ExpectationSuite(suite_name)
    context.suites.add(suite)
    print(f"📘 Nouvelle suite créée : {suite_name}")

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite,
    )

    print("📊 Aperçu des données (stg) :")
    print(validator.head(5))

    # Expectations de base sur le staging
    validator.expect_column_values_to_not_be_null("invoice_no")
    validator.expect_column_values_to_not_be_null("stock_code")
    validator.expect_table_row_count_to_be_between(min_value=1)
    validator.expect_column_values_to_be_between("quantity", min_value=0)
    validator.expect_column_values_to_be_between("unit_price", min_value=0)

    print("✅ Expectations (stg_sales_data) définies, lancement de la validation...")
    result = validator.validate()
    print("🏁 Résultat stg_sales_data : success =", result.success)

    html_path = render_validation_html(
        result,
        suite_name=suite_name,
        output_filename=STG_FILE,
    )
    print(f"📄 Rapport Data Docs (stg_sales_data) : {html_path}")


# -----------------------------------------------------------------------------
# 3. Validation de analytics.fct_sales
# -----------------------------------------------------------------------------
def validate_fct_sales():
    schema_name = "analytics"
    table_name = "fct_sales"
    asset_name = "fct_sales_asset"
    suite_name = "fct_sales_suite"

    print("\n🟣 Validation de analytics.fct_sales")

    asset = datasource.add_table_asset(
        name=asset_name,
        table_name=table_name,
        schema_name=schema_name,
    )
    print(f"📦 Asset ajouté : {schema_name}.{table_name}")

    batch_request = asset.build_batch_request()
    print("📥 BatchRequest créé")

    try:
        context.suites.delete(suite_name)
        print(f"🗑️ Ancienne suite supprimée : {suite_name}")
    except Exception:
        print("ℹ️ Aucune suite existante à supprimer pour", suite_name)

    suite = ExpectationSuite(suite_name)
    context.suites.add(suite)
    print(f"📘 Nouvelle suite créée : {suite_name}")

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite,
    )

    print("📊 Aperçu des données (fct_sales) :")
    print(validator.head(5))

    # Expectations métier sur la fact table
    validator.expect_column_values_to_not_be_null("invoice_number")
    validator.expect_column_values_to_not_be_null("product_code")
    validator.expect_table_row_count_to_be_between(min_value=1)

    validator.expect_column_values_to_be_between("quantity_sold", min_value=0)
    validator.expect_column_values_to_be_between("price_per_unit", min_value=0)

    validator.expect_column_values_to_be_between("gross_amount", min_value=0)
    validator.expect_column_values_to_be_between("discount_amount", min_value=0)
    validator.expect_column_values_to_be_between("net_sales_amount", min_value=0)
    validator.expect_column_values_to_be_between("line_total", min_value=0)

    validator.expect_column_values_to_not_be_null("invoice_timestamp")

    print("✅ Expectations (fct_sales) définies, lancement de la validation...")
    result = validator.validate()
    print("🏁 Résultat fct_sales : success =", result.success)

    html_path = render_validation_html(
        result,
        suite_name=suite_name,
        output_filename=FCT_FILE,
    )
    print(f"📄 Rapport Data Docs (fct_sales) : {html_path}")


# -----------------------------------------------------------------------------
# 4. Lancer les 2 validations + page d'accueil
# -----------------------------------------------------------------------------
validate_stg_sales_data()
validate_fct_sales()
build_homepage()

print("\n✅ Pipeline GE terminé. Rapports disponibles dans gx/validation_docs/")

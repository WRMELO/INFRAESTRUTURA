import argparse, os
import papermill as pm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Nome do projeto (ex: projeto_mba)")
    parser.add_argument("--raw_ids", nargs="+", type=int, required=True, help="Lista de raw_file_id")
    args = parser.parse_args()

    cfg_path = f"configs/{args.project}.yaml"
    output_nb = f"output/{args.project}_staging.ipynb"
    os.makedirs("output", exist_ok=True)

    pm.execute_notebook(
        "eda/staging/staging_template.ipynb",
        output_nb,
        parameters=dict(
            project_name=args.project,
            raw_file_ids=args.raw_ids,
            config_path=cfg_path,
            DATABASE_URL=os.getenv("DATABASE_URL")
        )
    )
    print(f"Notebook gerado em {output_nb}")

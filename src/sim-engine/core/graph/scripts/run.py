import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=os.path.abspath(os.path.join(__file__, "../../../../.env")))

import json
from pathlib import Path
from graph.models.generate_content_models import GraphState
from graph.workflows.generate_contents import run_generate_content_workflow


RESULTS_DIR = Path(__file__).parent.parent / "results"


def get_next_result_path():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    index = 1
    while True:
        file_path = RESULTS_DIR / f"result_{index}.json"
        if not file_path.exists():
            return file_path
        index += 1


def main():
    # Create initial empty state
    initial_state = GraphState()

    # Run workflow
    final_state = run_generate_content_workflow(initial_state)

    # Determine output file path
    output_file = get_next_result_path()

    # Serialize the GraphState to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        final_state = GraphState(**final_state)  # turn dict back into model
        json.dump(final_state.model_dump(), f, indent=2, ensure_ascii=False)

    print(f"✅ Workflow complete! Result saved to: {output_file.resolve()}")


if __name__ == "__main__":
    main()

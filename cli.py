import argparse
import json
import os

# Placeholder for prompt rendering logic (would be imported from core/)
class MockPromptRenderer:
    def render_prompt(self, platform: str, prompt_name: str, data: dict, version: str = "latest") -> str:
        # In a real scenario, this would load and format a prompt template
        # For now, we'll just return a simplified string based on the app data
        return f"# {data.get("id", "N/A")} - {data.get("name", "N/A")}\n\nOverview: {data.get("overview", "N/A")}\nCategory: {data.get("category", "N/A")}\nTech Stack: {data.get("tech_stack", "N/A")}\nMonetization: {data.get("monetization", "N/A")}\n"

def load_app_data(app_id: str) -> dict:
    app_file = os.path.join("portfolio-publisher", "apps", f"{app_id.lower()}_{app_id.lower().replace("a", "").replace(" ", "_")}.json")
    # This path construction is a bit hacky due to the previous generation script's naming convention.
    # A more robust solution would involve a lookup or consistent naming.
    # For now, let's try to find the file based on the ID and name from raw_listings.json
    with open("/home/ubuntu/raw_listings.json", "r") as f:
        all_listings = json.load(f)
    for listing in all_listings:
        if listing["id"].lower() == app_id.lower():
            app_name_slug = listing["name"].lower().replace(" ", "_")
            app_file = os.path.join("portfolio-publisher", "apps", f"{app_id.lower()}_{app_name_slug}.json")
            if os.path.exists(app_file):
                with open(app_file, "r") as f:
                    return json.load(f)
    raise FileNotFoundError(f"App data for {app_id} not found.")

def generate_listing(app_id: str, output_format: str):
    try:
        app_data = load_app_data(app_id)
        renderer = MockPromptRenderer()

        if output_format == "markdown":
            # In a real system, this would use a specific prompt for markdown generation
            generated_content = renderer.render_prompt("flippa", "listing_description", app_data)
            output_filename = os.path.join("portfolio-publisher", "output", f"{app_id.lower()}_{app_data["name"].lower().replace(" ", "_")}.md")
            with open(output_filename, "w") as f:
                f.write(generated_content)
            print(f"Generated Markdown listing for {app_id} at {output_filename}")
        else:
            print(f"Unsupported output format: {output_format}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Portfolio Publisher CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a Flippa listing")
    generate_parser.add_argument("app_id", type=str, help="ID of the app to generate (e.g., A01)")
    generate_parser.add_argument("--format", type=str, default="markdown", help="Output format (e.g., markdown)")
    generate_parser.set_defaults(func=lambda args: generate_listing(args.app_id, args.format))

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

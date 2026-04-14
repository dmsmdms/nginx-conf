#!/bin/python

from jinja2 import Environment, FileSystemLoader
import argparse
import tomllib
import sys

def main():
    parser = argparse.ArgumentParser(description="Nginx config generator from TOML")
    parser.add_argument("config", help="Path to the J2 template file (e.g., nginx.conf.j2)")
    parser.add_argument("input", help="Path to input TOML file (e.g., apps.toml)")
    parser.add_argument("output", help="Path to output Nginx config (e.g., nginx.conf)")
    
    args = parser.parse_args()

    try:
        # 1. Read the TOML configuration
        with open(args.input, "rb") as f:
            config_data = tomllib.load(f)

        # 2. Initialize Jinja2 (look for templates in the current directory)
        env = Environment(loader=FileSystemLoader('.'))
        # The template file name can also be passed as an argument if needed
        template = env.get_template(args.config)

        # 3. Render the data into the template
        rendered_config = template.render(
            apps=config_data.get('apps', []),
            binpkg=config_data.get('binpkg', {})
        )

        # 4. Write the result to the output file
        with open(args.output, "w") as f:
            f.write(rendered_config)

        print(f"Successfully generated: {args.input} -> {args.output}")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

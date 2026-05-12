#!/bin/python

from jinja2 import Environment, FileSystemLoader
import argparse
import tomllib
import sys
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Nginx config generator from TOML")
    parser.add_argument("config", help="Path to input TOML file (e.g., apps.toml)")
    parser.add_argument("input", help="Path to the J2 template file (e.g., nginx.conf.j2)")
    parser.add_argument("output", help="Path to output Nginx config (e.g., nginx.conf)")
    
    args = parser.parse_args()

    try:
        # 1. Read the TOML configuration
        with open(args.config, "rb") as f:
            config_data = tomllib.load(f)

        # 2. Initialize Jinja2
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(args.input)

        # 3. Render the data into the template
        rendered_config = template.render(
            apps=config_data.get('apps', []),
            binpkg=config_data.get('binpkg', {}),
            app_languages=config_data.get('app_languages') # Не забудь добавить в TOML, если нужно
        )

        # 4. Форматирование через nginxfmt
        # Используем путь к venv, который ты указал
        fmt_path = "./venv/bin/nginxfmt"
        
        # Запускаем процесс, передавая конфиг через stdin (-)
        process = subprocess.Popen(
            [fmt_path, "--max-empty-lines", "1", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        formatted_config, error = process.communicate(input=rendered_config)

        if process.returncode != 0:
            print(f"Warning: nginxfmt error: {error}")
            # Если форматирование упало, записываем сырой конфиг, чтобы не терять данные
            final_output = rendered_config
        else:
            final_output = formatted_config

        # 5. Write the result to the output file
        with open(args.output, "w") as f:
            f.write(final_output)

        print(f"Successfully generated and formatted: {args.input} -> {args.output}")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
FEDORO OS - Kickstart Flattener and Syntax Validator
Processes %include statements and verifies kickstart semantics using pykickstart.
"""

import sys
import os
import re
from pykickstart.parser import KickstartParser
from pykickstart.version import makeVersion


def resolve_includes(filepath, visited=None):
    if visited is None:
        visited = set()

    abs_path = os.path.abspath(filepath)
    if abs_path in visited:
        print(f"Warning: Circular include detected for {filepath}", file=sys.stderr)
        return ""
    visited.add(abs_path)

    base_dir = os.path.dirname(abs_path)
    output_lines = []

    with open(abs_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^\s*%include\s+(.+)$", line)
            if match:
                inc_target = match.group(1).strip()
                inc_path = inc_target if os.path.isabs(inc_target) else os.path.join(base_dir, inc_target)
                if not os.path.exists(inc_path):
                    raise FileNotFoundError(f"Included kickstart file not found: {inc_path}")
                output_lines.append(f"# --- Begin %include {inc_target} ---\n")
                output_lines.append(resolve_includes(inc_path, visited))
                output_lines.append(f"# --- End %include {inc_target} ---\n")
            else:
                output_lines.append(line)

    return "".join(output_lines)


def validate_kickstart_content(content):
    version = makeVersion()
    parser = KickstartParser(version)
    parser.readKickstartFromString(content)
    return parser


def main():
    if len(sys.argv) < 2:
        print("Usage: flatten_ks.py <input.ks> [output.ks]")
        return 1

    input_ks = sys.argv[1]
    output_ks = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_ks):
        print(f"Error: Input file {input_ks} does not exist.", file=sys.stderr)
        return 1

    print(f"Flattening kickstart: {input_ks}...")
    try:
        flattened = resolve_includes(input_ks)
        print("Validating kickstart syntax with pykickstart...")
        parser = validate_kickstart_content(flattened)
        print("✓ Kickstart syntax is valid.")
    except Exception as e:
        print(f"✗ Kickstart validation error: {e}", file=sys.stderr)
        return 2

    if output_ks:
        with open(output_ks, "w", encoding="utf-8") as f:
            f.write(flattened)
        print(f"✓ Output written to: {output_ks}")
    else:
        print(flattened)

    return 0


if __name__ == "__main__":
    sys.exit(main())

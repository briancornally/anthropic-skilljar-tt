#!/usr/bin/env python3
import sys
import os


def create_structure(overview_file, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(overview_file))
    heading_counter = 0
    file_counter = 0
    current_dir = None
    with open(overview_file) as f:
        for raw in f:
            line = raw.rstrip('\n')
            if line.startswith('# '):
                heading_counter += 1
                file_counter = 0
                dir_name = f"{heading_counter:02d} {line[2:].strip()}"
                current_dir = os.path.join(output_dir, dir_name)
                os.makedirs(current_dir, exist_ok=True)
            elif line.strip() and current_dir is not None:
                file_counter += 1
                path = os.path.join(current_dir, f"{file_counter:02d} {line.strip()}.md")
                open(path, 'w').close()


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'overview.md'
    dst = sys.argv[2] if len(sys.argv) > 2 else None
    create_structure(src, dst)

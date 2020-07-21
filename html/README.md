# Automated HTML generation

### Prerequisite

Nothing

### Usage

`python html_gen {path_to_instruction} {task}`

path_to_instruction is the path to a file containing html format instructions.

task is the name of the task (now only breakdown is supported, to add support, add entries to the dictionaries in html_gen.py)

```
optional arguments:
    -n              number of questions (default 5)
    --out_dir       path to the directory where to write output (default './hits')
```
import re
import sys
import os


def validate_filename(filepath):
    filename = os.path.basename(filepath)
    pattern = r'^\d{4}-\d{2}-\d{2}-[\w-]+\.md$'
    if not re.match(pattern, filename):
        return False, f"Filename '{filename}' does not match pattern YYYY-MM-DD-kebab-case.md"
    return True, "Filename format correct"


def parse_front_matter(content):
    match = re.match(r'^---\n(.*?)\n---\n?(.*)', content, re.DOTALL)
    if not match:
        return None, "File must start with YAML front matter (---...---)"

    fm_text = match.group(1)
    body = match.group(2)

    # Extract top-level keys (handles multi-line values like `description: >-`)
    fm = {}
    for m in re.finditer(r'^(\w[\w-]*)\s*:\s*(.*)', fm_text, re.MULTILINE):
        fm[m.group(1)] = m.group(2).strip()

    return fm, body


def validate_front_matter(fm):
    errors = []
    warnings = []

    required_keys = ['title', 'date', 'categories', 'tags']
    missing = [k for k in required_keys if k not in fm]
    if missing:
        errors.append(f"Missing required keys: {', '.join(missing)}")

    recommended_keys = ['description', 'comments']
    missing_rec = [k for k in recommended_keys if k not in fm]
    if missing_rec:
        warnings.append(f"Missing recommended keys: {', '.join(missing_rec)}")

    # Check description length
    if 'description' in fm:
        desc = fm['description']
        # Remove YAML multi-line indicators
        desc = desc.lstrip('>-').strip().strip('"').strip("'")
        if len(desc) > 160:
            warnings.append(f"Description is {len(desc)} chars (recommended < 160)")

    # Check title length (warning only — existing posts have longer titles)
    if 'title' in fm:
        title = fm['title'].strip('"').strip("'")
        if len(title) > 60:
            warnings.append(f"Title is {len(title)} chars (recommended < 60 for SEO)")

    return errors, warnings


def validate_content(body):
    issues = []

    # Check for H1 usage in body, ignoring code blocks
    in_code_block = False
    for line in body.split('\n'):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        if not in_code_block and re.match(r'^# [^#]', line):
            issues.append(f"Found H1 (#) in body: '{line.strip()}'. "
                          "Chirpy uses title from front matter as H1. Use ## for sections.")

    # Check image paths
    images = re.findall(r'!\[.*?\]\((.*?)\)', body)
    for img in images:
        if not img.startswith('/assets/img/') and not img.startswith('http'):
            issues.append(f"Image '{img}' should use /assets/img/ path")

    # Suggestions (non-blocking)
    suggestions = []
    if '{: .prompt-' not in body:
        suggestions.append("Consider adding Chirpy callouts ({: .prompt-tip }, {: .prompt-info }, etc.)")

    if '[^fn-' not in body and '[^' not in body:
        suggestions.append("Consider adding footnotes for source references")

    if issues:
        return False, "; ".join(issues), suggestions
    return True, "Content structure looks good", suggestions


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_blog_post.py <path_to_post.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    print(f"Validating {filepath}...\n")
    all_passed = True

    # 1. Validate Filename
    passed, msg = validate_filename(filepath)
    print(f"[{'PASS' if passed else 'FAIL'}] Filename: {msg}")
    if not passed:
        all_passed = False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # 2. Parse and Validate Front Matter
    fm, body_or_err = parse_front_matter(content)
    if fm is None:
        print(f"[FAIL] Front Matter: {body_or_err}")
        all_passed = False
    else:
        errors, warnings = validate_front_matter(fm)
        if errors:
            print(f"[FAIL] Front Matter: {'; '.join(errors)}")
            all_passed = False
        else:
            print("[PASS] Front Matter: Required keys present")

        if warnings:
            for w in warnings:
                print(f"[WARN] Front Matter: {w}")

        # 3. Validate Content
        passed, msg, suggestions = validate_content(body_or_err)
        print(f"[{'PASS' if passed else 'FAIL'}] Content: {msg}")
        if not passed:
            all_passed = False

        # Print suggestions
        if suggestions:
            print(f"\n[SUGGESTIONS]")
            for s in suggestions:
                print(f"  - {s}")

    print("\n" + ("=" * 40))
    if all_passed:
        print("SUCCESS: Post meets all requirements!")
        sys.exit(0)
    else:
        print("FAILURE: Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

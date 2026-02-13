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
    if not content.startswith('---\n'):
        return None, "File must start with YAML front matter (---)"
    
    parts = content.split('---\n')
    # parts[0] is empty (before first ---)
    # parts[1] is front matter
    # parts[2:] is body (joined back)
    
    if len(parts) < 3:
        return None, "Front matter not properly closed with ---"
    
    fm_content = parts[1]
    body = '---\n'.join(parts[2:])
    
    fm = {}
    for line in fm_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()
            
    return fm, body

def validate_front_matter(fm):
    required_keys = ['title', 'date', 'categories', 'tags']
    missing = [k for k in required_keys if k not in fm]
    if missing:
        return False, f"Missing front matter keys: {', '.join(missing)}"
    return True, "Front matter keys present"

def validate_content(body):
    issues = []
    
    # Check for H1 usage in body, ignoring code blocks
    in_code_block = False
    for line in body.split('\n'):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        if not in_code_block and line.strip().startswith('# '):
             issues.append(f"Found H1 (#) in body: '{line.strip()}'. Use H2 (##) for top-level sections.")

    # Check image paths
    images = re.findall(r'!\[.*?\]\((.*?)\)', body)
    for img in images:
        if not img.startswith('/') and not img.startswith('assets/img/') and not img.startswith('http'):
             issues.append(f"Image '{img}' should likely start with /assets/img/ or assets/img/")

    # Check for Chirpy callouts (Just as a suggestion/check)
    if '{: .prompt-' not in body:
        issues.append("Recommendation: No Chirpy callouts found (e.g., {: .prompt-tip }). Consider adding them.")

    if issues:
        return False, "; ".join(issues)
    return True, "Content structure looks good"

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
    if not passed: all_passed = False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # 2. Validate Front Matter
    fm, body_or_err = parse_front_matter(content)
    if fm is None:
        print(f"[FAIL] Front Matter: {body_or_err}")
        all_passed = False
    else:
        passed, msg = validate_front_matter(fm)
        print(f"[{'PASS' if passed else 'FAIL'}] Front Matter: {msg}")
        if not passed: all_passed = False
        
        # 3. Validate Content
        passed, msg = validate_content(body_or_err)
        print(f"[{'PASS' if passed else 'FAIL'}] Content: {msg}")
        if not passed: all_passed = False

    print("\n" + ("="*30))
    if all_passed:
        print("SUCCESS: Post meets all core requirements!")
        sys.exit(0)
    else:
        print("FAILURE: Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

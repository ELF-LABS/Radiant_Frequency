import os
import re
from urllib.parse import unquote

# Configuration
ROOT_DIR = r"C:\Users\ELF\Desktop\RADIANT_WEB"
PAGES_DIR = os.path.join(ROOT_DIR, "pages")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
INDEX_FILE = os.path.join(ROOT_DIR, "index.html")

# Expected Themes
THEME_MAP = {
    'vision.html': 'theme-vision',
    'security.html': 'theme-security',
    'architecture.html': 'theme-architecture',
    'science.html': 'theme-science',
    'arts.html': 'theme-arts',
    'physical.html': 'theme-physical',
    'integration.html': 'theme-integration',
    'soul.html': 'theme-soul',
    'reciprocity.html': 'theme-reciprocity',
    'development.html': 'theme-development',
    'donate.html': 'theme-donate',
    'contact.html': 'theme-contact',
    'faq.html': 'theme-faq',
    'volunteer.html': 'theme-volunteer'
}

def check_file_exists(path):
    return os.path.exists(path)

def scan_html_file(file_path):
    issues = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    filename = os.path.basename(file_path)
    
    # 1. Check Theme Class
    if filename in THEME_MAP:
        expected_theme = THEME_MAP[filename]
        if f'class="{expected_theme}"' not in content and f"class='{expected_theme}'" not in content:
             issues.append(f"[THEME] Body missing expected class '{expected_theme}'")

    # 2. Check Links
    links = re.findall(r'href=["\'](.*?)["\']', content)
    for link in links:
        if link.startswith('http') or link.startswith('mailto') or link.startswith('#'):
            continue
            
        # Resolve relative paths
        if filename == 'index.html':
            target_path = os.path.normpath(os.path.join(ROOT_DIR, link))
        else:
            target_path = os.path.normpath(os.path.join(PAGES_DIR, link))
            
        if not check_file_exists(target_path):
            issues.append(f"[LINK] Broken link to '{link}'")

    # 3. Check Images
    images = re.findall(r'src=["\'](.*?)["\']', content)
    for img in images:
        if img.startswith('http'): 
            continue
            
        # Resolve relative paths
        if filename == 'index.html':
            target_path = os.path.normpath(os.path.join(ROOT_DIR, img))
        else:
            target_path = os.path.normpath(os.path.join(PAGES_DIR, img))
            
        if not check_file_exists(target_path):
            issues.append(f"[IMAGE] Missing image '{img}'")

    # 4. Check Hero Image Existence Specifically (heuristic)
    if 'hero-image' in content:
        # Just ensure at least one image with class 'hero-image' exists
        if 'class="hero-image"' not in content and "class='hero-image'" not in content:
             issues.append("[HERO] Hero image class usage incorrect or missing.")

    return issues

def main():
    print("--- RADIANT FREQUENCY QA TRIAD ---")
    print(f"Scanning root: {ROOT_DIR}")
    
    all_issues = {}
    
    # Scan Index
    if os.path.exists(INDEX_FILE):
        issues = scan_html_file(INDEX_FILE)
        if issues: all_issues['index.html'] = issues
    else:
        print("CRITICAL: index.html not found!")
        
    # Scan Pages
    for page in os.listdir(PAGES_DIR):
        if page.endswith(".html"):
            path = os.path.join(PAGES_DIR, page)
            issues = scan_html_file(path)
            if issues: all_issues[page] = issues

    # Report
    if not all_issues:
        print("\n[SUCCESS] No bugs found. The Lattice is stable.")
    else:
        print(f"\n[ATTENTION] Found {sum(len(v) for v in all_issues.values())} issues:")
        for file, file_issues in all_issues.items():
            print(f"\nFile: {file}")
            for issue in file_issues:
                print(f"  - {issue}")

if __name__ == "__main__":
    main()

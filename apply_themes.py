import os
import re

# Map filenames to their theme class
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

PAGES_DIR = r"C:\Users\ELF\Desktop\RADIANT_WEB\pages"

def apply_theme(file_path, theme_class):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find <body ...> or <body>
    # We replace it with <body class="theme-name">
    # If a class already exists, we replace it.
    
    # 1. Simple Case: <body> -> <body class="...">
    if "class=" not in content.split("<body")[1].split(">")[0]:
         new_content = re.sub(r'<body>', f'<body class="{theme_class}">', content, count=1)
    else:
        # 2. Existing Class Case: <body class="old-class"> -> <body class="theme-name">
        # This is a bit brute force but effective for this specific project structure
        new_content = re.sub(r'<body class="[^"]+">', f'<body class="{theme_class}">', content, count=1)
    
    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file_path)} with {theme_class}")
    else:
        print(f"No changes needed for {os.path.basename(file_path)}")

def main():
    print("Applying Studio-Grade Themes...")
    for filename, theme_class in THEME_MAP.items():
        file_path = os.path.join(PAGES_DIR, filename)
        if os.path.exists(file_path):
            apply_theme(file_path, theme_class)
        else:
            print(f"Warning: {filename} not found.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Archetype Page Builder
Generates individual HTML pages for each of the 12 core archetypes
from the archetype_definitions.json file.
"""

import json
import os
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROTOCOLS_DIR = PROJECT_ROOT / "_PROTOCOLS"
PAGES_DIR = PROJECT_ROOT / "pages"
ARCHETYPE_JSON = PROTOCOLS_DIR / "archetype_definitions.json"

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | Radiant Frequency</title>
    <link rel="stylesheet" href="../css/style.css">
</head>

<body class="theme-vision">
    <div class="container">
        <div class="hero-container">
            <img src="../assets/images/vision_hero.png" alt="{name} Archetype" class="hero-image">
            <div class="hero-overlay"></div>
        </div>
        <div class="nav-controls">
            <a href="archetypes.html" class="back-button" style="margin-bottom: 0;">❖ Back to Archetypes</a>
        </div>

        <header style="text-align: center; margin-bottom: 50px;">
            <h1 class="page-title" style="color: {color};">{name}</h1>
            <p class="subtitle">{tagline}</p>
        </header>

        <section class="content-section">
            <!-- Origin Story -->
            <div style="margin-bottom: 50px;">
                <h2 style="color: {color}; margin-bottom: 20px;">Origin</h2>
                <p style="line-height: 1.8; font-size: 1.1rem;">
                    {origin}
                </p>
            </div>

            <!-- Strengths -->
            <div style="margin-bottom: 50px;">
                <h2 style="color: {color}; margin-bottom: 20px;">Strengths</h2>
                <ul style="line-height: 1.8; font-size: 1.05rem; list-style-position: inside;">
{strengths_html}
                </ul>
            </div>

            <!-- Shadows -->
            <div style="margin-bottom: 50px;">
                <h2 style="color: {color}; margin-bottom: 20px;">Shadows & Weaknesses</h2>
                <ul style="line-height: 1.8; font-size: 1.05rem; list-style-position: inside;">
{shadows_html}
                </ul>
            </div>

            <!-- How to Embody -->
            <div style="margin-bottom: 50px; padding: 30px; background: rgba(255,255,255,0.03); border-radius: 16px; border-left: 4px solid {color};">
                <h2 style="color: {color}; margin-bottom: 20px;">How to Embody This Archetype</h2>
                <p style="line-height: 1.8; font-size: 1.1rem;">
                    {how_to_embody}
                </p>
            </div>

            <!-- AI Companion Note -->
            <div style="margin-top: 60px; padding: 30px; background: rgba(255,255,255,0.03); border-radius: 16px; text-align: center;">
                <h3 style="color: var(--primary-color); margin-bottom: 15px;">Your AI Companion</h3>
                <p style="line-height: 1.6; opacity: 0.9;">
                    When you choose <strong style="color: {color};">{name}</strong> as your archetype, your AI companion will adapt to support your unique strengths and help you navigate your shadows. Together, you'll build a partnership that honors who you are and who you're becoming.
                </p>
            </div>
        </section>
    </div>

    <script>
        // Mirror top navigation to bottom
        const topNav = document.querySelector('.nav-controls');
        if (topNav) {{
            const bottomNav = topNav.cloneNode(true);
            bottomNav.style.marginTop = '60px';
            document.querySelector('.container').appendChild(bottomNav);
        }}
    </script>
</body>

</html>
"""


def load_archetype_data():
    """Load archetype definitions from JSON file."""
    with open(ARCHETYPE_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['archetypes']


def generate_list_html(items):
    """Convert a list of items to HTML list items."""
    return '\n'.join([f'                    <li>{item}</li>' for item in items])


def generate_archetype_page(archetype):
    """Generate an HTML page for a single archetype."""
    # Prepare data
    strengths_html = generate_list_html(archetype['strengths'])
    shadows_html = generate_list_html(archetype['shadows'])
    
    # Fill template
    html = HTML_TEMPLATE.format(
        name=archetype['name'],
        tagline=archetype['tagline'],
        color=archetype['color'],
        origin=archetype['origin'],
        strengths_html=strengths_html,
        shadows_html=shadows_html,
        how_to_embody=archetype['how_to_embody']
    )
    
    # Write to file
    filename = f"{archetype['id']}.html"
    output_path = PAGES_DIR / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated: {filename}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("ARCHETYPE PAGE BUILDER")
    print("=" * 60)
    print()
    
    # Load data
    print("Loading archetype definitions...")
    archetypes = load_archetype_data()
    print(f"Found {len(archetypes)} archetypes")
    print()
    
    # Generate pages
    print("Generating pages...")
    for archetype in archetypes:
        generate_archetype_page(archetype)
    
    print()
    print("=" * 60)
    print(f"SUCCESS: Generated {len(archetypes)} archetype pages")
    print("=" * 60)


if __name__ == "__main__":
    main()

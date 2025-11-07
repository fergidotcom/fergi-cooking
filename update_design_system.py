#!/usr/bin/env python3
"""
Update all HTML files with the v4.0 design system CSS variables
"""

import re

# New CSS variables with design system
NEW_CSS_VARS = """        :root {
            /* Primary colors */
            --color-primary: #3b82f6;
            --color-secondary: #f59e0b;
            --color-success: #10b981;
            --color-warning: #f59e0b;
            --color-danger: #ef4444;

            /* Neutrals */
            --color-bg: #ffffff;
            --color-bg-secondary: #f3f4f6;
            --color-bg-tertiary: #e5e7eb;
            --color-border: #e5e7eb;
            --color-text: #1f2937;
            --color-text-light: #6b7280;
            --color-text-lighter: #9ca3af;

            /* Spacing (8px base) */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;

            /* Shadows */
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);

            /* Border radius */
            --radius-sm: 0.25rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
            --radius-full: 9999px;

            /* Typography */
            --font-xs: 0.75rem;
            --font-sm: 0.875rem;
            --font-base: 1rem;
            --font-lg: 1.125rem;
            --font-xl: 1.25rem;
            --font-2xl: 1.5rem;
            --font-3xl: 1.875rem;
            --font-4xl: 2.25rem;

            --font-normal: 400;
            --font-medium: 500;
            --font-semibold: 600;
            --font-bold: 700;

            /* Legacy mappings */
            --primary-color: var(--color-primary);
            --secondary-color: var(--color-danger);
            --accent-color: var(--color-primary);
            --success-color: var(--color-success);
            --background: var(--color-bg-secondary);
            --card-background: var(--color-bg);
            --text-color: var(--color-text);
            --text-muted: var(--color-text-light);
            --shadow: var(--shadow-md);
            --shadow-hover: var(--shadow-lg);
            --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }"""

# Files to update
files = ['event-detail.html', 'respond.html', 'add-recipe.html']

# Pattern to match old :root block
pattern = r':root\s*\{[^}]+\}'

for filename in files:
    try:
        with open(filename, 'r') as f:
            content = f.read()

        # Replace the :root block
        updated_content = re.sub(pattern, NEW_CSS_VARS.strip(), content)

        with open(filename, 'w') as f:
            f.write(updated_content)

        print(f"✅ Updated {filename}")
    except Exception as e:
        print(f"❌ Error updating {filename}: {e}")

print("\n✅ Design system update complete!")

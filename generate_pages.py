#!/usr/bin/env python3
"""
UVA Computer Science Archive Page Generator
-------------------------------------------
Generates HTML pages for student presentations based on a CSV file
containing student data. This creates a static website structure that
preserves the original URL paths where backlinks are pointing.
"""

import os
import csv
from string import Template
import sys

# Configuration
CSV_FILE = 'student_presentations.csv'

# Template for student pages with thesis titles
TEMPLATE_WITH_TITLE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${name} - ${title} | UVA Computer Science Archive</title>
    <meta name="description" content="Archived record of ${name}'s ${type} at the University of Virginia Computer Science Department on ${date_formatted}.">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1>${name}</h1>
        <h2>${type}</h2>
    </header>
    
    <section class="meta">
        <p><strong>Date:</strong> ${date_formatted}</p>
        <p><strong>Location:</strong> ${location}, University of Virginia</p>
        <p><strong>Title:</strong> ${title}</p>
    </section>
    
    <div class="archive-notice">
        <p>This page is part of an independent academic archive initiative, preserving records of public presentations from the University of Virginia's Computer Science Department.</p>
    </div>
    
    <section class="abstract">
        <p>${abstract}</p>
    </section>
    
    <section class="details">
        <p>This archival record preserves the announcement of ${name}'s ${type} at the University of Virginia. ${explanation}</p>
        
        <p>${field_relevance}</p>
    </section>
    
    <footer>
        <p>Archival Record: ${type} from ${date_formatted}</p>
        <p>This archive is independently maintained and not affiliated with the University of Virginia.</p>
        <p>Preserved for academic and historical reference purposes only.</p>
        <p>Powered by <a href="https://agentius.ai" target="_blank" rel="nofollow">Agentius</a></p>
    </footer>
</body>
</html>""")

# Template for student pages without thesis titles
TEMPLATE_WITHOUT_TITLE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${name} - ${type} | UVA Computer Science Archive</title>
    <meta name="description" content="Archived record of ${name}'s ${type} at the University of Virginia Computer Science Department on ${date_formatted}.">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <h1>${name}</h1>
        <h2>${type}</h2>
    </header>
    
    <section class="meta">
        <p><strong>Date:</strong> ${date_formatted}</p>
        <p><strong>Location:</strong> ${location}, University of Virginia</p>
    </section>
    
    <div class="archive-notice">
        <p>This page is part of an independent academic archive initiative, preserving records of public presentations from the University of Virginia's Computer Science Department.</p>
    </div>
    
    <section class="details">
        <p>This page mirrors the archived announcement of ${name}'s ${type} presented at the University of Virginia Computer Science Department. ${explanation}</p>
        
        <p>${field_relevance}</p>
    </section>
    
    <footer>
        <p>Archival Record: ${type} from ${date_formatted}</p>
        <p>This archive is independently maintained and not affiliated with the University of Virginia.</p>
        <p>Preserved for academic and historical reference purposes only.</p>
        <p>Powered by <a href="https://agentius.ai" target="_blank" rel="nofollow">Agentius</a></p>
    </footer>
</body>
</html>""")

# Explanations by presentation type
EXPLANATIONS = {
    'PhD Dissertation Defense': 'The dissertation defense represents the culmination of doctoral research, where candidates present and defend their original contribution to the field before their dissertation committee.',
    'PhD Dissertation Defense Presentation': 'The dissertation defense represents the culmination of doctoral research, where candidates present and defend their original contribution to the field before their dissertation committee.',
    'Dissertation Defense': 'The dissertation defense represents the culmination of doctoral research, where candidates present and defend their original contribution to the field before their dissertation committee.',
    'PhD Proposal': 'The proposal presentation is a crucial milestone where PhD candidates outline their research plans and methodology for their dissertation work.',
    'PhD Proposal Presentation': 'The proposal presentation is a crucial milestone where PhD candidates outline their research plans and methodology for their dissertation work.',
    'PhD Qualifying Exam Presentation': 'The qualifying exam is a significant milestone in the PhD program, demonstrating a candidate\'s comprehensive understanding of their research area and readiness to proceed with dissertation research.',
    'Qualifying Exam Presentation': 'The qualifying exam is a significant milestone in the PhD program, demonstrating a candidate\'s comprehensive understanding of their research area and readiness to proceed with dissertation research.',
    'Master\'s Project Presentation': 'The master\'s project presentation represents the culmination of graduate-level research, where students demonstrate mastery of their specialized area within computer science.'
}

# Field relevance statements by research areas (you can expand this)
FIELD_RELEVANCE = {
    'algorithms': 'Algorithm research continues to be a foundational aspect of computer science, with applications spanning from basic data structures to complex computational systems.',
    'ai': 'Artificial intelligence remains a critical area of computer science research, with applications spanning from small-scale systems to enterprise-level frameworks.',
    'systems': 'Systems research addresses fundamental challenges in computer architecture, networking, and operating systems that enable modern computing infrastructure.',
    'security': 'Security research tackles increasingly complex threats in our interconnected digital world, developing novel protections for systems, networks, and data.',
    'data': 'Data-focused research explores innovative methods for processing, analyzing, and extracting insights from increasingly large and complex datasets.',
    'default': 'This area of computer science research continues to advance our understanding of computational methods and their applications in solving real-world problems.'
}

def format_date(date_str):
    """Convert YYYY-MM-DD to Month Day, Year format"""
    from datetime import datetime
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%B %d, %Y')

def get_field_relevance(title):
    """Determine field relevance based on title keywords"""
    if not title:
        return FIELD_RELEVANCE['default']
    
    title_lower = title.lower()
    
    if any(kw in title_lower for kw in ['algorithm', 'computational', 'scalable']):
        return FIELD_RELEVANCE['algorithms']
    elif any(kw in title_lower for kw in ['neural', 'learning', 'ai', 'classification', 'deep']):
        return FIELD_RELEVANCE['ai']
    elif any(kw in title_lower for kw in ['system', 'architecture', 'network']):
        return FIELD_RELEVANCE['systems']
    elif any(kw in title_lower for kw in ['security', 'privacy', 'authentication']):
        return FIELD_RELEVANCE['security']
    elif any(kw in title_lower for kw in ['data', 'e-commerce', 'personalization']):
        return FIELD_RELEVANCE['data']
    else:
        return FIELD_RELEVANCE['default']

def generate_abstract(title, type_str):
    """Generate a simple abstract based on the title"""
    if not title:
        return ""
    
    if "Dissertation" in type_str:
        return f"The dissertation explores approaches to {title.lower() if not title.endswith('.') else title.lower()[:-1]}. The research addresses challenges in this area and contributes new methodologies to the field of computer science."
    else:
        return f"This presentation examines {title.lower() if not title.endswith('.') else title.lower()[:-1]}. The research investigates key challenges in this domain and proposes novel approaches."

def create_page(row):
    """Create an HTML page for a student presentation"""
    # Extract data
    name = row['Name']
    type_str = row['Type']
    date = row['Date']
    title = row.get('Title', '')
    url_path = row['URL_Path']
    location = row.get('Location', 'Rice Hall')
    
    # Create formatted values
    date_formatted = format_date(date)
    explanation = EXPLANATIONS.get(type_str, 'This presentation represents an important milestone in the academic journey of computer science researchers.')
    field_relevance = get_field_relevance(title)
    abstract = generate_abstract(title, type_str)
    
    # Create directory structure
    dir_path = os.path.join(url_path)
    os.makedirs(dir_path, exist_ok=True)
    
    # Choose template based on whether title exists
    if title:
        html_content = TEMPLATE_WITH_TITLE.substitute(
            name=name,
            type=type_str,
            date=date,
            date_formatted=date_formatted,
            title=title,
            location=location,
            explanation=explanation,
            field_relevance=field_relevance,
            abstract=abstract
        )
    else:
        html_content = TEMPLATE_WITHOUT_TITLE.substitute(
            name=name,
            type=type_str,
            date=date,
            date_formatted=date_formatted,
            location=location,
            explanation=explanation,
            field_relevance=field_relevance
        )
    
    # Write HTML file
    with open(os.path.join(dir_path, 'index.html'), 'w') as f:
        f.write(html_content)
        
    print(f"Created page: {url_path}")

def main():
    """Main function to process the CSV and generate pages"""
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        sys.exit(1)
        
    # Read CSV and generate pages
    with open(CSV_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            create_page(row)
    
    print(f"Generated all pages.")

if __name__ == "__main__":
    main()

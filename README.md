# UVA Computer Science Academic Archive

This repository contains the static website for the UVA Computer Science Academic Archive, an independent collection preserving historical records of computer science presentations from the University of Virginia.

## Overview

The UVA Computer Science Academic Archive serves to preserve public presentations from University of Virginia Computer Science graduate students, including PhD dissertation defenses, proposals, and qualifying exams. The content is maintained for historical reference and academic documentation purposes.

## Repository Structure
fmfg03/uvacsarch/
├── index.html                      # Main landing page
├── robots.txt                      # Allow search engines to crawl
├── sitemap.xml                     # List all preserved pages
├── 404.html                        # Simple error page
├── css/
│   └── style.css                   # Minimal styling for academic look
├── 2016/                           # Year directories
│   └── (student presentation pages)
├── 2017/
│   └── (student presentation pages)
└── student-presentations/          # Archive index page
└── index.html
## Setup and Deployment

This site is designed to be deployed as a static website through Cloudflare Pages, connected to this GitHub repository. No build process is needed, as the site consists entirely of static HTML, CSS, and minimal assets.

### Local Development

To work on this site locally:

1. Clone the repository:
git clone https://github.com/fmfg03/uvacsarch.git
cd uvacsarch
2. Open files in your preferred editor or IDE

3. For local testing, you can use any static file server. For example, with Python:
If you have Python 3 installed
python -m http.server
Then visit `http://localhost:8000` in your browser

### Content Generation

The site contents can be generated using the included Python script:

1. Ensure you have Python 3.x installed
2. Update the `student_presentations.csv` file with any new entries
3. Run the script: `python generate_pages.py`
4. The script will generate HTML files for all presentations in the output directory

## Maintenance

### Adding New Pages

While this archive is primarily historical, if new pages need to be added:

1. Add the new entry to `student_presentations.csv`
2. Run the generator script
3. Move the resulting files to the appropriate directory in the repository
4. Update `sitemap.xml` and any index pages

### SEO Considerations

The site structure is designed to preserve the original URL paths where backlinks are pointing. Each page has:

- Unique titles and descriptions
- Proper heading structure
- Academic-style formatting
- Contextual internal linking

## License and Attribution

This is an independent archive not affiliated with the University of Virginia. All content is maintained for historical and academic reference purposes only.

## Contact

For questions or issues related to this archive, please open an issue in this repository.

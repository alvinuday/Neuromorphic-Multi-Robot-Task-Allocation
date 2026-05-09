#!/usr/bin/env python3
"""
Generate Interactive HTML Version of Master's Thesis
With embedded Plotly interactive figures and professional styling
"""

import os
import glob
from pathlib import Path
import json

class ThesisHTMLGenerator:
    def __init__(self, thesis_dir="ThesisDocument"):
        self.thesis_dir = thesis_dir
        self.figures_dir = Path(thesis_dir) / "Figures"
        self.output_dir = Path(thesis_dir) / "html_output"
        self.output_dir.mkdir(exist_ok=True)

        # Color scheme from thesis
        self.colors = {
            'primary_blue': '#1B4F72',
            'secondary_orange': '#D35400',
            'accent_green': '#1E8449',
            'accent_red': '#C0392B',
            'neutral_gray': '#566573',
            'light_gray': '#ECF0F1',
        }

        # Thesis metadata
        self.metadata = {
            'title': 'Bits to Atoms: Neuromorphic Computing for Physical Intelligence in Industrial Robotics',
            'subtitle': 'A Study in OIM-Based Coalition Task Allocation and SNN-Based Model Predictive Control for Robotic Systems',
            'author': 'Alvin Adarsh Kumar',
            'institution': 'BITS Pilani',
            'supervisors': ['Dhruv Kumar (BITS Pilani)', 'Debanjan Bhowmik (IIT Bombay)'],
            'date': 'May 2026',
            'degree': 'Master of Science in Physics',
        }

    def generate_html_header(self):
        """Generate HTML header with styling"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.metadata['title']}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'TeX Gyre Pagella', Georgia, serif;
            line-height: 1.6;
            color: #2c3e50;
            background-color: #fff;
        }}

        .header {{
            background: linear-gradient(135deg, {self.colors['primary_blue']} 0%, {self.colors['secondary_orange']} 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }}

        .header .subtitle {{
            font-size: 1.2rem;
            font-style: italic;
            margin-bottom: 1.5rem;
            opacity: 0.95;
        }}

        .header .metadata {{
            font-size: 0.9rem;
            opacity: 0.9;
            margin-top: 1rem;
        }}

        .metadata-item {{
            margin: 0.3rem 0;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        nav {{
            background-color: {self.colors['primary_blue']};
            padding: 1rem;
            margin-bottom: 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        nav ul {{
            list-style: none;
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        nav a {{
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: background-color 0.3s;
        }}

        nav a:hover {{
            background-color: rgba(255,255,255,0.2);
        }}

        .chapter {{
            margin: 3rem 0;
            padding: 2rem;
            background: {self.colors['light_gray']};
            border-left: 5px solid {self.colors['primary_blue']};
            border-radius: 4px;
        }}

        .chapter h2 {{
            color: {self.colors['primary_blue']};
            font-size: 2rem;
            margin-bottom: 1.5rem;
            border-bottom: 2px solid {self.colors['secondary_orange']};
            padding-bottom: 0.5rem;
        }}

        .chapter h3 {{
            color: {self.colors['secondary_orange']};
            font-size: 1.5rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}

        .section {{
            margin: 2rem 0;
            padding: 1.5rem;
            background: white;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .figure-container {{
            margin: 2rem 0;
            padding: 1.5rem;
            background: white;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .figure-container h4 {{
            color: {self.colors['primary_blue']};
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }}

        .figure-container iframe {{
            width: 100%;
            height: 600px;
            border: 1px solid {self.colors['light_gray']};
            border-radius: 4px;
        }}

        .figure-caption {{
            font-size: 0.9rem;
            font-style: italic;
            color: {self.colors['neutral_gray']};
            margin-top: 0.5rem;
            padding: 0.5rem;
            border-top: 1px solid {self.colors['light_gray']};
        }}

        p {{
            margin-bottom: 1rem;
            text-align: justify;
        }}

        .math {{
            background: {self.colors['light_gray']};
            padding: 0.5rem;
            margin: 0.5rem 0;
            border-left: 3px solid {self.colors['accent_green']};
        }}

        .insight {{
            background: {self.colors['accent_green']}15;
            border-left: 4px solid {self.colors['accent_green']};
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }}

        .insight::before {{
            content: "💡 Key Insight: ";
            font-weight: bold;
            color: {self.colors['accent_green']};
        }}

        footer {{
            background-color: {self.colors['primary_blue']};
            color: white;
            padding: 2rem;
            text-align: center;
            margin-top: 3rem;
        }}

        footer p {{
            margin-bottom: 0.5rem;
        }}

        .toc {{
            background: white;
            padding: 1.5rem;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}

        .toc h3 {{
            color: {self.colors['primary_blue']};
            margin-bottom: 1rem;
        }}

        .toc ul {{
            list-style-position: inside;
        }}

        .toc li {{
            margin: 0.3rem 0;
        }}

        .toc a {{
            color: {self.colors['primary_blue']};
            text-decoration: none;
        }}

        .toc a:hover {{
            text-decoration: underline;
        }}

        .back-to-top {{
            text-align: center;
            margin: 2rem 0;
        }}

        .back-to-top a {{
            color: {self.colors['primary_blue']};
            text-decoration: none;
            padding: 0.5rem 1rem;
            border: 1px solid {self.colors['primary_blue']};
            border-radius: 4px;
            transition: background-color 0.3s;
        }}

        .back-to-top a:hover {{
            background-color: {self.colors['primary_blue']};
            color: white;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}

            nav ul {{
                flex-direction: column;
                gap: 0;
            }}

            nav a {{
                display: block;
                border-radius: 0;
            }}
        }}
    </style>
</head>
<body>
'''

    def generate_header_section(self):
        """Generate thesis header"""
        supervisors_html = '<br>'.join(self.metadata['supervisors'])
        return f'''
    <div class="header">
        <h1>{self.metadata['title']}</h1>
        <div class="subtitle">{self.metadata['subtitle']}</div>
        <div class="metadata">
            <div class="metadata-item"><strong>By:</strong> {self.metadata['author']}</div>
            <div class="metadata-item"><strong>Degree:</strong> {self.metadata['degree']}</div>
            <div class="metadata-item"><strong>Supervisors:</strong> {supervisors_html}</div>
            <div class="metadata-item"><strong>Institution:</strong> {self.metadata['institution']}</div>
            <div class="metadata-item"><strong>Date:</strong> {self.metadata['date']}</div>
        </div>
    </div>
'''

    def generate_navigation(self):
        """Generate navigation menu"""
        chapters = [
            ('intro', 'Introduction'),
            ('background', 'Background'),
            ('system', 'System Architecture'),
            ('cmrta', 'CMRTA-OIM'),
            ('snn', 'SNN-MPC'),
            ('results', 'Results'),
            ('india', 'Impact & Vision'),
            ('conclusion', 'Conclusion'),
        ]

        nav_items = ''.join([f'<li><a href="#{ch_id}">{ch_name}</a></li>' for ch_id, ch_name in chapters])
        return f'''
    <nav>
        <ul>
            {nav_items}
        </ul>
    </nav>
'''

    def generate_interactive_figure(self, figure_name, caption):
        """Generate HTML for an interactive Plotly figure"""
        html_file = self.figures_dir / f"{figure_name}.html"
        if html_file.exists():
            return f'''
    <div class="figure-container">
        <h4>{caption}</h4>
        <iframe src="../Figures/{figure_name}.html" frameborder="0"></iframe>
        <div class="figure-caption">Interactive figure - hover for details, click legend to toggle series</div>
    </div>
'''
        return ""

    def generate_toc(self):
        """Generate table of contents"""
        return '''
    <div class="container">
        <div class="toc">
            <h3>Table of Contents</h3>
            <ul>
                <li><a href="#intro">1. Introduction</a></li>
                <li><a href="#background">2. Literature Review and Background</a></li>
                <li><a href="#system">3. System Architecture: The Bits-to-Atoms Stack</a></li>
                <li><a href="#cmrta">4. Coalition MRTA with OIM</a></li>
                <li><a href="#snn">5. Model Predictive Control with SNNs</a></li>
                <li><a href="#results">6. Experimental Results</a></li>
                <li><a href="#india">7. Neuromorphic Manufacturing: India's Opportunity</a></li>
                <li><a href="#conclusion">8. Conclusion and Future Work</a></li>
            </ul>
        </div>
    </div>
'''

    def generate_chapter_sections(self):
        """Generate chapter sections with interactive figures"""
        chapters = [
            {
                'id': 'intro',
                'title': '1. Introduction',
                'content': '''
The integration of neuromorphic computing paradigms with multi-robot task allocation represents a fundamental shift in how we design systems for real-time autonomous operation. This thesis presents a unified hardware-software framework that exploits physics-native computation to solve two complementary problems in robotics: combinatorial task allocation and continuous model predictive control.
                ''',
                'figures': [
                    ('fig_1_1_timeline', 'Hardware-Algorithm Evolution Timeline'),
                    ('fig_1_3_energy_delay', 'Energy-Delay Product Comparison'),
                ]
            },
            {
                'id': 'background',
                'title': '2. Literature Review and Background',
                'content': '''
Understanding the convergence of three research frontiers—Ising machines, multi-robot task allocation, and neuromorphic computing—is essential to appreciating the novelty of this work.
                ''',
                'figures': [
                    ('fig_2_1_hardware_landscape', 'Neuromorphic Platforms Landscape'),
                ]
            },
            {
                'id': 'system',
                'title': '3. System Architecture: The Bits-to-Atoms Stack',
                'content': '''
The central design philosophy of this thesis rejects the Von Neumann separation of hardware and software. Instead, we propose a four-layer abstraction stack that integrates algorithm design with hardware architecture, enabling specialized neuromorphic processors to naturally solve domain-specific problems.
                ''',
                'figures': [
                    ('fig_3_2_tradeoff', 'Hardware-Problem Trade-off Space'),
                ]
            },
            {
                'id': 'cmrta',
                'title': '4. Coalition MRTA with Oscillator Ising Machines',
                'content': '''
Coalition formation for multi-robot task allocation is NP-hard in general, but the physics of coupled oscillators offers a naturally parallel, energy-efficient solution path. We present the mathematical mapping from MRTA to Ising formulations and demonstrate hardware implementation on OIM platforms.
                ''',
                'figures': []
            },
            {
                'id': 'snn',
                'title': '5. Model Predictive Control with Spiking Neural Networks',
                'content': '''
Real-time model predictive control requires solving quadratic programs at every control cycle. SNNs implement iterative optimization algorithms through their spike-based integration, achieving millisecond convergence with microwatt power consumption.
                ''',
                'figures': []
            },
            {
                'id': 'results',
                'title': '6. Experimental Results and Validation',
                'content': '''
We validate both the OIM-MRTA and SNN-MPC approaches on realistic robotic scenarios, demonstrating solution quality, timing guarantees, and energy efficiency metrics that justify specialization over universal computing.
                ''',
                'figures': []
            },
            {
                'id': 'india',
                'title': '7. Neuromorphic Manufacturing: India\'s Opportunity',
                'content': '''
India stands at a unique intersection of low-cost electronics manufacturing expertise and emerging neuromorphic computing needs. This chapter explores how India can lead in neuromorphic hardware production for the next two decades.
                ''',
                'figures': []
            },
            {
                'id': 'conclusion',
                'title': '8. Conclusion and Future Work',
                'content': '''
The Bits-to-Atoms framework demonstrates that rejecting Von Neumann universality in favor of specialized hardware-algorithm co-design can solve real problems in robotics. Future work will extend this to heterogeneous multi-robot teams and larger-scale neuromorphic systems.
                ''',
                'figures': []
            },
        ]

        sections = ''
        for ch in chapters:
            sections += f'''
    <div class="container">
        <div class="chapter" id="{ch['id']}">
            <h2>{ch['title']}</h2>
            <div class="section">
                <p>{ch['content'].strip()}</p>
            </div>
'''
            for fig_name, fig_caption in ch['figures']:
                sections += self.generate_interactive_figure(fig_name, fig_caption)

            sections += '''
            <div class="back-to-top">
                <a href="#top">↑ Back to Top</a>
            </div>
        </div>
    </div>
'''
        return sections

    def generate_footer(self):
        """Generate footer"""
        return '''
    <footer>
        <p><strong>Bits to Atoms: Neuromorphic Computing for Physical Intelligence</strong></p>
        <p>Master's Thesis - BITS Pilani, May 2026</p>
        <p><small>Interactive HTML version with embedded Plotly figures. For the complete thesis with appendices, see the PDF version.</small></p>
    </footer>
</body>
</html>
'''

    def generate(self):
        """Generate the complete HTML thesis"""
        html_content = (
            self.generate_html_header() +
            self.generate_header_section() +
            self.generate_navigation() +
            self.generate_toc() +
            self.generate_chapter_sections() +
            self.generate_footer()
        )

        # Save HTML file
        output_file = self.output_dir / "thesis.html"
        with open(output_file, 'w') as f:
            f.write(html_content)

        print(f"✓ Generated interactive HTML thesis: {output_file}")
        print(f"  - Professional styling with thesis color scheme")
        print(f"  - Embedded Plotly interactive figures")
        print(f"  - Responsive design for mobile and desktop")
        print(f"  - Sticky navigation for easy browsing")
        print(f"\nTo view: Open {output_file} in a web browser")

if __name__ == "__main__":
    generator = ThesisHTMLGenerator()
    generator.generate()

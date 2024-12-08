import subprocess
import os

def escape_latex(text):
    if not isinstance(text, str):
        return text
    replacements = {
        '&': r'\&', '%': r'\%', '_': r'\_', '#': r'\#',
        '{': r'\{', '}': r'\}', '\\': r'\textbackslash{}',
        '^': r'\^{}', '~': r'\~{}', '$': r'\$'
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

def get_latex(information):
    fullname = escape_latex(f"{information.get('firstName', 'Unknown')} {information.get('lastName', 'Unknown')}")
    email = escape_latex(information.get('email', 'your.email@example.com'))
    linkedin = f"https://www.linkedin.com/in/{escape_latex(information.get('username', 'unknown'))}"
    phone = escape_latex(information.get('phone', '(123) 456-7890'))
    summary = escape_latex(information.get('summary', ''))

    # Begin LaTeX document
    latex_content = f"""
    \\documentclass[letterpaper,11pt]{{article}}

    % Required Packages
    \\usepackage{{latexsym}}
    \\usepackage[empty]{{fullpage}}
    \\usepackage{{titlesec}}
    \\usepackage{{enumitem}}
    \\usepackage[hidelinks]{{hyperref}}
    \\usepackage[english]{{babel}}
    \\usepackage{{tabularx}}
    \\usepackage{{multicol}}
    \\usepackage{{xcolor}}

    % Custom Colors
    \\definecolor{{cvblue}}{{HTML}}{{0E5484}}
    \\definecolor{{darkcolor}}{{HTML}}{{0F4539}}

    % Font and Margin Adjustments
    \\usepackage{{charter}}
    \\addtolength{{\\oddsidemargin}}{{-0.6in}}
    \\addtolength{{\\evensidemargin}}{{-0.6in}}
    \\addtolength{{\\textwidth}}{{1.2in}}
    \\addtolength{{\\topmargin}}{{-0.7in}}
    \\addtolength{{\\textheight}}{{1.4in}}

    % Section Formatting
    \\titleformat{{\\section}}{{\\vspace{{-5pt}}\\scshape\\large\\bfseries\\color{{cvblue}}}}{{}}{{0em}}{{}}[\\titlerule\\vspace{{-5pt}}]

    % Custom Commands
    \\newcommand{{\\resumeItem}}[1]{{\\item\\small{{#1\\vspace{{-2pt}}}}}}
    \\newcommand{{\\resumeSubheading}}[4]{{\\item
        \\begin{{tabular*}}{{\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
        \\textbf{{#1}} & \\textbf{{#2}} \\\\
        \\textit{{#3}} & \\textit{{#4}} \\\\
        \\end{{tabular*}}\\vspace{{-5pt}}}}
    \\newcommand{{\\resumeSubHeadingListStart}}{{\\begin{{itemize}}[leftmargin=0.15in, label={{}}]}}
    \\newcommand{{\\resumeSubHeadingListEnd}}{{\\end{{itemize}}}}

    % Document Starts
    \\begin{{document}}

    % Header
    \\begin{{center}}
        {{\\huge \\textbf{{{fullname}}}}} \\\\
        \\href{{mailto:{email}}}{{{email}}} ~|~ \\href{{{linkedin}}}{{LinkedIn}} ~|~ {phone}
    \\end{{center}}
    """

    # Summary Section
    if summary:
        latex_content += f"""
        \\section{{Summary}}
        {summary}
        """

    # Education Section
    if 'educations' in information and information['educations']:
        latex_content += "\\section{Education}\n\\resumeSubHeadingListStart\n"
        for edu in information['educations']:
            start_year = edu.get('start', {}).get('year', 'Unknown')
            end_year = edu.get('end', {}).get('year', 'Present')
            school_name = escape_latex(edu.get('schoolName', 'Unknown School'))
            degree = escape_latex(edu.get('degree', 'Unknown Degree')).replace('-', '{-}')
            latex_content += f"""
            \\resumeSubheading
                {{{school_name}}}{{{end_year}}}
                {{\\textnormal{{{degree}}}}}{{{start_year} -- {end_year}}}
            """
        latex_content += "\\resumeSubHeadingListEnd\n"

    # Skills Section
    if 'skills' in information and isinstance(information['skills'], list):
        skills_list = ", ".join(
            escape_latex(skill['name']) for skill in information['skills'] if 'name' in skill
        )
        latex_content += f"{skills_list}\n"
    else:
        latex_content += "No skills provided.\n"

    # Work Experience Section
    if 'position' in information and isinstance(information['position'], list):
        latex_content += "\\section{Work Experience}\n\\resumeSubHeadingListStart\n"
        for pos in information['position']:
            company_name = escape_latex(pos.get('companyName', 'Unknown Company'))
            title = escape_latex(pos.get('title', 'Unknown Title'))
            location = escape_latex(pos.get('location', 'Unknown Location'))

            start_year = pos.get('start', {}).get('year', 'Unknown')
            start_month = pos.get('start', {}).get('month', 'Unknown')
            end_year = pos.get('end', {}).get('year', 'Present')
            end_month = pos.get('end', {}).get('month', 'Unknown')

            start_date = f"{start_month}/{start_year}" if start_month != 'Unknown' else start_year
            end_date = f"{end_month}/{end_year}" if end_month != 'Unknown' else end_year

            latex_content += f"""
            \\resumeSubheading
                {{{company_name}}}{{{start_date} -- {end_date}}}
                {{{title}}}{{{location}}}
            """
        latex_content += "\\resumeSubHeadingListEnd\n"
    else:
        latex_content += "\\section{Work Experience}\nNo work experience provided.\n"

    # Projects Section
    if 'projects' in information and information['projects']:
        latex_content += "\\section{{Projects}}\n\\resumeSubHeadingListStart\n"
        for proj in information['projects']:
            if isinstance(proj, dict):
                title = escape_latex(proj.get('title', 'Untitled Project'))
                description = escape_latex(proj.get('description', 'No description available.'))
                latex_content += f"\\resumeItem{{\\textbf{{{title}}}: {description}}}\n"
            elif isinstance(proj, str):
                latex_content += f"\\resumeItem{{{escape_latex(proj)}}}\n"
        latex_content += "\\resumeSubHeadingListEnd\n"
    else:
        latex_content += "\\section{{Projects}}\nNo projects provided.\n"

    # Courses Section
    if 'courses' in information:
        courses = information['courses']
        if isinstance(courses, list):
            courses_list = ", ".join(escape_latex(course) for course in courses)
        elif isinstance(courses, str):
            courses_list = escape_latex(courses)
        else:
            courses_list = "No courses provided."
        latex_content += f"\\section{{Courses}}\n{courses_list}\n"
    else:
        latex_content += "\\section{{Courses}}\nNo courses provided.\n"

    # Languages Section
    if 'languages' in information and information['languages']:
        languages = information['languages']
        if isinstance(languages, list):  # Check if it's a list
            languages_list = ", ".join(
                f"{escape_latex(lang['name'])} ({escape_latex(lang['proficiency'])})" for lang in languages if
                'name' in lang and 'proficiency' in lang
            )
        else:  # If it's not a list, provide a fallback
            languages_list = "No languages provided."
        latex_content += "\\section{{Languages}}\n"
        latex_content += f"{languages_list}\n"
    else:
        latex_content += "\\section{{Languages}}\n"
        latex_content += "No languages provided.\n"

    # End document
    latex_content += "\\end{document}"

    return latex_content

def tex_to_pdf(input_tex_file='resume.tex', output_dir=''):
    if not input_tex_file.endswith(".tex"):
        raise ValueError("Input file must have a .tex extension")

    output_dir = output_dir or os.getcwd()
    pdf_output_path = os.path.join(output_dir, "resume.pdf")

    try:
        subprocess.run(
            ["pdflatex", "-output-directory", output_dir, input_tex_file],
            check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"PDF successfully generated: {pdf_output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e.stderr.decode()}")
    finally:
        pass
        # for ext in [".aux", ".log", ".out"]:
        #     aux_file = os.path.join(output_dir, f"{base_name}{ext}")
        #     if os.path.exists(aux_file):
        #         os.remove(aux_file)

    return pdf_output_path

tex_to_pdf("resume.tex")
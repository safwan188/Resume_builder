import json
import requests

def convert_markdown_to_pdf(markdown_content, Resume_file="Resume.pdf", engine="weasyprint"):
    # Define CSS styles for the PDF with smaller font size and tighter margins
    cssfile = """
                body {
                    padding: 5px;  /* Reduced padding */
                    margin: 5px;   /* Reduced margin */
                    font-size: 9pt;  /* Smaller font size */
                    line-height: 1.1;  /* Reduced line height */
                }
                h1 {
                    font-size: 14pt;  /* Slightly smaller font size for the name */
                    color: MidnightBlue;
                    margin: 0;
                    padding: 0;
                }
                h3 {
                    font-size: 11pt;  /* Smaller heading size */
                    color: MidnightBlue;
                    margin: 0;
                    padding-bottom: 3px;
                }
                li {
                    margin-top: 2px;
                    font-size: 9pt;  /* Smaller font for list items */
                }
                p {
                    margin: 4px 0;
                    font-size: 9pt;  /* Smaller font for paragraphs */
                }
              """
    # API endpoint for converting Markdown to PDF
    url = "https://md-to-pdf.fly.dev"

    # Data to be sent in the POST request
    data = {
        'markdown': markdown_content,
        'css': cssfile,
        'engine': engine
    }

    # Send a POST request to the API
    response = requests.post(url, data=data)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Save the generated PDF to a file
        with open(Resume_file, 'wb') as f:
            f.write(response.content)
        print(f"PDF saved to {Resume_file}")
    else:
        print(f"Error {response.status_code}: {response.text}")

class Resume:
    def __init__(self, name, email, mobile, linkedin, github, summary, education, skills, experience, projects, languages):
        # Initialize the Resume object with user information
        self.name = name
        self.email = email
        self.mobile = mobile
        self.linkedin = linkedin
        self.github = github
        self.summary = summary
        self.education = education
        self.skills = skills
        self.experience = experience
        self.projects = projects
        self.languages = languages

    def generate_markdown(self):
        # Generate Markdown content for the resume
        markdown_text = f"<h1 style=\"text-align:center;\">{self.name}</h1>\n"
        markdown_text += f"<p style=\"text-align:center; font-size: 9pt;\">{self.email} | {self.mobile} | <a href=\"{self.linkedin}\">LinkedIn</a> | <a href=\"{self.github}\">GitHub</a></p>\n\n"
        
        markdown_text += "### Summary\n\n---\n\n"
        markdown_text += f"{self.summary}\n\n"

        markdown_text += "### Education\n\n---\n\n"
        # Add education details to the Markdown content
        for edu in self.education:
            markdown_text += f"- {edu['level']}: {edu['institution']} | {edu['field']} | {edu['duration']}. | Average grade: {edu.get('score', '')}\n\n"

        markdown_text += "### Skills\n\n---\n\n"
        # Add categorized skills to the Markdown content
        markdown_text += "**Programming Languages**: " + ', '.join(self.skills["Programming Languages"]) + "\n\n"
        markdown_text += "**Frameworks and Libraries**: " + ', '.join(self.skills["Frameworks and Libraries"]) + "\n\n"
        markdown_text += "**Databases**: " + ', '.join(self.skills["Databases"]) + "\n\n"
        markdown_text += "**DevOps and Tools**: " + ', '.join(self.skills["DevOps and Tools"]) + "\n\n"

        markdown_text += "### Experience\n\n---\n\n"
        # Add work experience details to the Markdown content without cutting sentences
        for exp in self.experience:
            markdown_text += f"- **{exp['job_role']} ({exp['company_name']})**: {exp['description']}\n"

        markdown_text += "\n### Projects\n\n---\n\n"
        # Add project details to the Markdown content with GitHub links in the project name
        for proj in self.projects:
            markdown_text += f"- **[{proj['name']}]({proj['github_link']})**: {proj['description']}\n"

        markdown_text += "\n### Languages\n\n---\n\n"
        # Add languages to the Markdown content
        markdown_text += ', '.join(self.languages) + '\n'

        return markdown_text

def load_data_from_json(json_file):
    # Load data from data.json file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract data from JSON to create a Resume object
    name = data.get("name")
    email = data["contact"].get("email")
    mobile = data["contact"].get("phone")
    linkedin = data["contact"].get("linkedin")
    github = data["contact"].get("github")
    summary = data.get("summary", "")
    education = data.get("education", [])
    skills = data.get("skills", {})
    experience = data.get("work_experience", [])
    projects = data.get("projects", [])
    languages = data.get("languages", [])

    return Resume(name, email, mobile, linkedin, github, summary, education, skills, experience, projects, languages)

if __name__ == "__main__":
    # Load resume data from data.json
    resume_data = load_data_from_json('data.json')
    
    # Generate markdown content from the resume data
    markdown_text = resume_data.generate_markdown()
    
    # Convert markdown to PDF with smaller font size and optimized formatting
    convert_markdown_to_pdf(markdown_text)

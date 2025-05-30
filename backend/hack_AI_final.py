import json
import requests
from pymongo import MongoClient



api_key = "#"
uri =  "#"
client = MongoClient(uri)
db = client["resume_user"]
students_collection = db["user"]


def render_section_from_json(section_name, json_obj):
    """
    Pretty renders resume sections from JSON format to mimic a clean resume layout.
    """

    def render_personal_info(data):
        lines = []

        # Name (always shown)
        name = data.get("name", "")
        if name:
            lines.append(name)

        # Contact line (email, phone, address)
        contact = " | ".join(
            filter(None, [
                data.get("email", ""),
                data.get("phone", ""),
                data.get("address", "")
            ])
        )
        if contact:
            lines.append(contact)

        # Links (LinkedIn + Website)
        links = " | ".join(
            filter(None, [
                data.get("linkedin", ""),
                data.get("personal_website", "")
            ])
        )
        if links:
            lines.append(links)

        # Objective statement
        if data.get("objective"):
            lines.append("")
            lines.append(f"Objective: {data['objective']}")

        return "\n".join(lines)

    def render_education(data):
        lines = ["EDUCATION"]

        if type(data) is list:
            for edu in data:
                institution = edu.get("institution", "")
                degree = edu.get("degree", "")
                major = edu.get("major", "")
                gpa = edu.get("gpa", "")
                start = edu.get("start_date", "")
                end = edu.get("end_date", "")
                honors = edu.get("honors", "")
                coursework = edu.get("relevant_coursework", "")

                # Header: Institution | Dates
                date_range = f"{start} – {end}" if start or end else ""
                lines.append(f"{institution} | {date_range}")

                # Degree + Major
                deg_line = f"  * {degree} in {major}"
                if gpa:
                    deg_line += f", GPA: {gpa}"
                lines.append(deg_line)

                # Honors
                if honors:
                    lines.append(f"    • Honors: {honors}")

                # Relevant Coursework
                if coursework:
                    lines.append(f"    • Coursework: {coursework}")

                lines.append("")  # Extra spacing between entries

            return "\n".join(lines)
        else:
            institution = data.get("institution", "")
            degree = data.get("degree", "")
            major = data.get("major", "")
            gpa = data.get("gpa", "")
            start = data.get("start_date", "")
            end = data.get("end_date", "")
            honors = data.get("honors", "")
            coursework = data.get("relevant_coursework", "")

            # Header: Institution | Dates
            date_range = f"{start} – {end}" if start or end else ""
            lines.append(f"{institution} | {date_range}")

            # Degree + Major
            deg_line = f"  * {degree} in {major}"
            if gpa:
                deg_line += f", GPA: {gpa}"
            lines.append(deg_line)

            # Honors
            if honors:
                lines.append(f"    • Honors: {honors}")

            # Relevant Coursework
            if coursework:
                lines.append(f"    • Coursework: {coursework}")

            lines.append("")  # Extra spacing between entries

        return "\n".join(lines)

    def render_experience(data):
        lines = ["EXPERIENCE"]
        if type(data) is list:
            for job in data:
                company = job.get("company", "")
                title = job.get("job_title", "")
                location = job.get("location", "")
                start = job.get("start_date", "")
                end = job.get("end_date", "")
                responsibilities = job.get("responsibilities", [])

                # First line: Company | Dates | Location
                line = f"{company}"
                if start or end:
                    line += f" | {start} – {end}"
                if location:
                    line += f" | {location}"
                lines.append(line)

                # Job title
                if title:
                    lines.append(f"  * {title}")

                # Responsibilities
                for item in responsibilities:
                    lines.append(f"    • {item}")

                lines.append("")  # Spacing between entries

            return "\n".join(lines)
        else:
            company = data.get("company", "")
            title = data.get("job_title", "")
            location = data.get("location", "")
            start = data.get("start_date", "")
            end = data.get("end_date", "")
            responsibilities = data.get("responsibilities", [])

            # First line: Company | Dates | Location
            line = f"{company}"
            if start or end:
                line += f" | {start} – {end}"
            if location:
                line += f" | {location}"
            lines.append(line)

            # Job title
            if title:
                lines.append(f"  * {title}")

            # Responsibilities
            for item in responsibilities:
                lines.append(f"    • {item}")

            lines.append("")  # Spacing between entries

        return "\n".join(lines)

    def render_publication(data):
        lines = ["PUBLICATIONS"]

        # Ensure data is a list for unified handling
        if isinstance(data, dict):
            data = [data]

        for pub in data:
            title = pub.get("title", "")
            authors = pub.get("authors", "")
            venue = pub.get("venue", "")
            year = pub.get("year", "")
            doi = pub.get("doi", "")
            summary = pub.get("summary", "")

            # Display fields if they exist
            if title:
                lines.append(f"  - Title: {title}")
            if authors:
                lines.append(f"  - Authors: {authors}")
            if venue:
                lines.append(f"  - Venue: {venue}")
            if year:
                lines.append(f"  - Year: {year}")
            if doi:
                lines.append(f"  - DOI: {doi}" if doi.strip() else "  - DOI: N/A")
            if summary:
                lines.append(f"  - Summary: {summary}")

            lines.append("")  # Space between publications

        return "\n".join(lines)

    def render_projects(data):
        lines = ["PROJECTS"]
        if isinstance(data, dict):
            data = [data]

        for proj in data:
            name = proj.get("project_name", "")
            start = proj.get("start_date", "")
            end = proj.get("end_date", "")
            description = proj.get("description", [])

            # Header line: Project name | Duration
            header = f"{name}"
            if start or end:
                header += f" | {start} – {end}"
            lines.append(header)

            # Description bullets
            for bullet in description:
                lines.append(f"  • {bullet}")

            lines.append("")  # Space between projects

        return "\n".join(lines)

    def render_skills(data):
        lines = ["SKILLS"]
        for category, value in data.items():
            if value and isinstance(value, str) and value.strip():
                # Format the category name into Title Case with spaces
                formatted_category = category.replace('_', ' ').title()
                lines.append(f"{formatted_category}: {value}")
        return "\n".join(lines)

    section_formatters = {
        "personal_info": render_personal_info,
        "education": render_education,
        "professional_experience": render_experience,
        "publication": render_publication,
        "project": render_projects,
        "skills": render_skills
    }

    formatter = section_formatters.get(section_name, lambda x: str(x))
    return formatter(json_obj)


def save_section_to_db(user_id, section_name, content_lines):
    student_id = user_id
    existing = students_collection.find_one({"_id": student_id})

    if existing:
        # Student exists: update the specific section
        result = students_collection.update_one(
            {"_id": student_id},
            {"$set": {section_name: content_lines}}
        )
        print("🤖 Assistant", f"Student {user_id} updated: section '{section_name}' saved.")
    else:
        # Student doesn't exist: create new document with _id and section
        new_doc = {
            "_id": student_id,
            section_name: content_lines
        }
        students_collection.insert_one(new_doc)
        print("🤖 Assistant", f"New student {user_id} added with section '{section_name}'.")

def load_full_json_from_db(user_id):
    """
    Load the entire resume doc for a user from the mock DB.
    """
    return students_collection.find_one({"_id": user_id})

"""## Main Functionality Implementation"""

def call_openai(prompt: str, api_key: str) -> str:
    """
    Sends a prompt to the Open AI chat completion API to generate structured JSON
    and improvement suggestions for resume content.

    Parameters:
    - prompt (str): The formatted user/system prompt to send to Open AI.
    - api_key (str): The user's Open AI API key used for authentication.

    Returns:
    - str: The response from the Open AI model as a string.
           If successful, returns only the message content.
           If there's an error, returns a formatted error message.
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI career coach and educator working with college students, especially those new to the U.S. job market.\n\n"
                    "Your mission is to help users:\n"
                    "- Write or improve resumes with structured JSON data\n"
                    "- Generate realistic interview questions and coach responses\n"
                    "- Provide actionable suggestions to clarify, deepen, and reflect on their experience\n\n"
                    "Instructions:\n"
                    "- For resume structuring, return ONLY structured JSON between <<<JSON>>> and <<<END>>>.\n"
                    "- Provide improvement suggestions between <<<SUGGEST>>> and <<<END>>>.\n"
                    "- For interview coaching, you may return questions or feedback directly.\n"
                    "- DO NOT invent facts. Leave unknown fields empty.\n"
                    "- NEVER use placeholder text (e.g., [X], TBD).\n"
                    "- Do not include any additional commentary outside the defined blocks.\n"
                    "- Be supportive, but professional — like a mentor helping students grow."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"Error {response.status_code}: {response.text}"

def extract_json_and_suggestions(output: str):
    json_block, suggestion_block = "", ""
    inside_json, inside_suggest = False, False
    lines = output.strip().splitlines()
    for line in lines:
        if "<<<JSON>>>" in line:
            inside_json = True
            continue
        if "<<<SUGGEST>>>" in line:
            inside_suggest = True
            inside_json = False
            continue
        if "<<<END>>>" in line:
            inside_json = False
            inside_suggest = False
            continue
        if inside_json:
            json_block += line + "\n"
        elif inside_suggest:
            suggestion_block += line + "\n"
    try:
        return json.loads(json_block), suggestion_block.strip()
    except json.JSONDecodeError:
        print("⚠️ Failed to parse JSON from AI response")
        print(json_block)
        return {}, suggestion_block.strip()


def refine_section_to_json(
    raw_input: str,
    section_name: str,
    api_key: str,
    section_prompt: str = "",
    previous_json: dict = None
) -> tuple:
    """
    Converts a user's freeform input for a resume section into structured JSON and suggestions.
    Now supports incremental refinement by passing in previous_json as context.
    """

    # Construct the base system instructions
    prompt = f"""
You are a resume editing assistant.

The user is working on the **{section_name.replace('_', ' ').title()}** section of their resume.

Your job is to:
1. Preserve existing content from the previous JSON, unless the user clearly wants it removed or overwritten.
2. Add or revise information based on the user's new input.
3. Maintain a consistent structure and field names across updates.
4. Output clean, valid JSON ready for database storage.
5. Do NOT imagine or add information that the user did not explicitly provide.
6. Approach the task as a supportive career advisor — don’t just complete the section, but guide the student to improve it through thoughtful suggestions, clarifying questions, and positive reinforcement. Help them feel confident and in control of their resume.
7. When the user updates an existing entry (such as a project, publication, internship, or education record), identify the correct item by matching key fields (like title, project name, company, or institution). Once matched, replace the old version with the updated one. Do not keep both versions — only return the final, updated version in your output.

{section_prompt.strip() if section_prompt else ''}
"""

    # Add previous state if exists
    if previous_json:
        prev_json_str = json.dumps(previous_json, indent=2)

        if section_name in ["education", "professional_experience", "project", "publication"]:
            prompt += f"""
The section '{section_name}' is a list of items (e.g., multiple jobs or projects).
When given new input, you should:
- Preserve existing items from the previous JSON.
- Append new entries to the list if user describes new jobs/projects/etc.
- Do NOT replace or delete previous items unless user clearly requests it.

Current JSON for this section:
{prev_json_str}
"""
        else:
          # For dict-based sections like personal_info
            prompt += f"\nCurrent JSON for this section:\n{prev_json_str}"

    # Add user update
    prompt += f"\n\nUser Update:\n{raw_input.strip()}\n"

    # Final instruction
    prompt += """
Return exactly TWO blocks:

<<<JSON>>>
{ ... updated structured JSON ... }
<<<END>>>

<<<SUGGEST>>>
... suggestions to improve the section ...
<<<END>>>
"""

    output = call_openai(prompt, api_key)
    return extract_json_and_suggestions(output)

def run_section(section_name, section_prompt, api_key, user_id="test_user"):
    """
    Handles input, refinement, and saving for a single resume section.
    Supports iterative edits based on AI suggestions and saves cleaned JSON to database.
    """

    print(f"\n=== {section_name.replace('_', ' ').title()} ===")



    input_history = []

    # Load existing section (for patching purposes)
    previous_json = load_full_json_from_db(user_id).get(section_name, {})

    if previous_json:
        print("\n📝 Existing Content:")
        print(render_section_from_json(section_name, previous_json))

    # Initial user input
    initial_input = input(f"Describe your {section_name.replace('_', ' ')} (type 'done' anytime to save and exit this section):\n").strip()

    if initial_input.lower() == "done":
        print(f"↪️ Skipping {section_name.replace('_', ' ').title()} section.")
        return

    input_history.append(initial_input)


    while True:
        full_input = "\n\n---\n\n".join(input_history)

        # Pass previous_json for incremental refinement
        json_obj, suggestions = refine_section_to_json(
            full_input, section_name, api_key, section_prompt, previous_json
        )

        if json_obj:
            print("\n✅ AI-parsed content:")
            if json_obj.get(section_name):
                print(render_section_from_json(section_name, json_obj.get(section_name)))
            else:
                print(render_section_from_json(section_name, json_obj))

        if suggestions:
            print("\n💡 Suggestions to improve:")
            print(suggestions)

        follow_up = input("\nWould you like to add more or revise? (type 'done' to finish this section): ").strip().lower()
        if follow_up == "done":
            # FIX: Unwrap nested section name like {"education": {"education": [...]}}
            if isinstance(json_obj, dict) and section_name in json_obj:
                inner = json_obj[section_name]
                if isinstance(inner, (dict, list)):
                    json_obj = inner

            save_section_to_db(user_id, section_name, json_obj)
            print("\n✅ Section saved!")
            break
        else:
            input_history.append(follow_up)
            previous_json = json_obj  # Update previous_json for next loop

def login_user() -> str:
    """
    Handles user login by user_id. If the user exists in the database, load their data;
    otherwise, initialize a new profile.

    Returns:
    - str or None: The user_id if login successful, or None if user exited.
    """
    while True:
        user_id = input("Enter your user ID (or type 'exit' to quit): ").strip()
        if user_id.lower() == "exit":
            print("👋 Goodbye!")
            return None

        check = students_collection.find_one({"_id": user_id})
        if check:
            print(f"\n👋 Welcome back, {user_id}!")
            existing_sections = list(check.keys())
            if existing_sections:
                print("✅ Existing resume sections:", ", ".join(existing_sections))
            else:
                print("🗒️ You haven't started your resume yet.")
        else:
            print(f"\n🆕 Creating new profile for {user_id}.")
            students_collection.insert_one({"_id": user_id})

        return user_id

def run_resume_builder(section_order, section_prompts, api_key, user_id="test_user"):
    print("Welcome! I’m your AI resume assistant. Let’s build your resume section by section!\n")

    while True:
        check = students_collection.find_one({"_id": user_id})  # ✅ move inside the loop

        print("\n📌 Resume Sections Available:")
        for idx, section in enumerate(section_order, 1):
            status = "✅" if section in check else "❌"
            print(f"{idx}. {section.replace('_', ' ').title()} {status}")

        print(f"{len(section_order)+1}. 🎤 Mock Interview Mode")
        print(f"{len(section_order)+2}. 📄 View Full Resume")
        print(f"{len(section_order)+3}. ❌ Exit")

        choice = input("\nType the number of the section you want to work on (or view/exit): ").strip()

        try:
            choice_idx = int(choice)
            if 1 <= choice_idx <= len(section_order):
                section = section_order[choice_idx - 1]
                run_section(section, section_prompts.get(section, "{{input}}"), api_key, user_id)
            elif choice_idx == len(section_order) + 1:
                run_interview_mode(user_id, api_key)
            elif choice_idx == len(section_order) + 2:
                print("\n📄 Generating Full Resume...\n")
                resume_doc = load_full_json_from_db(user_id)
                print(generate_full_resume(resume_doc))
            elif choice_idx == len(section_order) + 3:
                print("\n👋 Exiting resume builder. See you next time!\n")
                break
            else:
                print("Invalid number. Please choose a valid section or command.")
        except ValueError:
            print("Please enter a number.")


def generate_full_resume(resume_data: dict) -> str:
    lines = ["=================\n📄 FINAL RESUME\n=================\n"]
    for section, content in resume_data.items():
        lines.append(f"\n--- {section.replace('_', ' ').title()} ---")
        lines.append(render_section_from_json(section, content))
    return "\n\n".join(lines)

def run_interview_mode(user_id, api_key):
    """
    Mock interview assistant using the user's resume + target job.
    """

    print("\n🧠 Welcome to the AI Mock Interview Coach!")

    # Step 1: Ask for job title and JD
    job_title = input("Enter the job title you're applying for (e.g., 'Data Analyst') (or type 'exit' to leave interview mode):\n").strip()
    if job_title.lower() == "exit":
        print("👋 Exiting mock interview.")
        return

    job_description = input("\nPaste the job description (JD). Press Enter on an empty line when you're done (or type 'exit' to leave interview mode):\n").strip()
    if job_description.lower() == "exit":
        print("👋 Exiting mock interview.")
        return


    # Step 2: Construct prompt
    resume_json = load_full_json_from_db(user_id)
    prompt = f"""
You are an AI mock interview coach.

The user is applying for the following role:
**Job Title**: {job_title}

**Job Description**:
{job_description}

Below is the user's resume in structured JSON format:
{json.dumps(resume_json, indent=2)}

Please generate 5–7 realistic interview questions tailored to this role and resume.
Include a mix of technical and behavioral questions.

Return in this format:
<<<QUESTIONS>>>
- Question 1
- Question 2
- ...
<<<END>>>
"""

    response = call_openai(prompt, api_key)

    # Step 3: Extract questions
    questions = []
    inside = False
    for line in response.strip().splitlines():
        if "<<<QUESTIONS>>>" in line:
            inside = True
            continue
        if "<<<END>>>" in line:
            break
        if inside and line.startswith("- "):
            questions.append(line[2:].strip())

    if not questions:
        print("\n⚠️ Failed to extract interview questions. Here's the raw output:")
        print(response)
        return

    # Step 4: Interactive Q&A
    while True:
        print("\n📋 Here are your personalized interview questions:")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q}")

        choice = input("\nChoose a question number to practice (or type 'new' for more, 'exit' to return): ").strip().lower()
        if choice == "exit":
            print("👋 Exiting mock interview.")
            break
        elif choice == "new":
            return run_interview_mode(user_id, api_key)
        elif choice.isdigit() and 1 <= int(choice) <= len(questions):
            idx = int(choice) - 1
            print(f"\n💬 Question: {questions[idx]}")
            user_answer = input("Your Answer (or type 'exit' to return):\n").strip()
            if user_answer.lower() == "exit":
                print("👋 Exiting mock interview.")
                break

            # Ask AI to review the answer
            review_prompt = f"""
You are a helpful AI career coach.

Here is a candidate's answer to the following interview question:

**Q**: {questions[idx]}
**A**: {user_answer}

Please provide constructive feedback, improvements, or an example answer.
Return your feedback directly. Do not include formatting instructions.
"""
            feedback = call_openai(review_prompt, api_key)
            print("\n🧠 AI Feedback:\n")
            print(feedback)
        else:
            print("❗ Invalid input. Try again.")

def start_resume_session(section_order, section_prompts, api_key):
    user_id = login_user()
    if user_id is None:
        return  # User chose to exit

    print("\n🛠️ Entering resume builder...\n")
    run_resume_builder(section_order, section_prompts, api_key, user_id)



"""## Prompt"""

# The order in which main resume sections will be prompted
section_order = [
    "personal_info",
    "education",
    "professional_experience",
    "publication",
    "project",
    "skills"
]


# Prompt templates for each main section (Improved with Strict Rules and User Guidance)
section_prompts = {
    "personal_info": (
        "You are an AI assistant helping an undergraduate user write their personal information for a resume.\n"
        "Your tone should be friendly, encouraging, and professional — like a helpful career coach.\n"
        "IMPORTANT: Do NOT ask about Education, Internships, Projects, Skills, Certifications, or Publications.\n"
        "- Use ONLY the following fields:\n"
        "  - name\n"
        "  - email\n"
        "  - phone\n"
        "  - address\n"
        "  - linkedin\n"
        "  - objective\n"
        "  - personal_website\n"
        "- Do not modify previous data unless instructed. Leave missing fields empty.\n"
        "For the 'name' field, validate that the input is a full name with at least two words, each starting with a capital letter and separated by a space.\n"
        "If the input does not follow this format (e.g., a single word or all lowercase), leave the field blank and ask the user to confirm or correct it.\n"
        "Only accept such input if the user explicitly confirms it is their intended full name.\n"
        "Ensure names are capitalized properly (e.g., John Doe).\n"
        "If the user provides a university name like 'Upenn', automatically correct it to 'University of Pennsylvania'.\n"
        "If the input is meaningless or a typo (e.g., 'aaa', 'xjssjs'), return a message asking the user to provide valid input.\n"
        "Provide suggestions if applicable, such as using a professional LinkedIn URL.\n"
        "Return only valid JSON data.\n"
        "Input: {{input}}"
    ),
    "education": (
        "You are an AI assistant helping an undergraduate user write their education history for a resume.\n"
        "Your tone should be friendly, encouraging, and professional — like a helpful career coach.\n"
        "IMPORTANT: Do NOT ask about Internships, Projects, Skills, Certifications, or Publications.\n"
        "- Use ONLY these fields:\n"
        "  - institution\n"
        "  - degree\n"
        "  - major\n"
        "  - gpa\n"
        "  - start_date (Format: 'May 2023') \n"
        "  - end_date (Format: 'June 2024' or 'Present') \n"
        "  - honors\n"
        "  - relevant_coursework\n"
        "- Do not modify previous data unless instructed. Leave missing fields empty.\n"
        "Ensure institution names are fully written (e.g., 'Upenn' -> 'University of Pennsylvania').\n"
        "Your output must be in structured JSON format, following the fields mentioned above.\n"
        "Provide suggestions to enhance clarity and impact, such as adding high-level courses related to the target job.\n"
        "If the user provides incomplete information, prompt them to add more details.\n"
        "If the user provides invalid input (e.g., 'aaa'), ask them to provide valid information.\n"
        "Return only valid JSON data.\n"
        "Input: {{input}}"
    ),
    "professional_experience": (
        "You are an AI assistant helping an undergraduate user describe their internship or job experience.\n"
        "Your tone should be friendly, encouraging, and professional — like a helpful career coach.\n"
        "IMPORTANT: Do NOT ask about Publications, Projects, Skills, Certifications, or Hobbies.\n"
        "Ensure company names are properly capitalized (e.g., Google, Microsoft).\n"
        "Your output must be in structured JSON format.\n"
        "- Use ONLY the following fields:\n"
        "  - company\n"
        "  - job_title\n"
        "  - location\n"
        "  - start_date (Format: 'May 2023') \n"
        "  - end_date (Format: 'June 2024' or 'Present') \n"
        "  - responsibilities (as list of bullet points)\n"
        "Do not modify previous data unless instructed. Leave missing fields empty.\n"
        "If the user provides invalid input (e.g., 'bbb'), ask them to provide valid information.\n"
        "Provide suggestions to enhance clarity and impact, such as quantifying results when possible.\n"
        "Return only valid JSON data.\n"
        "Input: {{input}}"
    ),
    "publication": (
        "You are an AI assistant helping an undergraduate user summarize their publication for a resume.\n"
        "Your tone should be friendly, encouraging, and professional — like a helpful career coach.\n"
        "IMPORTANT: Do NOT ask about Internships, Projects, Skills, Certifications, or Hobbies.\n"
        "Your output must be in structured JSON format.\n"
        "- Use ONLY the following fields:\n"
        "  - title\n"
        "  - authors\n"
        "  - venue\n"
        "  - year\n"
        "  - doi (Digital Object Identifier)\n"
        "  - summary (A brief description of the work)\n"
        "- Do not modify previous data unless instructed. Leave missing fields empty.\n"
        "- DO NOT invent new content or structure.\n"
        "- If the user provides invalid input (e.g., 'ccc'), ask them to provide valid information.\n"
        "Provide suggestions if applicable, such as using citation formats or mentioning co-authors.\n"
        "Return only valid JSON data.\n"
        "Input: {{input}}"
    ),
    "project": (
        "You are an AI assistant helping an undergraduate user describe their project for a resume.\n"
        "Your tone should be friendly, encouraging, and professional — like a helpful career coach.\n"
        "IMPORTANT: Do NOT ask about Internships, Publications, Skills, Certifications, or Hobbies.\n"
        "Your output must be in structured JSON format.\n"
        "- Use ONLY the following fields:\n"
        "  - project_name\n"
        "  - start_date (Format: 'May 2023') \n"
        "  - end_date (Format: 'June 2024' or 'Present') \n"
        "  - description (2–4 bullet points describing the project, tasks performed, and impact, using strong active verbs)\n"
        "- Do not modify previous data unless instructed. Leave missing fields empty.\n"
        "- Do not add or change field names. Do not include placeholders.\n"
        "- If the user provides invalid input (e.g., 'ddd'), ask them to provide valid information.\n"
        "Provide suggestions if applicable, such as using active verbs and quantifying achievements.\n"
        "Return only valid JSON data.\n"
        "Input: {{input}}"
    ),
    "skills": (
        "You are an AI assistant helping an undergraduate user organize their skills list for a resume.\n"
        "Your tone should be friendly, encouraging, and professional — like a helpful career coach.\n"
        "IMPORTANT: Do NOT ask about Internships, Publications, Certifications, or Hobbies.\n"
        "Identify skill categories and group them into structured JSON.\n"
        "Common categories include: Languages (such as Spanish, Chinese, etc.), Programming Languages, Tools, Frameworks, Soft Skills (Leadership, Communication, Problem-Solving, etc.), Certifications, etc.\n\n"
        "Output Rules:\n"
        "- Automatically categorize the provided skills into appropriate categories.\n"
        "- Only include categories with non-empty content. Show at most **two to three categories**.\n"
        "- Format each category's content as a single line, separated by commas.\n"
        "- Structure JSON as:\n"
        "{\n"
        "  \"programming_languages\": \"Python, Java, SQL\",\n"
        "  \"tools\": \"Tableau, Git, Excel\",\n"
        "  \"soft_skills\": \"Leadership, Communication, Problem-Solving\"\n"
        "}\n"
        "- Include only mentioned skills. Do not hallucinate. Leave unspecified categories empty.\n"
        "- Return only valid JSON data.\n"
        "Input: {{input}}"
    )
}


# Run this to play with the application
start_resume_session(section_order, section_prompts, api_key)

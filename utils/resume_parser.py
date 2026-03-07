@app.post("/parse-resume")
def parse_resume():

    resume_text = """
    Suraj Gavali
    Software Developer
    Skills: Python, FastAPI, Angular, SQL, Docker
    Experience: 3 years backend development
    """

    prompt = f"""
    Extract the following information from the resume.

    Return JSON only.

    Fields:
    - skills
    - years_of_experience
    - technologies
    - job_roles

    Resume:
    {resume_text}
    """

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"result": response["message"]["content"]}
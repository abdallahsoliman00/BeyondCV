BASE_TEMPLATE = {
    "name": "Name",
    "title": "Title",
    "profile_summary": "summary",
    "education": [
        {"institute": "institute name", "degree": "degree name", "year": "year"}
    ],
    "experience": [
        {
            "organisation": "organisation name",
            "job_title": "job title",
            "job_period": "period",
            "description": ["Experience bullet 1", "Experience bullet 2", "etc..."]
        }
    ],
    "projects": [
        {
            "project_name": "Proj Name",
            "period": "period",
            "description": ["Bullet 1", "Bullet 2", "etc..."]
        }
    ],
    "tools_prog_languages": ["tool 1", "tool 2", "etc..."],
    "soft_skills": ["Communication", "Problem Solving", "etc..."],
    "languages": [
        {"language": "Arabic", "proficiency": "Native"}
    ],
    "certifications": ["certification 1", "certification n.."]
}

EXTRA_MODULES = {
    "salary": [
        {
            "key": "salary_expectation",
            "description": "Candidate's stated salary expectation",
            "type": "string"
        }
    ],
    "military_status": [
        {
            "key": "military_status",
            "description": "Candidtate's military status",
            "type": "string"
        }
    ],
    "social": [
        {
            "key": "linkedin",
            "description": "LinkedIn profile URL",
            "type": "string"
        },
        {
            "key": "github",
            "description": "GitHub profile URL",
            "type": "string"
        },
        {
            "key": "email",
            "description": "Email",
            "type": "string"
        }
    ]
}


def build_extra_fields_text(modules: list[str]) -> str:
    """Builds the extra instruction block to append to the prompt."""
    if not modules:
        return ""

    fields = [f for m in modules for f in EXTRA_MODULES.get(m, [])]
    if not fields:
        return ""

    lines = ["Also extract the following additional fields:"]
    for f in fields:
        lines.append(f"- \"{f['key']}\": {f['description']} (type: {f['type']})")
    return "\n".join(lines)

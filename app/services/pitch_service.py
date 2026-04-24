def build_pitches(domain: str) -> dict:
    company_name = domain.split(".")[0].replace("-", " ").title()

    full_pitch = (
        f"Subject: Helping {company_name} accelerate pipeline growth\n\n"
        f"Hi Team {company_name},\n\n"
        "I noticed your team is scaling and likely evaluating ways to improve qualified lead flow. "
        "We help B2B teams identify high-intent prospects, automate first-touch outreach, "
        "and improve conversion with AI-assisted personalization.\n\n"
        "Would you be open to a 15-minute call next week to explore whether this could fit your growth goals?\n\n"
        "Best regards,\n"
        "Your Name"
    )

    short_pitch = (
        f"Hi {company_name} team — we help B2B companies automate prospect discovery "
        "and personalized outreach. Open to a quick 15-min intro next week?"
    )

    return {"pitch": full_pitch, "short_pitch": short_pitch}

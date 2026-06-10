import requests
import json


def get_profile_info(linkedin_username):
    """Gets the profile information for the specified LinkedIn user."""

    url = "https://api.linkedin.com/v2/me"
    headers = {
        "Authorization": f"Bearer {_get_token('LINKEDIN_ACCESS_TOKEN')}"
    }
    params = {
        "q": linkedin_username
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception("Error getting profile information: {}".format(response.status_code))

    profile_info = json.loads(response.content)
    return profile_info


def check_profile_for_errors(profile_info):
    """Checks the specified profile for errors."""

    for field in profile_info:
        if isinstance(profile_info[field], str):
            profile_info[field] = profile_info[field].strip()
            if not profile_info[field]:
                raise Exception("Error: The {} field is empty.".format(field))

    for field in ["name", "headline", "summary", "skills", "experience"]:
        if field not in profile_info:
            raise Exception("Error: The {} field is missing.".format(field))

    return profile_info


def generate_keywords(profile_info):
    """Generates a list of keywords from the specified profile."""

    keywords = set()
    for field in ["name", "headline", "summary", "skills", "experience"]:
        if isinstance(profile_info[field], str):
            keywords.update(profile_info[field].split())

    return keywords


def request_recommendations(linkedin_username):
    """Requests recommendations from the specified LinkedIn user."""

    url = "https://api.linkedin.com/v2/recommendations/recommendations"
    headers = {
        "Authorization": f"Bearer {_get_token('LINKEDIN_ACCESS_TOKEN')}"
    }
    data = {
        "recommendationType": "recommendation"
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception("Error requesting recommendations: {}".format(response.status_code))

    recommendations = json.loads(response.content)
    return recommendations


def search_for_jobs(keywords, location):
    """Searches for jobs that match the specified keywords and location."""

    url = "https://api.indeed.com/v2/jobs?q={}&l={}".format(keywords, location)
    headers = {
        "Authorization": f"Bearer {_get_token('INDEED_API_KEY')}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Error searching for jobs: {}".format(response.status_code))

    jobs = json.loads(response.content)
    return jobs


def _get_token(env_var):
    """Read an API token from environment; raise a clear error if missing."""
    import os
    token = os.environ.get(env_var)
    if not token:
        raise EnvironmentError(
            f"{env_var} is not set. "
            "Add it to your environment or a .env file before running."
        )
    return token

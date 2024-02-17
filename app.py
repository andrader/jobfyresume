import streamlit as st
from myapp.job_listing import Linkedin
from myapp.resume_upload import process_file
from myapp.job_listing import ListedAt
from dotenv import load_dotenv
import os

state = st.session_state


def init(key, value=None):
    if key not in st.session_state:
        st.session_state[key] = value


# @st.cache_resource
@st.cache_data
def create_api(username, password):
    print("Creating API instance")
    return Linkedin(username, password)


def cb_login_api(username, password):
    state["linkedin_api"] = create_api(username, password)


def cb_save_resume_text(key):
    text = state[key]
    if key == "resume_file_uploader":
        text = process_file(text)
    state["resume_text"] = text
    st.toast("Resume text saved!")


def display_form_login_linkedin_api():
    with st.container(border=True):
        st.subheader("Linkedin API")
        if "linkedin_api" in state:
            st.write("Logged in")
            st.button("Logout", on_click=lambda: state.pop("linkedin_api", None))

        else:
            with st.form("linkedin_login"):
                username = st.text_input("Username", key="linkedin_username")
                password = st.text_input(
                    "Password", type="password", key="linkedin_password"
                )
                st.form_submit_button(
                    "Login", on_click=cb_login_api, args=(username, password)
                )


def display_sidebar():
    with st.sidebar:
        st.title("LinkedIn Job Search & Resume Adaptation")
        display_form_login_linkedin_api()

        display_form_job_search()


def display_upload_resume():
    st.header("Upload Resume")

    st.text_area(
        "Paste your resume here:",
        key="resume_text_area",
        on_change=cb_save_resume_text,
        args=("resume_text_area",),
    )
    st.file_uploader(
        "Or upload your resume",
        type=["txt", "docx", "pdf"],
        key="resume_file_uploader",
        on_change=cb_save_resume_text,
        args=("resume_file_uploader",),
    )
    if st.button("Save"):
        pass


def display_form_job_search():
    listed_at_opts = {
        "1 day": ListedAt._1DAY,
        "2 days": ListedAt._2DAYS,
        "1 week": ListedAt._1WEEK7,
        "1 motnh": ListedAt._1MONTH,
    }

    with st.form("JobSearch"):
        st.subheader("Job Search")
        keywords = st.text_input("Keywords", "Data Scientist")
        location_name = st.text_input("Location", "United States")
        remote = st.multiselect(
            "Work model", ["onsite", "remote", "hybrid"], ["remote"]
        )
        listed_at = st.selectbox("Listed at", listed_at_opts)
        limit = st.slider("Limit", -1, 100, 5)

        kwargs = dict(
            keywords=keywords,
            location_name=location_name,
            remote=remote,
            listed_at=listed_at,
            limit=limit,
        )
        st.form_submit_button("Search", on_click=cb_search_jobs, kwargs=kwargs)


@st.cache_data
def get_jobs_cached(**kwargs):
    print(f"get_jobs() for {kwargs}")
    api = state["linkedin_api"]
    return api.get_job_search_results(**kwargs)


def cb_search_jobs(**kwargs):
    if "linkedin_api" not in state:
        st.error("Not logged in to Linkedin")
        return

    jobs = get_jobs_cached(**kwargs)
    state["jobs_found"] = jobs


tpt = """### {title} - [{company}]({company_url})

[Apply]({applyurl}), id:{job_id}

{location}

remote: {remote},
apply: {apply}

{description}

---"""


def display_jobs_search_results():

    jobs = state["jobs_found"]

    # keys = ['job_id', 'title', 'company', 'universalName', 'company_url', 'remote',
    #  'applyurl', 'apply', 'location', 'jobsate', 'description', '_raw']

    for job_ in jobs:

        job = dict(**job_)  # copy?

        job["remote"] = "Remote" if job["remote"] is True else "Not Remote"

        label = """{title} - {company}""".format(**job)
        st.checkbox(label, True)
        s = tpt.format(**job).replace("$", "\$")
        with st.expander(label):
            st.markdown(s)


def main():
    # st.title("LinkedIn Job Search & Resume Adaptation")

    display_sidebar()

    # st.write(state)

    display_upload_resume()

    # Display job listings
    st.header("Job Listings")
    if "jobs_found" in state:
        st.write("Job Search Results")
        display_jobs_search_results()
    else:
        st.write("No search yet")


if __name__ == "__main__":

    load_dotenv(".env")

    init("linkedin_username", os.environ.get("LINKEDIN_USERNAME", ""))
    init("linkedin_password", os.environ.get("LINKEDIN_PASSWORD", ""))

    main()

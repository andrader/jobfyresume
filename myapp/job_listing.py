from linkedin_api import Linkedin as LinkedinBase
from enum import Enum
from typing import Any


class ListedAt(Enum):
    _1DAY = 24 * 60 * 60
    _2DAYS = _1DAY * 2
    _1WEEK7 = _1DAY * 7
    _2WEEK7 = _1WEEK7 * 2
    _1MONTH = _1DAY * 30
    _2MONTH = _1MONTH * 2


# ',' separated json path to fields of interest
ATTRS_ = dict(
    job_id="jobPostingId",
    title="title",
    company="""companyDetails,com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany,companyResolutionResult,name""",
    universalName="""companyDetails,com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany,companyResolutionResult,universalName""",
    company_url="""companyDetails,com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany,companyResolutionResult,url""",
    remote="workRemoteAllowed",
    applyurl="applyMethod,com.linkedin.voyager.jobs.OffsiteApply,companyApplyUrl",
    apply="applyMethod",
    location="formattedLocation",
    jobsate="jobState",
    description="description,text",
)
for k, v in ATTRS_.items():
    ATTRS_[k] = [s.strip() for s in v.split(",")]


class Linkedin(LinkedinBase):

    @staticmethod
    def structure_job_data(job_data):
        structured = dict()
        for key in ATTRS_:
            value = job_data
            for step in ATTRS_[key]:
                if isinstance(value, dict) and step:
                    value = value.get(step)
                else:
                    value = "ERROR"
                    break
            structured[key] = value

        structured["_raw"] = job_data
        return structured

    # @functools.wraps(cls.search_jobs)
    def get_job_search_results(
        self,
        keywords: Any | None = None,
        companies: Any | None = None,
        experience: Any | None = None,
        job_type: Any | None = None,
        job_title: Any | None = None,
        industries: Any | None = None,
        location_name: Any | None = None,
        remote: Any | None = None,
        listed_at: int = 24 * 60 * 60,
        distance: Any | None = None,
        limit: int = -1,
        offset: int = 0,
    ):

        jobs_found = self.search_jobs(
            keywords=keywords,
            companies=companies,
            experience=experience,
            job_type=job_type,
            job_title=job_title,
            industries=industries,
            location_name=location_name,
            remote=remote,
            listed_at=listed_at,
            distance=distance,
            limit=limit,
            offset=offset,
        )

        jobs_data_fmtd = []
        for i, job_post in enumerate(jobs_found):
            job_id = job_post["trackingUrn"].split(":")[-1]
            job_data = self.get_job(job_id)
            job_data_fmtd = self.structure_job_data(job_data)

            jobs_data_fmtd.append(job_data_fmtd)

        return jobs_data_fmtd


# def get_jobs_search_results(user, password, **kwargs):

#     # Authenticate using any Linkedin account credentials

#     kwargs_ = dict(
#         keywords="Data Science",
#         # job_title=[]
#         location_name="United States",
#         remote=["2"],
#         listed_at=At._1WEEK7,
#         limit=10,
#     )
#     kwargs_.update(kwargs)

#     jobs_found = api.get_job_search_results(**kwargs_)
#     return jobs_found


if __name__ == "__main__":
    pass
    # from getpass import getpass

    # Authenticate using any Linkedin account credentials

    # api = Linkedin(input('username'), getpass())

    # jobs_found = api.search_jobs(
    #     keywords="Data Science",
    #     # job_title=[]
    #     location_name="United States",
    #     remote=["2"],
    #     listed_at=At._1WEEK7,
    #     limit=10,
    # )

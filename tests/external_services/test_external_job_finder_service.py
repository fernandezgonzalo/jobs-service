from app.services.external_job_finder_service import JobberwockyExtraSource, Job, JobFilters


service = JobberwockyExtraSource(
    "test_url"
)

dummy_jobs = [
    ['Jr Java Developer', 24000, 'Argentina', ['Java', 'OOP']],
    ['SSr Java Developer', 34000, 'Argentina', ['Java', 'OOP', 'Design Patterns']],
    ['Sr Java Developer', 44000, 'Argentina', ['Java', 'OOP', 'Design Patterns']],
    ['Sr Developer', 44000, 'Argentina', ['PHP', 'OOP', 'Design Patterns']],
    ['Functional Analyst', 38000, 'Argentina', ['UX']],
    ['React Developer', 49000, 'Argentina', ['React', 'TypeScript']],
    ['Angular Developer', 49000, 'Argentina', ['Angular', 'TypeScript']],
    ['Database Administrator', 44000, 'Argentina', ['MySQL', 'Percona']],
    ['Windows server Admin', 44000, 'Argentina', ['Windows Server']],
    ['Sr UX Designer', 40000, 'Argentina', ['UX']],
    ['Jr C# Developer', 30000, 'Argentina', ['C#', 'OOP']],
    ['Ruby Developer', 34000, 'Argentina', ['Ruby', 'OOP']]
]

def get_jobs(httpx_mock):
    httpx_mock.add_response(json=dummy_jobs)

    service = JobberwockyExtraSource("test_url")

    jobs = service.get_jobs()

    assert len(jobs) == len(dummy_jobs)
    assert all(isinstance(job, Job) for job in jobs)
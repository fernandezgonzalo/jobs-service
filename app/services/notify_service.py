from app.domain.job import Job


class PrintEmailNotifier:
    def notify(self, email: str, new_job: Job):
        print(f"Sending email to {email} with new job {new_job}")

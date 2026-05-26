class JobBoardException(Exception):
    def __init__(self,msg:str,status_code:int =400):
        self.msg=msg
        self.status_code=status_code
        super().__init__(msg)

class CompanyNotFoundError(JobBoardException):
    def __init__(self, company_id:int):
        super().__init__(f"company {company_id} not found", status_code=404)

class JobNotFoundError(JobBoardException):
    def __init__(self,job_id:int):
        super().__init__(f"Job with id {job_id} not found",404)


class ApplicantNotFoundError(JobBoardException):
    def __init__(self,applicant_id):
        super().__init__(f"Applicant {applicant_id} not found",404)




class ApplicationNotFoundError(JobBoardException):
    def __init__(self, application_id):
        super().__init__(f"Application with id {application_id} not found",404)


class InvalidTranstionError(JobBoardException):
    def __init__(self,current:str,target:str,allowed:list):
        super().__init__(f"Invalid transition from {current} -> {target} \n valid transitions are {allowed}", 400)

class DuplicateApplicationError(JobBoardException):
    def __init__(self):
        super().__init__("Already applied for this job",409)

    
class JobNotActiveError(JobBoardException):
    def __init__(self):
        super().__init__("Job is not accepting your application",400)

class NoJobs(JobBoardException):
    def __init__(self):
        super().__init__("No jobs found",404)

class InvalidCursor(JobBoardException):
    def __init__(self):
        super().__init__("Cursor is invalid",404)

    



    
from ..repositories.managers import ReportManager
from sqlalchemy.exc import SQLAlchemyError

class ReportController:
    manager = ReportManager

    @classmethod
    def get_report(cls):
        try:
            report = cls.manager.get_report()
            return report, None
        except SQLAlchemyError as error:
            return None, str(error)
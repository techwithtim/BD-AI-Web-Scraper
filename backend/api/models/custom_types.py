from enum import Enum


class TaskStatus(Enum):
    STARTED = "Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"

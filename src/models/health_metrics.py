from pydantic import BaseModel, Field


class HealthMetrics(BaseModel):
    uptime: str 
    approximate_db_size: str 
    total_authenticated_requests: int 
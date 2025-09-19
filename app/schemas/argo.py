"""Argo data schemas for API responses."""

from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class ArgoMeasurementDTO(BaseModel):
    """Argo measurement data transfer object."""
    pressure: float = Field(..., description="Pressure in decibar")
    temperature: float = Field(..., description="Temperature in degree Celsius") 
    salinity: float = Field(..., description="Salinity in PSU")


class ArgoLocationDTO(BaseModel):
    """Argo location data transfer object."""
    latitude: float = Field(..., description="Latitude in decimal degrees")
    longitude: float = Field(..., description="Longitude in decimal degrees")


class ArgoProfileSummaryDTO(BaseModel):
    """Summarized Argo profile for API responses."""
    profile_id: str = Field(..., description="Unique profile identifier")
    float_id: int = Field(..., description="Float platform number")
    cycle_number: int = Field(..., description="Cycle number")
    timestamp: datetime = Field(..., description="Profile timestamp")
    project_name: str = Field(..., description="Project name")
    location: ArgoLocationDTO = Field(..., description="Profile location")
    measurement_count: int = Field(..., description="Number of measurements")
    
    class Config:
        schema_extra = {
            "example": {
                "profile_id": "5906527_94",
                "float_id": 5906527,
                "cycle_number": 94,
                "timestamp": "2023-03-15T12:00:00Z",
                "project_name": "Argo-France",
                "location": {
                    "latitude": 42.1,
                    "longitude": -40.5
                },
                "measurement_count": 150
            }
        }


class ArgoProfileDetailDTO(ArgoProfileSummaryDTO):
    """Detailed Argo profile with measurements."""
    measurements: List[ArgoMeasurementDTO] = Field(..., description="Profile measurements")
    
    class Config:
        schema_extra = {
            "example": {
                "profile_id": "5906527_94",
                "float_id": 5906527,
                "cycle_number": 94,
                "timestamp": "2023-03-15T12:00:00Z",
                "project_name": "Argo-France",
                "location": {
                    "latitude": 42.1,
                    "longitude": -40.5
                },
                "measurement_count": 2,
                "measurements": [
                    {
                        "pressure": 10.5,
                        "temperature": 15.2,
                        "salinity": 35.1
                    },
                    {
                        "pressure": 20.0,
                        "temperature": 14.8,
                        "salinity": 35.2
                    }
                ]
            }
        }
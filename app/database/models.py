"""Database models for Argo data."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ArgoMeasurement(BaseModel):
    """Single measurement from an Argo profile."""
    pressure: float = Field(..., description="Pressure in decibar")
    temperature: float = Field(..., description="Temperature in degree Celsius")
    salinity: float = Field(..., description="Salinity in PSU")


class ArgoLocation(BaseModel):
    """GeoJSON Point location."""
    type: str = Field(default="Point", description="GeoJSON type")
    coordinates: List[float] = Field(..., description="[longitude, latitude] coordinates")


class ArgoProfile(BaseModel):
    """Argo float profile document."""
    id: str = Field(..., alias="_id", description="Unique profile identifier")
    float_id: int = Field(..., description="Float platform number")
    cycle_number: int = Field(..., description="Cycle number for this float")
    time: datetime = Field(..., description="Profile timestamp")
    project_name: str = Field(..., description="Project name")
    location: ArgoLocation = Field(..., description="Profile location")
    measurements: List[ArgoMeasurement] = Field(..., description="Pressure/temperature/salinity measurements")
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "5906527_94",
                "float_id": 5906527,
                "cycle_number": 94,
                "time": "2023-03-15T12:00:00Z",
                "project_name": "Argo-France",
                "location": {
                    "type": "Point",
                    "coordinates": [-40.5, 42.1]
                },
                "measurements": [
                    {
                        "pressure": 10.5,
                        "temperature": 15.2,
                        "salinity": 35.1
                    }
                ]
            }
        }
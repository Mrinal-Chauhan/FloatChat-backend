"""Argo data ingestion script for MongoDB."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import xarray as xr
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def _decode_bytes(value) -> str:
    """Best-effort conversion of NetCDF byte/char arrays to clean strings."""
    try:
        arr = np.array(value)
        if arr.dtype.kind in {"S", "U", "O"}:  # bytes/str/object
            s = arr.astype(str)
            # For scalar values, collapse to a string; for char arrays, join
            if s.ndim == 0:
                return str(s)
            elif s.ndim == 1:
                return "".join(s).strip()
            else:
                # Multi-dim arrays: just join everything
                return "".join(s.flatten()).strip()
        else:
            return str(value)
    except Exception:
        return str(value)


def extract_profiles_from_netcdf(file_path: Path) -> List[Dict]:
    """Extract Argo profiles from a NetCDF file and return as documents."""
    logger.info(f"Processing file: {file_path}")
    
    try:
        ds = xr.open_dataset(file_path)
        logger.info(f"Dataset dimensions: {dict(ds.dims)}")
        
        # Extract basic info
        n_prof = ds.dims.get("N_PROF", 0)
        if n_prof == 0:
            logger.warning("No profiles found in dataset")
            return []
        
        documents = []
        
        for i in range(n_prof):
            try:
                # Extract profile metadata
                float_id = int(ds["PLATFORM_NUMBER"].isel(N_PROF=i).values)
                cycle_number = int(ds["CYCLE_NUMBER"].isel(N_PROF=i).values)
                
                # Create document ID
                doc_id = f"{float_id}_{cycle_number}"
                
                # Extract time (convert JULD to datetime)
                juld = float(ds["JULD"].isel(N_PROF=i).values)
                # JULD is days since 1950-01-01
                reference_date = pd.Timestamp("1950-01-01")
                profile_time = reference_date + pd.Timedelta(days=juld)
                
                # Extract location
                lat = float(ds["LATITUDE"].isel(N_PROF=i).values)
                lon = float(ds["LONGITUDE"].isel(N_PROF=i).values)
                
                # Extract project name if available
                project_name = "Unknown"
                if "PROJECT_NAME" in ds:
                    project_name = _decode_bytes(ds["PROJECT_NAME"].isel(N_PROF=i).values)
                
                # Extract measurements (PRES, TEMP, PSAL)
                measurements = []
                n_levels = ds.dims.get("N_LEVELS", 0)
                
                for level in range(n_levels):
                    try:
                        pres = ds["PRES"].isel(N_PROF=i, N_LEVELS=level).values
                        temp = ds["TEMP"].isel(N_PROF=i, N_LEVELS=level).values
                        psal = ds["PSAL"].isel(N_PROF=i, N_LEVELS=level).values
                        
                        # Skip if any measurement is NaN or fill value
                        if (np.isnan(pres) or np.isnan(temp) or np.isnan(psal) or
                            pres > 99990 or temp > 99990 or psal > 99990):
                            continue
                        
                        measurements.append({
                            "pressure": float(pres),
                            "temperature": float(temp),
                            "salinity": float(psal)
                        })
                    except (ValueError, KeyError) as e:
                        continue
                
                # Create document
                doc = {
                    "_id": doc_id,
                    "float_id": float_id,
                    "cycle_number": cycle_number,
                    "time": profile_time.to_pydatetime(),
                    "project_name": project_name,
                    "location": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "measurements": measurements
                }
                
                documents.append(doc)
                
            except Exception as e:
                logger.error(f"Error processing profile {i}: {e}")
                continue
        
        logger.info(f"Extracted {len(documents)} profiles from {file_path}")
        return documents
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return []
    finally:
        if 'ds' in locals():
            ds.close()


def ingest_files_to_mongodb(data_dir: Path, mongo_uri: str, db_name: str, collection_name: str):
    """Ingest all NetCDF files from data directory to MongoDB."""
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    
    logger.info(f"Connected to MongoDB: {db_name}.{collection_name}")
    
    # Find all NetCDF files
    nc_files = list(data_dir.glob("*.nc"))
    logger.info(f"Found {len(nc_files)} NetCDF files to process")
    
    total_inserted = 0
    total_errors = 0
    
    for nc_file in nc_files:
        try:
            documents = extract_profiles_from_netcdf(nc_file)
            
            if documents:
                # Insert documents in batch
                try:
                    result = collection.insert_many(documents, ordered=False)
                    inserted_count = len(result.inserted_ids)
                    total_inserted += inserted_count
                    logger.info(f"Inserted {inserted_count} documents from {nc_file.name}")
                    
                except BulkWriteError as e:
                    # Handle duplicate key errors gracefully
                    inserted_count = len(e.details.get("writeErrors", []))
                    duplicate_count = len([err for err in e.details.get("writeErrors", []) 
                                         if err.get("code") == 11000])
                    actual_inserted = len(documents) - len(e.details.get("writeErrors", []))
                    total_inserted += actual_inserted
                    
                    if duplicate_count > 0:
                        logger.info(f"Inserted {actual_inserted} new documents from {nc_file.name} "
                                  f"({duplicate_count} duplicates skipped)")
                    else:
                        logger.error(f"Bulk write errors for {nc_file.name}: {e}")
                        total_errors += 1
        
        except Exception as e:
            logger.error(f"Failed to process {nc_file.name}: {e}")
            total_errors += 1
    
    logger.info(f"Ingestion complete! Total inserted: {total_inserted}, Errors: {total_errors}")
    client.close()


def main():
    """Main ingestion function."""
    # Load environment variables
    load_dotenv()
    
    # Configuration
    data_dir = Path("data")
    mongo_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("DB_NAME", "argo_data")
    collection_name = os.getenv("COLLECTION_NAME", "profiles")
    
    if not mongo_uri:
        logger.error("MONGODB_URI not found in environment variables")
        return
    
    if not data_dir.exists():
        logger.error(f"Data directory {data_dir} not found")
        return
    
    logger.info("Starting Argo data ingestion...")
    ingest_files_to_mongodb(data_dir, mongo_uri, db_name, collection_name)
    logger.info("Ingestion completed!")


if __name__ == "__main__":
    main()
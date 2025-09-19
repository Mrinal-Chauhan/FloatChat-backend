"""NetCDF analysis script for Argo data."""

from __future__ import annotations

from pathlib import Path
import numpy as np
import xarray as xr


def analyze_netcdf(file_path: str | Path) -> None:
    """
    Open a NetCDF file and print a concise analysis of its contents.
    
    Args:
        file_path: Path to the NetCDF file to analyze
    """
    file_path = Path(file_path)
    
    try:
        with xr.open_dataset(file_path) as ds:
            print("--- Xarray Dataset Summary ---")
            print(ds)
            print("\n" + "=" * 50 + "\n")

            print("--- Global Attributes ---")
            if ds.attrs:
                for key, value in ds.attrs.items():
                    print(f"- {key}: {value}")
            else:
                print("(none)")
            print("\n" + "=" * 50 + "\n")

            print("--- Variables ---")
            for var_name, variable in ds.variables.items():
                print(f"\n- {var_name}")
                print(f"  dims: {variable.dims}")
                if variable.attrs:
                    print("  attrs:")
                    for k, v in variable.attrs.items():
                        print(f"    - {k}: {v}")
                sample = np.array(variable.values).ravel()[:5]
                print(f"  sample: {sample}")

    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
    except Exception as e:
        print(f"ERROR: {e}")


def main():
    """Main analysis function."""
    # Default to a representative file in the data directory for convenience
    root = Path(__file__).resolve().parents[1]  # Go up one level from scripts/
    candidates = sorted((root / "data").glob("*.nc"))
    
    if not candidates:
        print("No .nc files found in the data directory.")
        print(f"Looked in: {root / 'data'}")
    else:
        print(f"Analyzing: {candidates[0]}")
        analyze_netcdf(candidates[0])


if __name__ == "__main__":
    main()
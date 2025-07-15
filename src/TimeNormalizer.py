import pytz
import pandas as pd

class TimeNormalizer:

    @staticmethod
    def normalize_time(
            df: pd.DataFrame,
            column: str,
            timezone: str,
            input_format: str = "%Y-%m-%d %H:%M:%S",
            return_copy: bool = False
    ):
        print(f"Normalizing time in column '{column}' to timezone '{timezone}'")
        print(f"Actual Type is: {df[column].dtype}")
        print(f"First line is: {df[column].iloc[0]}")
        try:
            working_df = df.copy() if return_copy else df

            # Convert to datetime first (regardless of current type)
            working_df[column] = pd.to_datetime(
                working_df[column],
                format=input_format,
                errors='coerce'
            )
            print(f"New Type is: {working_df[column].dtype}")

            # Check if conversion failed completely
            if working_df[column].isna().all():
                raise ValueError(f"Could not parse any valid dates in column '{column}'")

            # Handle timezone conversion
            if working_df[column].dt.tz is None:
                # If no timezone info, localize first
                working_df[column] = working_df[column].dt.tz_localize(pytz.UTC)
            working_df[column] = working_df[column].dt.tz_convert(timezone)

            return working_df

        except Exception as e:
            print(f"Error while normalizing time: {e}")
            return None
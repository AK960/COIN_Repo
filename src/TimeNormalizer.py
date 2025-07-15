import pytz
import pandas as pd

class TimeNormalizer:

    @staticmethod
    def normalize_time(
            df: pd.DataFrame,
            column: str,
            timezone: str,
            input_format: str = "%a %b %d %H:%M:%S %z %Y",
            return_copy: bool = False
    ):
        try:
            working_df = df.copy()
            working_df[column] = pd.to_datetime(
                working_df[column],
                format=input_format,
                errors="coerce"
            )

            # Handle timezone conversion
            if working_df[column].dt.tz is None:
                # If no timezone info, localize first
                working_df[column] = working_df[column].dt.tz_localize(pytz.UTC)
            else:
                # If timezone info exists, convert directly
                working_df[column] = working_df[column].dt.tz_convert(timezone)

        except Exception as e:
            print(f"Error while normalizing time: {e}")
            return None

        return working_df
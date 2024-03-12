import pandas as pd


def extractLabel(import_path: str, export_path: str) -> None:
    """This functions extracts the shot type from the file
    specified in the import_path and saves it to export_path

    Args:
        import_path (str): path to the Garmin metrics csv file
        export_path (str): path to the export files
    """
    df = importFile(path=import_path)
    df = createShotType(df=df)
    writeLabel(df=df, path=export_path)


def importFile(path: str) -> pd.DataFrame:
    """This function import the Garmin metrix file as a data frame

    Args:
        path (str): path to the Garmin metrics csv file

    Returns:
        pd.DataFrame: pandas data frame
    """
    return pd.read_csv(path, header=[0], skiprows=[1])


def createShotType(df: pd.DataFrame) -> pd.DataFrame:
    """This function gets a data frame with columns Launch Direction
    and Sidespin and extracts the shot type.

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    df["Direction"] = df["Launch Direction"].apply(shot_direction)
    df["Shape"] = df["Sidespin"].apply(shot_curvature)
    df["ShotType"] = df["Direction"] + "-" + df["Shape"]
    return df[["ShotType"]]


def writeLabel(df: pd.DataFrame, path: str) -> None:
    """This function writes a data frame to a csv file

    Args:
        df (pd.DataFrame): data frame to be exported
        path (str): path to the export file
    """
    df["ShotType"].to_csv(path, index=False)


def shot_direction(x: float) -> str:
    """This function categorises the direction of the shot
    based on the launch direction

    Args:
        x (float): Launch direction [°]

    Returns:
        str: type of shot direction
    """
    if x < -5:
        return "pull"
    elif x > 5:
        return "push"
    else:
        return "straight"


def shot_curvature(x: float) -> str:
    """This function categorises the curvature of the shot
    based on the sidespin

    Args:
        x (float): Sidespin [rpm]

    Returns:
        str: the of curvature
    """
    if x < -800:
        return "slice"
    elif x < -300:
        return "fade"
    elif x < 300:
        return ""
    elif x < 800:
        return "draw"
    else:
        return "hook"

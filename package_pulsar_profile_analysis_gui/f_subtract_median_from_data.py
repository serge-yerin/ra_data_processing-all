from package_ra_data_processing.filtering import median_filter


def subtract_median_from_data(profile_data):

    # Subtraction of median from the data
    median = median_filter(profile_data, 100)
    profile_data = profile_data - median

    return profile_data

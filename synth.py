import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_cov_level=100, cov_level=100, unit_test_external_dependencies=["click"]
)
s.move(templated_files,
excludes=['docs/multiprocessing.rst'])

# Change black paths
s.replace(
    "noxfile.py",
    """BLACK_PATHS =.*""",
    """BLACK_PATHS = ["docs", "google_auth_oauthlib", "tests", "noxfile.py", "setup.py"]"""
)
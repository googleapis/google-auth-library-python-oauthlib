# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil

import nox

TEST_DEPENDENCIES = ["mock", "pytest", "pytest-cov", "futures", "click"]
BLACK_VERSION = "black==19.3b0"
BLACK_PATHS = ["google_auth_oauthlib", "tests", "noxfile.py", "setup.py"]


@nox.session(python="3.7")
def lint(session):
    session.install("flake8", "flake8-import-order", "docutils", BLACK_VERSION)
    session.install(".")
    session.run("black", "--check", *BLACK_PATHS)
    session.run(
        "flake8",
        "--import-order-style=google",
        "--application-import-names=google_auth_oauthlib,tests",
        "google_auth_oauthlib",
        "tests",
    )
    session.run(
        "python", "setup.py", "check", "--metadata", "--restructuredtext", "--strict"
    )


@nox.session(python="3.6")
def blacken(session):
    """Run black.

    Format code to uniform standard.

    This currently uses Python 3.6 due to the automated Kokoro run of synthtool.
    That run uses an image that doesn't have 3.6 installed. Before updating this
    check the state of the `gcp_ubuntu_config` we use for that Kokoro run.
    """
    session.install(BLACK_VERSION)
    session.run("black", *BLACK_PATHS)


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "pypy"])
def unit(session):
    session.install(*TEST_DEPENDENCIES)
    session.install(".")
    session.run("py.test", "--cov=google_auth_oauthlib", "--cov=tests", "tests")


@nox.session(python="3.7")
def cover(session):
    session.install(*TEST_DEPENDENCIES)
    session.install(".")
    session.run(
        "py.test", "--cov=google_auth_oauthlib", "--cov=tests", "--cov-report=", "tests"
    )
    session.run("coverage", "report", "--show-missing", "--fail-under=99")


def docgen(session):
    session.env["SPHINX_APIDOC_OPTIONS"] = "members,inherited-members,show-inheritance"
    session.install(*TEST_DEPENDENCIES, "sphinx")
    session.install(".")
    session.run("rm", "-rf", "docs/reference")
    session.run(
        "sphinx-apidoc",
        "--output-dir",
        "docs/reference",
        "--separate",
        "--module-first",
        "google_auth_oauthlib",
    )

@nox.session(python="3.7")
def docs(session):
    """Build the docs for this library."""

    docgen(session)
    session.install("sphinx", "-r", "docs/requirements-docs.txt")

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-W",  # warnings as errors
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )

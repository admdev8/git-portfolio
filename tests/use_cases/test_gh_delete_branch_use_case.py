"""Test cases for the Github delete branch use case."""
import pytest
from pytest_mock import MockerFixture

import git_portfolio.domain.config as c
import git_portfolio.use_cases.gh_delete_branch_use_case as ghdb


@pytest.fixture
def mock_github_manager(mocker: MockerFixture) -> MockerFixture:
    """Fixture for mocking GithubManager."""
    mock = mocker.patch("git_portfolio.github_manager.GithubManager", autospec=True)
    mock.return_value.config = c.Config(
        "", "mytoken", ["staticdev/omg", "staticdev/omg2"]
    )
    mock.return_value.delete_branch_from_repo.return_value = "success message\n"
    return mock


@pytest.fixture
def domain_branch() -> str:
    """Branch fixture."""
    return "my-branch"


def test_execute_for_all_repos(
    mock_github_manager: MockerFixture, domain_branch: str
) -> None:
    """It returns success."""
    github_manager = mock_github_manager.return_value
    response = ghdb.GhDeleteBranchUseCase(github_manager).execute(domain_branch)

    assert bool(response) is True
    assert "success message\nsuccess message\n" == response.value


def test_execute_for_specific_repo(
    mock_github_manager: MockerFixture, domain_branch: str
) -> None:
    """It returns success."""
    github_manager = mock_github_manager.return_value
    response = ghdb.GhDeleteBranchUseCase(github_manager).execute(
        domain_branch, "staticdev/omg"
    )

    assert bool(response) is True
    assert "success message\n" == response.value

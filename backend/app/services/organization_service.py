import json
import os
import random
import string
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import uuid4

from app.models.organization import (
    OrganizationInDB,
    OrganizationCreate,
    OrganizationPublic
)

# File path for organization JSON storage
ORGANIZATIONS_FILE_PATH = "backend/app/data/organizations.json"


def ensure_organizations_directory():
    """Ensure the data directory and organizations.json file exist."""
    directory = os.path.dirname(ORGANIZATIONS_FILE_PATH)

    os.makedirs(directory, exist_ok=True)

    if not os.path.exists(ORGANIZATIONS_FILE_PATH):
        with open(
            ORGANIZATIONS_FILE_PATH,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump([], file)


def load_organizations() -> List[Dict[str, Any]]:
    """Load organizations from JSON file."""
    ensure_organizations_directory()

    try:
        with open(
            ORGANIZATIONS_FILE_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

            return data if isinstance(data, list) else []

    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def save_organizations(
    organizations: List[Dict[str, Any]]
):
    """Save organizations to JSON file without recursion."""
    directory = os.path.dirname(ORGANIZATIONS_FILE_PATH)

    os.makedirs(directory, exist_ok=True)

    with open(
        ORGANIZATIONS_FILE_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            organizations,
            file,
            indent=2,
            default=str
        )


def generate_organization_code() -> str:
    """Generate an organization code like ORG-7F3K92."""
    random_chars = "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )

    return f"ORG-{random_chars}"


def is_organization_code_unique(code: str) -> bool:
    """Check whether an organization code is unique."""
    organizations = load_organizations()

    for organization in organizations:
        if organization.get("organization_code") == code:
            return False

    return True


def create_organization(
    organization_data: OrganizationCreate,
    owner_user_id: str
) -> OrganizationInDB:
    """Create a new organization."""

    organization_code = generate_organization_code()

    while not is_organization_code_unique(
        organization_code
    ):
        organization_code = generate_organization_code()

    new_organization = OrganizationInDB(
        id=str(uuid4()),
        organization_name=organization_data.organization_name,
        organization_code=organization_code,
        owner_user_id=owner_user_id,
        created_at=datetime.utcnow()
    )

    organizations = load_organizations()

    organizations.append(
        new_organization.model_dump()
    )

    save_organizations(organizations)

    return new_organization


def get_organization_by_id(
    organization_id: str
) -> Optional[OrganizationInDB]:
    """Get an organization by ID."""
    organizations = load_organizations()

    for organization_data in organizations:
        if organization_data.get("id") == organization_id:
            return OrganizationInDB(**organization_data)

    return None


def get_organization_by_code(
    organization_code: str
) -> Optional[OrganizationInDB]:
    """Get an organization by code."""
    organizations = load_organizations()

    for organization_data in organizations:
        if (
            organization_data.get("organization_code")
            == organization_code
        ):
            return OrganizationInDB(**organization_data)

    return None


def get_organization_by_owner(
    owner_user_id: str
) -> Optional[OrganizationInDB]:
    """Get an organization by owner user ID."""
    organizations = load_organizations()

    for organization_data in organizations:
        if (
            organization_data.get("owner_user_id")
            == owner_user_id
        ):
            return OrganizationInDB(**organization_data)

    return None


def list_organizations() -> List[OrganizationInDB]:
    """List all organizations."""
    organizations = load_organizations()

    return [
        OrganizationInDB(**organization_data)
        for organization_data in organizations
    ]
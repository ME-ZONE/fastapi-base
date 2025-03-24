import os
import re
import sys

# ANSI color codes for terminal output
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Ensure a migration path argument is provided
if len(sys.argv) < 2:
    print(f"{RED}Usage: python check_enum.py <MIGRATION_PATH>{RESET}")  # noqa: T201
    sys.exit(1)

MIGRATION_PATH = sys.argv[1]

# Regex patterns for detecting Enum creation and removal
ENUM_PATTERN = re.compile(r"sa\.Enum\((?:[^)]*?)name=['\"](\w+)['\"]", re.DOTALL)
DROP_ENUM_PATTERN = re.compile(r"op\.execute\(['\"]DROP TYPE IF EXISTS (\w+)['\"]\)")
COMMENTED_DROP_PATTERN = re.compile(r"#\s*op\.execute\(['\"]DROP TYPE IF EXISTS (\w+)['\"]\)")

def check_alembic_enum() -> None:
    """Scans Alembic migration files to ensure all added Enums are properly dropped in downgrade."""
    print(f"{RESET}Checking Enums in migrations...{RESET}")  # noqa: T201

    if not os.path.isdir(MIGRATION_PATH):
        print(f"{RED}Migration path '{MIGRATION_PATH}' does not exist!{RESET}")  # noqa: T201
        sys.exit(1)

    errors = []
    for filename in os.listdir(MIGRATION_PATH):
        if not filename.endswith(".py"):
            continue  # Skip non-Python files

        filepath = os.path.join(MIGRATION_PATH, filename)
        with open(filepath, encoding="utf-8") as file:
            content = file.read()

        upgrade_enums = set(ENUM_PATTERN.findall(content))
        downgrade_drops = set(DROP_ENUM_PATTERN.findall(content))
        commented_drops = set(COMMENTED_DROP_PATTERN.findall(content))

        # Check for missing Enum removals
        missing_drops = upgrade_enums - downgrade_drops
        if missing_drops:
            errors.append(
                f"{YELLOW}Migration {filename} defines Enum(s) {missing_drops}"
                f" but does not remove them in downgrade!{RESET}"
            )

        # Check for commented-out Enum drops
        if commented_drops:
            errors.append(
                f"{RED}Migration {filename} has commented-out Enum drop(s): {commented_drops}."
                f" Please uncomment them!{RESET}"
            )

    if errors:
        print("\n".join(errors))  # noqa: T201
        print(f"{RED}Enum issues detected in migrations!{RESET}") # noqa: T201
        sys.exit(1)  # Exit with error to indicate failed validation
    else:
        print(f"{GREEN}All migrations properly handle Enums!{RESET}") # noqa: T201


if __name__ == "__main__":
    check_alembic_enum()

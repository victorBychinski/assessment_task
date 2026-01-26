# BVNK API Testing Framework Task

---

## Getting Started

### Prerequisites

- **Python 3.14+**
- **uv** installed (The ultra-fast Python package manager)
  - Install via: `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux)
  - Or: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <assessment_task_path>
   ```

2. **Setup environment and dependencies:**
   ```bash
   uv sync
   ```

### Running Tests

The framework utilizes a centralized Config manager that prioritizes command-line arguments over static JSON configuration.

#### Basic Execution

Run the full suite with default settings from `config.json`:

```bash
uv run pytest
```

#### Execution with CLI Parameters

Override system parameters dynamically without modifying code:

```bash
# Run against a specific environment with a custom service fee
uv run pytest --base-url="https://bvnksimulator.pythonanywhere.com" --fee=0.01
```

**Available parameters:**
- `--base-url` - Base URL for the API
- `--fee` - Service fee percentage (e.g., 0.01)
- `--precision` - Decimal precision for amounts

#### Targeted Testing (Markers)

```bash
# Run mandatory E2E trade scenarios
uv run pytest -m e2e
```

### Project Structure

- **clients/** - Low-level API wrappers for Quote, Wallet, and Authorization endpoints
- **services/** - High-level orchestrators that manage complex workflows
- **models/** - Pydantic schemas ensuring type safety of API responses
- **utils/** - Shared logic for Decimal math, fee calculations, and balance comparisons
- **configuration/** - Framework configuration

### Assumptions

- The `/init` endpoint creates an account with a consistent baseline
- Account has multiple wallets with sufficient funds for E2E tests
- Framework does not manage any test data cleanup (this is a test task)
- No reporting integration
- No Dockerization
- Models validation and required fields rules are not added for simplicity.

### TODO

- Extend test coverage
- Add reporting
- Custom error handling




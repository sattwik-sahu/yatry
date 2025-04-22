# Yatry

Hassle-Free Ride Sharing powered by Advanced Optimization Algorithms

## Installation

### Prerequisites

1. [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/) for dependency management
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

### Setup

1. Fork the repo and clone your fork
    ```bash
    git clone https://github.com/<your_username>/yatry
    ```
3. Create the virtual environment and install dependencies
    ```bash
    uv sync
    ```

> `uv` will install the required Python version automatically from [`pyproject.toml`](./pyproject.toml)

## Contributing

1. Set up remote to sync changes with your fork
    ```bash
    git remote add origin https://github.com/<your_username>/yatry
    ```
2. Create a new branch in your fork
    ```bash
    git checkout -b <your_branch_name>
    ```
3. Commit your changes
    ```bash
    git add .
    git commit -m "<your_commit_message>"
    ```
    > To know more about meaningful commit messages, follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary).
4. Push your changes to your fork
    ```bash
    git push -u origin <your_branch_name>
    ```
5. Go to your fork on GitHub and create a pull request from your branch.

---

Made in IISER Bhopal

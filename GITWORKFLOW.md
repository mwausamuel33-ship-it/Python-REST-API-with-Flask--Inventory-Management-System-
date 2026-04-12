# Git Workflow Documentation

## Repository Structure

This project demonstrates a proper Git workflow with multiple branches:

```
* master (main production branch)
* develop (development branch)
```

## Commits

```
a22a9bf - Add comprehensive test suite and documentation
fe699a8 - Initial commit: Add Flask app, CLI interface, requirements
```

## Branch Strategy

The project follows a Git Flow workflow with:
- **master**: Production-ready code
- **develop**: Integration branch for features

## What Was Implemented

### Feature 1: Flask REST API with CRUD Endpoints
- File: `app.py`
- Includes: GET, POST, PATCH, DELETE routes
- External API integration endpoint

### Feature 2: CLI Interface
- File: `cli.py`
- Interactive menu for all CRUD operations
- Integration with external API

### Feature 3: Unit Testing
- File: `test_app.py`
- 22 comprehensive tests
- Full endpoint coverage

## Git Commands Used

```bash
# Initialize repository
git init
git config user.email "dev@example.com"
git config user.name "Developer"

# Create and switch branches
git checkout -b develop
git checkout -b master

# Make commits
git add .
git commit -m "commit message"

# Switch between branches
git checkout develop
git checkout master

# View branch status
git branch -a
git log --graph --oneline --all
```

## Merging Strategy

When features are complete:
1. Test thoroughly on feature branch
2. Switch to develop: `git checkout develop`
3. Merge feature: `git merge feature/branch-name`
4. After release testing, merge develop to master: `git merge develop`

## Best Practices Demonstrated

✓ Meaningful commit messages
✓ Separate branches for different purposes
✓ Clean repository structure
✓ Proper .gitignore configuration
✓ Clear project documentation

# Contributing to Aegis AI

Thank you for your interest in contributing! 🎉

## Development Setup

1. Fork the repository
2. Clone your fork
3. Follow setup instructions in `docs/SETUP.md`
4. Create a new branch for your feature

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Use async/await for I/O operations

```python
async def generate_scenario(label: str, difficulty: Difficulty) -> ScenarioResponse:
    """Generate AI-powered phishing scenario."""
    # Implementation
```

### JavaScript (Frontend)
- Use ES6+ features
- Clear variable names
- Add comments for complex logic
- Follow existing code structure

```javascript
async function startSim(ctx) {
    // Generate and display scenario
}
```

### SQL
- Use lowercase for keywords
- Descriptive table/column names
- Add comments for complex queries

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add senior citizen quiz mode
fix: Correct leaderboard sorting issue
docs: Update API documentation
refactor: Simplify scenario scoring logic
```

## Testing

Before submitting:
1. Test all modified endpoints
2. Check browser console for errors
3. Verify mobile responsiveness
4. Test with different scenarios

## Pull Request Process

1. Update documentation if needed
2. Test thoroughly
3. Create PR with clear description
4. Reference any related issues

## Feature Ideas

- Multi-language support
- Email notification system
- Advanced analytics dashboard
- Integration with Slack/Teams
- Custom scenario templates
- Reporting & export features

## Bug Reports

Please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Browser/OS information

## Questions?

Open an issue for discussion!

---

**Thank you for contributing to cybersecurity awareness! 🛡️**

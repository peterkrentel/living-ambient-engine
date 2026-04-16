# Contributing to Living Ambient Engine

Thank you for your interest in contributing! This project thrives on community input.

## How Can You Contribute?

### 🐛 Report Bugs
Found a bug? [Open an issue](https://github.com/peterkrentel/living-ambient-engine/issues/new) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System info (OS, Python version)
- Error messages or logs

### 💡 Suggest Features
Have an idea? [Open an issue](https://github.com/peterkrentel/living-ambient-engine/issues/new) with:
- What problem it solves
- Proposed solution
- Use cases
- Alternative approaches considered

### 📖 Improve Documentation
- Fix typos or unclear explanations
- Add examples or tutorials
- Translate documentation
- Create video guides

### 🎨 Enhance Visuals
- New fractal patterns
- Sacred geometry designs
- Color schemes
- Animation effects

### 🎵 Improve Audio
- New rhythm patterns
- Additional instruments
- Better binaural beat generation
- Sound effects

### 🧪 Add Tests
- Unit tests for audio/visual modules
- Integration tests for pipeline
- Performance benchmarks
- CI/CD improvements

## Development Setup

### 1. Fork and Clone
```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/living-ambient-engine.git
cd living-ambient-engine
```

### 2. Create Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Make Changes
- Follow existing code style
- Add comments for complex logic
- Update documentation if needed

### 5. Test Your Changes
```bash
# Test video generation
python run_job.py --mood trance --duration 30

# Test batch generation
python batch_generate.py --moods sleep,study --durations 30s

# Run any existing tests
python -m pytest  # If tests exist
```

### 6. Commit and Push
```bash
git add .
git commit -m "feat: add amazing feature"
git push origin feature/your-feature-name
```

### 7. Open Pull Request
- Go to GitHub
- Click "New Pull Request"
- Describe your changes
- Reference related issues

## Coding Guidelines

### Python Style
- Follow PEP 8
- Use type hints where helpful
- Keep functions focused and small
- Add docstrings for public functions

### Commit Messages
Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Tests
- `chore:` Maintenance

Examples:
```
feat: add new meditation mood preset
fix: resolve audio sync issue
docs: update installation instructions
```

### Documentation
- Use Markdown for docs
- Include code examples
- Keep it beginner-friendly
- Update relevant files (README, GETTING_STARTED, etc.)

## Project Structure

Understanding the codebase:

```
├── audio/              # Audio generation modules
├── visuals/            # Visual generation modules
├── render/             # FFmpeg rendering pipeline
├── orchestrator/       # Job coordination
├── config/             # Configuration files
├── docs/               # Documentation
├── scripts/            # Utility scripts
├── .github/            # GitHub Actions workflows
├── run_job.py          # Main CLI entry point
├── batch_generate.py   # Batch generation CLI
└── youtube_upload.py   # YouTube upload CLI
```

## Testing Guidelines

### Manual Testing
Always test your changes:
1. Generate a short video (30s)
2. Verify output plays correctly
3. Check audio and visuals sync
4. Ensure metadata is generated

### Automated Testing
If adding tests:
- Use `pytest` framework
- Place in `tests/` directory
- Mock expensive operations
- Aim for >80% coverage

## Feature Development

### Adding a New Mood
1. Edit `config/moods.yaml`
2. Add preset with parameters
3. Test generation
4. Update documentation
5. Add to mood table in README

### Adding Visual Effects
1. Create module in `visuals/`
2. Implement generation function
3. Register in visual pipeline
4. Test performance
5. Document parameters

### Adding Audio Patterns
1. Create module in `audio/`
2. Implement synthesis function
3. Register in audio pipeline
4. Test audio quality
5. Document usage

## Spec-Driven Development

This project uses **spec-driven development** to keep AI agents and humans aligned. **Orientation:** [`docs/START_HERE.md`](docs/START_HERE.md) — do not duplicate that map in PRs or new docs. **Every markdown file:** [`docs/MARKDOWN_INDEX.md`](docs/MARKDOWN_INDEX.md).

### Spec Structure

```
docs/
├── START_HERE.md       # Doc map: handoff vs spec vs ADR vs chat (read first for orientation)
├── HANDOFF.md          # Active work snapshot (short; overwrite when state moves)
└── decisions/          # ADRs — why a decision was made

docs/spec/
├── SYSTEM.md           # Canonical system spec (governance + invariants)
├── contracts/          # Component interface contracts
│   ├── orchestrator-audio.md
│   ├── orchestrator-visual.md
│   └── orchestrator-youtube.md
└── workflows.md        # GitHub Actions specs

audio/SPEC.md           # Audio generator spec
visuals/SPEC.md         # Visual generator spec
orchestrator/SPEC.md    # Orchestrator spec
youtube/SPEC.md         # YouTube uploader spec
config/SPEC.md          # Configuration spec
render/SPEC.md          # FFmpeg renderer spec
```

### The Spec-First Rule

> **Any change to cross-component behavior requires a spec update in the same PR.**

Examples requiring spec updates:
- New config parameters affecting multiple components
- Changes to data flow between components
- New workflow inputs or outputs
- API/interface changes

### PR Checklist

Every PR should verify:

- [ ] **Spec reviewed** - Read relevant specs before coding
- [ ] **Spec updated** - Changed behavior = updated spec (or N/A)
- [ ] **Contract honored** - Component interfaces match contracts
- [ ] **Tests added** - Acceptance criteria have tests
- [ ] **Docs updated** - User-facing changes reflected in docs

### Working with AI Agents

When using AI assistants (Copilot, Claude, etc.):

1. **Point to specs first**: "Read `docs/spec/SYSTEM.md` and `audio/SPEC.md`"
2. **Request spec extraction**: "List requirements you found in the spec"
3. **Verify alignment**: "Show how each requirement is satisfied"
4. **Enforce updates**: "Update the spec if behavior changed"

This reduces AI drift and keeps implementations consistent.

## Code Review Process

### What We Look For
- ✅ Functionality works as described
- ✅ Code is clean and readable
- ✅ Documentation is updated
- ✅ Spec is updated (if behavior changed)
- ✅ No breaking changes (or clearly noted)
- ✅ Follows project style

### Review Timeline
- Initial feedback: 1-3 days
- Revisions as needed
- Merge when approved

## Community Guidelines

### Be Respectful
- Treat everyone with kindness
- Assume good intentions
- Provide constructive feedback
- Celebrate contributions

### Be Patient
- Maintainers are volunteers
- Reviews take time
- Discussion is healthy
- Quality over speed

### Be Helpful
- Answer questions
- Share knowledge
- Mentor newcomers
- Improve documentation

## Getting Help

### Stuck?
- Check [FAQ](docs/FAQ.md)
- Read [Getting Started](docs/GETTING_STARTED.md)
- Search existing issues
- Ask in discussions

### Need Guidance?
- Comment on related issues
- Ask before major changes
- Request feedback early
- Collaborate openly

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- Special thanks in docs

## Questions?

Open an issue or start a discussion. We're here to help!

---

**Thank you for contributing to Living Ambient Engine! 🎨🎵🙏**

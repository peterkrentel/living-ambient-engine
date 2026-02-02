"""
Contract tests for Workflow Metadata Consistency.

Verifies that all workflows use youtube_upload.py for uploads
and do not generate metadata inline.

Spec: docs/spec/workflows.md § Metadata Consistency Rule
Guardrails: docs/spec/GUARDRAILS.md § Metadata Consistency Violations  
Contract: docs/spec/contracts/orchestrator-youtube.md § Workflow Integration
"""

import pytest
import os
import re
from pathlib import Path


# Get paths relative to repo root
REPO_ROOT = Path(__file__).parent.parent.parent
WORKFLOWS_DIR = REPO_ROOT / '.github' / 'workflows'


class TestWorkflowMetadataConsistency:
    """Ensure all upload workflows use youtube_upload.py."""
    
    # Workflows that upload to YouTube
    UPLOAD_WORKFLOWS = [
        'content-factory.yml',
        'content-factory-brand.yml',
        'art-creator.yml',
    ]
    
    # Patterns that indicate forbidden inline metadata generation
    FORBIDDEN_PATTERNS = [
        # Inline Python generating description/tags directly for upload
        r'uploader\.upload\([^)]*description\s*=\s*description',
        r'uploader\.upload\([^)]*tags\s*=\s*tags',
        # Hardcoded tags list in upload call
        r"tags\s*=\s*\[\s*['\"]ambient['\"]",
        # Direct YouTubeUploader usage in workflow (should use youtube_upload.py CLI)
        r'from youtube\.uploader import YouTubeUploader',
    ]
    
    # Required pattern - must call youtube_upload.py
    ALLOWED_PATTERN = r'python\s+youtube_upload\.py'
    
    @pytest.fixture
    def upload_workflow_files(self):
        """Load content of all upload workflows."""
        workflows = {}
        for name in self.UPLOAD_WORKFLOWS:
            path = WORKFLOWS_DIR / name
            if path.exists():
                workflows[name] = path.read_text()
        return workflows
    
    def test_all_upload_workflows_exist(self):
        """All expected upload workflows should exist."""
        for name in self.UPLOAD_WORKFLOWS:
            path = WORKFLOWS_DIR / name
            assert path.exists(), f"Workflow {name} should exist"
    
    def test_upload_workflows_use_youtube_upload_py(self, upload_workflow_files):
        """All upload workflows must use youtube_upload.py."""
        for name, content in upload_workflow_files.items():
            assert re.search(self.ALLOWED_PATTERN, content), \
                f"{name} must use 'python youtube_upload.py' for uploads. " \
                "See: docs/spec/contracts/orchestrator-youtube.md § Workflow Integration"
    
    def test_no_inline_metadata_generation(self, upload_workflow_files):
        """Workflows must not generate metadata inline."""
        for name, content in upload_workflow_files.items():
            for pattern in self.FORBIDDEN_PATTERNS:
                match = re.search(pattern, content)
                assert not match, \
                    f"{name} contains forbidden inline metadata pattern: {pattern}. " \
                    f"Found: {match.group() if match else 'N/A'}. " \
                    "See: docs/spec/GUARDRAILS.md § Metadata Consistency Violations"


class TestMetadataFlowIntegrity:
    """Ensure metadata flows from moods.yaml through the pipeline."""
    
    def test_moods_yaml_has_required_fields(self):
        """All moods in moods.yaml should have SEO fields."""
        import yaml
        
        moods_path = REPO_ROOT / 'config' / 'moods.yaml'
        assert moods_path.exists(), "config/moods.yaml must exist"
        
        with open(moods_path) as f:
            moods = yaml.safe_load(f)
        
        for name, config in moods.items():
            # Skip non-mood entries (like defaults)
            if not isinstance(config, dict):
                continue
            
            # Check for SEO fields
            assert 'tags' in config, \
                f"Mood '{name}' missing 'tags' field. " \
                "See: config/SPEC.md § moods.yaml Schema"
            
            assert 'description_template' in config, \
                f"Mood '{name}' missing 'description_template' field. " \
                "See: config/SPEC.md § moods.yaml Schema"
            
            # Tags should be a list
            assert isinstance(config['tags'], list), \
                f"Mood '{name}' tags must be a list"
            
            # Tags should not be empty
            assert len(config['tags']) > 0, \
                f"Mood '{name}' must have at least one tag"
    
    def test_youtube_upload_reads_metadata(self):
        """youtube_upload.py should read from metadata.json."""
        upload_script = REPO_ROOT / 'youtube_upload.py'
        assert upload_script.exists(), "youtube_upload.py must exist"
        
        content = upload_script.read_text()
        
        # Must support description_template
        assert 'description_template' in content, \
            "youtube_upload.py must support description_template field"
        
        # Must support tags from metadata
        assert "meta.get('tags'" in content or 'tags' in content, \
            "youtube_upload.py must read tags from metadata"


class TestGuardrailEnforcement:
    """Verify guardrails documentation matches enforcement."""
    
    def test_guardrails_has_metadata_section(self):
        """GUARDRAILS.md must document metadata consistency violations."""
        guardrails_path = REPO_ROOT / 'docs' / 'spec' / 'GUARDRAILS.md'
        assert guardrails_path.exists()
        
        content = guardrails_path.read_text()
        
        assert 'Metadata Consistency Violations' in content, \
            "GUARDRAILS.md must have Metadata Consistency Violations section"
        
        assert 'youtube_upload.py' in content, \
            "GUARDRAILS.md must mention youtube_upload.py as required tool"
    
    def test_contract_has_workflow_integration(self):
        """orchestrator-youtube.md must document workflow integration rules."""
        contract_path = REPO_ROOT / 'docs' / 'spec' / 'contracts' / 'orchestrator-youtube.md'
        assert contract_path.exists()
        
        content = contract_path.read_text()
        
        assert 'Workflow Integration' in content, \
            "Contract must have Workflow Integration section"
        
        assert 'Forbidden Pattern' in content, \
            "Contract must document forbidden patterns"


#!/usr/bin/env python3
"""
Art Combination Selector for Daily Art Creator Workflow

This script manages the automated cycling through Art Creator combinations.
It reads the list of available combinations, tracks which have been used,
and selects the next unused combination for daily art generation.

Usage:
    python select_art_combo.py [--reset] [--status] [--dry-run]

Options:
    --reset     Reset tracking to start from the beginning
    --status    Show current status without selecting a new combination
    --dry-run   Select next combination but don't update tracking file

Environment Variables (set by GitHub Actions):
    GITHUB_OUTPUT - Path to file where outputs will be written for GitHub Actions

Outputs (written to $GITHUB_OUTPUT):
    selected_id            - ID of the selected combination
    selected_name          - Name of the selected combination
    art_period             - Art historical period
    visual_pattern         - Visual pattern type
    visual_speed           - Visual speed value
    visual_complexity      - Visual complexity value
    color_palette          - Color palette
    music_style            - Music style
    tempo                  - Tempo value
    brainwave_frequency    - Brainwave frequency
    solfeggio_frequency    - Solfeggio frequency
    rhythm_volume          - Rhythm volume
    ambient_volume         - Ambient volume
    journey                - Journey type
    journey_intensity      - Journey intensity
    duration               - Duration
    all_completed          - "true" if all combinations have been used, "false" otherwise
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


class ArtCombinationSelector:
    """Manages selection and tracking of Art Creator combinations."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize the selector.
        
        Args:
            base_dir: Base directory for data files (defaults to .github/data)
        """
        if base_dir is None:
            # Default to .github/data relative to repo root
            repo_root = Path(__file__).parent.parent.parent
            base_dir = repo_root / ".github" / "data"
        
        self.base_dir = Path(base_dir)
        self.combinations_file = self.base_dir / "art-combinations.json"
        self.tracking_file = self.base_dir / "art-tracking.json"
        
    def load_combinations(self) -> Dict[str, Any]:
        """Load the combinations data file."""
        try:
            with open(self.combinations_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: Combinations file not found: {self.combinations_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in combinations file: {e}", file=sys.stderr)
            sys.exit(1)
    
    def load_tracking(self) -> Dict[str, Any]:
        """Load the tracking data file."""
        try:
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: Tracking file not found: {self.tracking_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in tracking file: {e}", file=sys.stderr)
            sys.exit(1)
    
    def save_tracking(self, tracking: Dict[str, Any]) -> None:
        """Save the updated tracking data."""
        tracking['last_updated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(tracking, f, indent=2)
                f.write('\n')  # Add trailing newline
        except Exception as e:
            print(f"❌ Error: Failed to save tracking file: {e}", file=sys.stderr)
            sys.exit(1)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of combination usage."""
        combinations_data = self.load_combinations()
        tracking = self.load_tracking()
        
        total = len(combinations_data['combinations'])
        used = len(tracking['used_combinations'])
        remaining = total - used
        
        return {
            'total_combinations': total,
            'used_combinations': used,
            'remaining_combinations': remaining,
            'current_index': tracking['current_index'],
            'completed': tracking['completed'],
            'last_updated': tracking['last_updated']
        }
    
    def select_next_combination(self, dry_run: bool = False) -> Optional[Dict[str, Any]]:
        """
        Select the next unused combination.
        
        Args:
            dry_run: If True, don't update the tracking file
            
        Returns:
            Dictionary with combination data, or None if all combinations are used
        """
        combinations_data = self.load_combinations()
        tracking = self.load_tracking()
        
        combinations = combinations_data['combinations']
        
        # Check if all combinations have been used
        if tracking['completed']:
            print("ℹ️  All combinations have already been used.")
            return None
        
        # Find next unused combination
        current_index = tracking['current_index']
        
        if current_index >= len(combinations):
            print("ℹ️  All combinations have been used.")
            tracking['completed'] = True
            if not dry_run:
                self.save_tracking(tracking)
            return None
        
        # Get the next combination
        selected = combinations[current_index]
        
        print(f"✅ Selected combination {current_index + 1}/{len(combinations)}")
        print(f"   ID: {selected['id']}")
        print(f"   Name: {selected['name']}")
        print(f"   Art Period: {selected['art_period']}")
        print(f"   Visual Pattern: {selected['visual_pattern']}")
        print(f"   Music Style: {selected['music_style']}")
        print(f"   Journey: {selected['journey']}")
        
        # Update tracking
        if not dry_run:
            tracking['used_combinations'].append({
                'id': selected['id'],
                'name': selected['name'],
                'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                'index': current_index
            })
            tracking['current_index'] = current_index + 1
            
            # Mark as completed if this was the last one
            if tracking['current_index'] >= len(combinations):
                tracking['completed'] = True
                print("ℹ️  This was the last combination!")
            
            self.save_tracking(tracking)
            print(f"✅ Tracking file updated")
        else:
            print("ℹ️  Dry run - tracking file not updated")
        
        return selected
    
    def reset_tracking(self) -> None:
        """Reset tracking to start from the beginning."""
        combinations_data = self.load_combinations()
        total = len(combinations_data['combinations'])
        
        tracking = {
            'description': 'Tracks which Art Creator combinations have been used',
            'last_updated': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'current_index': 0,
            'used_combinations': [],
            'total_combinations': total,
            'completed': False
        }
        
        self.save_tracking(tracking)
        print(f"✅ Tracking reset - ready to cycle through {total} combinations")
    
    def write_github_output(self, combination: Dict[str, Any], all_completed: bool) -> None:
        """
        Write combination parameters to GitHub Actions output file.
        
        Args:
            combination: The selected combination data
            all_completed: Whether all combinations have been used
        """
        github_output = os.environ.get('GITHUB_OUTPUT')
        if not github_output:
            print("⚠️  GITHUB_OUTPUT environment variable not set - skipping output write")
            return
        
        try:
            with open(github_output, 'a') as f:
                # Write each parameter
                f.write(f"selected_id={combination['id']}\n")
                f.write(f"selected_name={combination['name']}\n")
                f.write(f"art_period={combination['art_period']}\n")
                f.write(f"visual_pattern={combination['visual_pattern']}\n")
                f.write(f"visual_speed={combination['visual_speed']}\n")
                f.write(f"visual_complexity={combination['visual_complexity']}\n")
                f.write(f"color_palette={combination['color_palette']}\n")
                f.write(f"music_style={combination['music_style']}\n")
                f.write(f"tempo={combination['tempo']}\n")
                f.write(f"brainwave_frequency={combination['brainwave_frequency']}\n")
                f.write(f"solfeggio_frequency={combination['solfeggio_frequency']}\n")
                f.write(f"rhythm_volume={combination['rhythm_volume']}\n")
                f.write(f"ambient_volume={combination['ambient_volume']}\n")
                f.write(f"journey={combination['journey']}\n")
                f.write(f"journey_intensity={combination['journey_intensity']}\n")
                f.write(f"duration={combination['duration']}\n")
                f.write(f"all_completed={'true' if all_completed else 'false'}\n")
            
            print(f"✅ Wrote outputs to {github_output}")
        except Exception as e:
            print(f"❌ Error writing to GITHUB_OUTPUT: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Select next Art Creator combination for daily workflow'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset tracking to start from the beginning'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show current status without selecting a combination'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Select combination but do not update tracking file'
    )
    
    args = parser.parse_args()
    
    selector = ArtCombinationSelector()
    
    # Handle reset
    if args.reset:
        selector.reset_tracking()
        return
    
    # Handle status
    if args.status:
        status = selector.get_status()
        print(f"\n📊 Art Creator Combination Status")
        print(f"   Total combinations: {status['total_combinations']}")
        print(f"   Used: {status['used_combinations']}")
        print(f"   Remaining: {status['remaining_combinations']}")
        print(f"   Current index: {status['current_index']}")
        print(f"   Completed: {status['completed']}")
        print(f"   Last updated: {status['last_updated']}")
        return
    
    # Select next combination
    combination = selector.select_next_combination(dry_run=args.dry_run)
    
    if combination is None:
        # All combinations used - write a marker to GITHUB_OUTPUT
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output and not args.dry_run:
            try:
                with open(github_output, 'a') as f:
                    f.write("all_completed=true\n")
                    f.write("selected_id=0\n")
            except Exception as e:
                print(f"⚠️  Warning: Could not write to GITHUB_OUTPUT: {e}", file=sys.stderr)
        
        print("\n⚠️  All combinations have been used. No new art will be generated.")
        print("   To start over, run with --reset flag")
        sys.exit(0)
    else:
        # Write outputs for GitHub Actions
        if not args.dry_run:
            selector.write_github_output(combination, all_completed=False)


if __name__ == '__main__':
    main()

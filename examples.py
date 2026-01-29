#!/usr/bin/env python3
"""
Interactive Examples for Living Ambient Engine

Run this script to see demonstrations of what you can create!
Make sure dependencies are installed first: pip install -r requirements.txt
"""

import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if the project dependencies are installed."""
    try:
        import click
        import yaml
        return True
    except ImportError as e:
        print("\n⚠️  Warning: Some dependencies are not installed.")
        print(f"   Missing: {e.name}")
        print("\nPlease run:")
        print("   pip install -r requirements.txt")
        print("\nThen try again.\n")
        return False


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_section(text):
    """Print a section header."""
    print(f"\n{'─' * 70}")
    print(f"  {text}")
    print(f"{'─' * 70}\n")


def show_welcome():
    """Show welcome message."""
    print_header("🎨 Welcome to Living Ambient Engine! 🎵")
    print("This interactive guide will show you what you can create.")
    print("\nLiving Ambient Engine generates hypnotic ambient videos with:")
    print("  • Mesmerizing fractal visuals")
    print("  • Tribal drum patterns")
    print("  • Binaural beats for brainwave entrainment")
    print("  • Healing Solfeggio frequencies")
    print("\nPerfect for YouTube monetization in meditation/focus/sleep niches!")


def show_menu():
    """Display the main menu."""
    print_section("What would you like to do?")
    print("1. 🧪 Quick Demo (30 seconds) - Test the engine")
    print("2. 😴 Sleep Aid (5 minutes) - Bedtime meditation")
    print("3. 🧠 Deep Focus (5 minutes) - Work/study session")
    print("4. 🌀 Trance State (5 minutes) - Meditation journey")
    print("5. ⚡ Energy Boost (5 minutes) - Morning motivation")
    print("6. 📚 Batch Generate - Create multiple videos")
    print("7. 📖 View Documentation")
    print("8. ❓ Show FAQ")
    print("9. 🚀 Advanced Options")
    print("0. 👋 Exit")
    print()


def run_example(mood, duration, description):
    """Run a video generation example."""
    print_section(f"Generating: {description}")
    print(f"Mood: {mood}")
    print(f"Duration: {duration} seconds")
    print("\nCommand being run:")
    print(f"  python run_job.py --mood {mood} --duration {duration}")
    print("\nGenerating... (this may take a few minutes)")
    
    try:
        result = subprocess.run(
            ["python", "run_job.py", "--mood", mood, "--duration", str(duration)],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✅ Success! Video generated in output/ directory")
            print("   Check output/ for your video, thumbnail, and metadata")
        else:
            print(f"\n❌ Error: Command failed with code {result.returncode}")
            print("   Make sure you've run: pip install -r requirements.txt")
            
    except FileNotFoundError:
        print("\n❌ Error: Python not found or script not in current directory")
        print("   Make sure you're in the project root directory")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def show_documentation():
    """Show available documentation."""
    print_section("📖 Available Documentation")
    
    docs = {
        "Getting Started": "docs/GETTING_STARTED.md",
        "Quick Reference": "docs/QUICK_REFERENCE.md",
        "FAQ": "docs/FAQ.md",
        "Architecture": "docs/architecture.md",
        "YouTube Setup": "docs/youtube-auth.md",
        "Master Plan": "docs/master-plan.md"
    }
    
    for name, path in docs.items():
        doc_path = Path(path)
        status = "✅" if doc_path.exists() else "❌"
        print(f"{status} {name}: {path}")
    
    print("\nTip: Open these files in your text editor or browser!")


def show_faq():
    """Show quick FAQ."""
    print_section("❓ Frequently Asked Questions")
    
    faqs = [
        ("What is this?", "An automated system for creating ambient videos for YouTube"),
        ("Is it free?", "Yes! Open source (MIT License) and free to use"),
        ("Can I monetize?", "Absolutely! Perfect for YouTube Partner Program"),
        ("What do I need?", "Python 3.9+, FFmpeg, and this repository"),
        ("How long does generation take?", "~2-5 minutes per minute of video"),
        ("Can I customize?", "Yes! Edit moods, colors, audio, and more"),
    ]
    
    for question, answer in faqs:
        print(f"\nQ: {question}")
        print(f"A: {answer}")
    
    print(f"\n📄 Full FAQ available at: docs/FAQ.md")


def show_advanced():
    """Show advanced options."""
    print_section("🚀 Advanced Options")
    
    print("Batch Generation:")
    print("  python batch_generate.py --moods all --durations 1h,2h")
    
    print("\nCustom Output Directory:")
    print("  python run_job.py --mood trance --duration 600 --output ./my_videos")
    
    print("\nYouTube Upload:")
    print("  python youtube_upload.py --file output/video.mp4")
    
    print("\nVerbose Logging:")
    print("  python run_job.py --mood sleep --duration 600 --verbose")
    
    print("\nAll Available Moods:")
    moods = ["deep_focus", "sleep", "chill", "study", "trance", "energize", "ceremony", "warrior"]
    for mood in moods:
        print(f"  • {mood}")
    
    print("\n📖 See docs/QUICK_REFERENCE.md for complete command list")


def main():
    """Main interactive loop."""
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    show_welcome()
    
    while True:
        show_menu()
        choice = input("Enter your choice (0-9): ").strip()
        
        if choice == "1":
            run_example("trance", 30, "Quick Demo - 30 second trance video")
        
        elif choice == "2":
            run_example("sleep", 300, "Sleep Aid - 5 minute delta wave meditation")
        
        elif choice == "3":
            run_example("deep_focus", 300, "Deep Focus - 5 minute gamma wave study session")
        
        elif choice == "4":
            run_example("trance", 300, "Trance State - 5 minute theta wave meditation")
        
        elif choice == "5":
            run_example("energize", 300, "Energy Boost - 5 minute beta wave energizer")
        
        elif choice == "6":
            print_section("📚 Batch Generation")
            print("Example batch commands:")
            print("\n1. Generate all moods (1 hour each):")
            print("   python batch_generate.py --moods all --durations 1h")
            print("\n2. Generate specific moods (multiple durations):")
            print("   python batch_generate.py --moods sleep,study --durations 30m,1h,2h")
            print("\n3. Quick test (all moods, 30 seconds):")
            print("   python batch_generate.py --moods all --durations 30s")
            input("\nPress Enter to continue...")
        
        elif choice == "7":
            show_documentation()
            input("\nPress Enter to continue...")
        
        elif choice == "8":
            show_faq()
            input("\nPress Enter to continue...")
        
        elif choice == "9":
            show_advanced()
            input("\nPress Enter to continue...")
        
        elif choice == "0":
            print("\n👋 Thanks for using Living Ambient Engine!")
            print("Happy creating! 🎨🎵🧘")
            print("\n💡 Tip: Star the repo on GitHub if you find it useful!")
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice. Please enter 0-9.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)

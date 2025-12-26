#!/bin/bash
# Documentation generation script for Haze-Library
# This script generates both Rust API documentation and Python documentation

set -e  # Exit on error

echo "🔧 Haze-Library Documentation Generator"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if rust directory exists
if [ ! -d "rust" ]; then
    echo -e "${RED}❌ Error: rust directory not found${NC}"
    exit 1
fi

# Function to generate Rust documentation
generate_rust_docs() {
    echo -e "\n${BLUE}📚 Generating Rust API Documentation...${NC}"
    cd "$PROJECT_ROOT/rust"

    # Generate documentation with available features (excluding polars due to disabled dependencies)
    cargo doc --no-deps --document-private-items --features "python streaming"

    # Check if documentation was generated
    if [ -d "target/doc" ]; then
        echo -e "${GREEN}✅ Rust documentation generated successfully${NC}"
        echo -e "   Location: rust/target/doc/haze_library/index.html"
    else
        echo -e "${RED}❌ Failed to generate Rust documentation${NC}"
        exit 1
    fi

    cd "$PROJECT_ROOT"
}

# Function to check documentation coverage
check_doc_coverage() {
    echo -e "\n${BLUE}📊 Checking Documentation Coverage...${NC}"
    cd "$PROJECT_ROOT/rust"

    # Check for missing documentation
    echo "Checking for missing documentation warnings..."
    cargo rustdoc --features "python streaming" -- -W missing_docs 2>&1 | tee /tmp/doc_warnings.log || true

    # Count warnings
    MISSING_COUNT=$(grep -c "warning: missing documentation" /tmp/doc_warnings.log || echo "0")

    if [ "$MISSING_COUNT" -eq 0 ]; then
        echo -e "${GREEN}✅ All public items are documented!${NC}"
    else
        echo -e "${RED}⚠️  Found $MISSING_COUNT missing documentation items${NC}"
        echo "   Run 'cargo rustdoc --all-features -- -W missing_docs' for details"
    fi

    cd "$PROJECT_ROOT"
}

# Function to open documentation in browser
open_docs() {
    echo -e "\n${BLUE}🌐 Opening Documentation in Browser...${NC}"

    DOC_PATH="$PROJECT_ROOT/rust/target/doc/haze_library/index.html"

    if [ ! -f "$DOC_PATH" ]; then
        echo -e "${RED}❌ Documentation not found. Please run generation first.${NC}"
        return 1
    fi

    # Detect OS and open browser
    case "$(uname -s)" in
        Darwin*)
            open "$DOC_PATH"
            ;;
        Linux*)
            if command -v xdg-open &> /dev/null; then
                xdg-open "$DOC_PATH"
            elif command -v firefox &> /dev/null; then
                firefox "$DOC_PATH" &
            elif command -v google-chrome &> /dev/null; then
                google-chrome "$DOC_PATH" &
            else
                echo -e "${RED}❌ Could not detect browser${NC}"
                echo "   Please open: $DOC_PATH"
            fi
            ;;
        MINGW*|MSYS*|CYGWIN*)
            start "$DOC_PATH"
            ;;
        *)
            echo -e "${RED}❌ Unknown operating system${NC}"
            echo "   Please open: $DOC_PATH"
            ;;
    esac
}

# Function to generate Python documentation (if Sphinx is available)
generate_python_docs() {
    echo -e "\n${BLUE}📚 Generating Python Documentation...${NC}"

    if [ -d "$PROJECT_ROOT/docs" ] && [ -f "$PROJECT_ROOT/docs/Makefile" ]; then
        cd "$PROJECT_ROOT/docs"

        if command -v sphinx-build &> /dev/null; then
            make html
            echo -e "${GREEN}✅ Python documentation generated successfully${NC}"
            echo -e "   Location: docs/_build/html/index.html"
        else
            echo -e "${RED}⚠️  Sphinx not found. Skipping Python documentation.${NC}"
            echo "   Install with: pip install sphinx sphinx-rtd-theme"
        fi

        cd "$PROJECT_ROOT"
    else
        echo -e "${RED}⚠️  No Sphinx documentation found. Skipping Python docs.${NC}"
    fi
}

# Main execution
main() {
    # Parse command line arguments
    OPEN_BROWSER=false
    SKIP_PYTHON=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --open|-o)
                OPEN_BROWSER=true
                shift
                ;;
            --no-python)
                SKIP_PYTHON=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --open, -o       Open documentation in browser after generation"
                echo "  --no-python      Skip Python documentation generation"
                echo "  --help, -h       Show this help message"
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done

    # Generate Rust documentation
    generate_rust_docs

    # Check documentation coverage
    check_doc_coverage

    # Generate Python documentation (unless skipped)
    if [ "$SKIP_PYTHON" = false ]; then
        generate_python_docs
    fi

    # Open in browser if requested
    if [ "$OPEN_BROWSER" = true ]; then
        open_docs
    fi

    echo -e "\n${GREEN}✅ Documentation generation complete!${NC}"
    echo ""
    echo "View Rust docs:"
    echo "  file://$PROJECT_ROOT/rust/target/doc/haze_library/index.html"
    if [ -f "$PROJECT_ROOT/docs/_build/html/index.html" ]; then
        echo ""
        echo "View Python docs:"
        echo "  file://$PROJECT_ROOT/docs/_build/html/index.html"
    fi
}

# Run main function
main "$@"

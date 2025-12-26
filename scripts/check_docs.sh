#!/bin/bash
# Documentation quality check script for Haze-Library
# This script performs comprehensive documentation quality checks

set -e  # Exit on error

echo "🔍 Haze-Library Documentation Quality Checker"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Exit codes
EXIT_CODE=0

# Check if rust directory exists
if [ ! -d "rust" ]; then
    echo -e "${RED}❌ Error: rust directory not found${NC}"
    exit 1
fi

# Function to check for missing documentation
check_missing_docs() {
    echo -e "\n${BLUE}📝 Checking for Missing Documentation...${NC}"
    cd "$PROJECT_ROOT/rust"

    # Run rustdoc with missing_docs warning (using available features only)
    cargo rustdoc --features "python streaming" -- -W missing_docs 2>&1 | tee /tmp/missing_docs.log || true

    # Count missing documentation warnings
    MISSING_COUNT=$(grep -c "warning: missing documentation" /tmp/missing_docs.log || echo "0")

    if [ "$MISSING_COUNT" -eq 0 ]; then
        echo -e "${GREEN}✅ All public items are documented${NC}"
    else
        echo -e "${YELLOW}⚠️  Found $MISSING_COUNT items missing documentation${NC}"
        echo ""
        echo "Missing documentation summary:"
        grep "warning: missing documentation" /tmp/missing_docs.log | head -20

        if [ "$MISSING_COUNT" -gt 20 ]; then
            echo ""
            echo "... and $((MISSING_COUNT - 20)) more items"
        fi

        EXIT_CODE=1
    fi

    cd "$PROJECT_ROOT"
}

# Function to check for broken documentation links
check_broken_links() {
    echo -e "\n${BLUE}🔗 Checking for Broken Documentation Links...${NC}"
    cd "$PROJECT_ROOT/rust"

    # Check if cargo-deadlinks is installed
    if ! command -v cargo-deadlinks &> /dev/null; then
        echo -e "${YELLOW}⚠️  cargo-deadlinks not installed${NC}"
        echo "   Install with: cargo install cargo-deadlinks"
        cd "$PROJECT_ROOT"
        return 1
    fi

    # Build documentation first (required for deadlinks)
    echo "Building documentation for link checking..."
    cargo doc --no-deps --features "python streaming" --quiet

    # Check for broken links
    echo "Checking for broken links..."
    if cargo deadlinks --check-http --dir target/doc 2>&1 | tee /tmp/deadlinks.log; then
        echo -e "${GREEN}✅ No broken links found${NC}"
    else
        echo -e "${RED}❌ Found broken links in documentation${NC}"
        cat /tmp/deadlinks.log
        EXIT_CODE=1
    fi

    cd "$PROJECT_ROOT"
}

# Function to generate documentation coverage report
generate_coverage_report() {
    echo -e "\n${BLUE}📊 Generating Documentation Coverage Report...${NC}"
    cd "$PROJECT_ROOT/rust"

    REPORT_FILE="$PROJECT_ROOT/doc-coverage-report.md"

    # Create report header
    cat > "$REPORT_FILE" << EOF
# Documentation Coverage Report

**Generated:** $(date '+%Y-%m-%d %H:%M:%S')

## Summary

EOF

    # Get total public items count
    echo "Analyzing public items..."
    cargo rustdoc --all-features -- --document-private-items 2>&1 > /tmp/all_items.log || true

    # Get missing documentation count
    cargo rustdoc --features "python streaming" -- -W missing_docs 2>&1 | tee /tmp/missing_docs_full.log || true
    MISSING_COUNT=$(grep -c "warning: missing documentation" /tmp/missing_docs_full.log || echo "0")

    # Calculate coverage percentage (approximate)
    PUBLIC_ITEMS=$(grep -E "(pub fn|pub struct|pub enum|pub trait)" rust/src -r | wc -l | tr -d ' ')
    if [ "$PUBLIC_ITEMS" -gt 0 ]; then
        DOCUMENTED=$((PUBLIC_ITEMS - MISSING_COUNT))
        COVERAGE=$((DOCUMENTED * 100 / PUBLIC_ITEMS))
    else
        COVERAGE=100
    fi

    # Add summary to report
    cat >> "$REPORT_FILE" << EOF
- **Total Public Items:** $PUBLIC_ITEMS (approximate)
- **Documented Items:** $((PUBLIC_ITEMS - MISSING_COUNT))
- **Missing Documentation:** $MISSING_COUNT
- **Coverage:** ~$COVERAGE%

EOF

    # Add status badge
    if [ "$COVERAGE" -ge 80 ]; then
        echo "**Status:** ✅ Good" >> "$REPORT_FILE"
    elif [ "$COVERAGE" -ge 60 ]; then
        echo "**Status:** ⚠️ Needs Improvement" >> "$REPORT_FILE"
    else
        echo "**Status:** ❌ Poor" >> "$REPORT_FILE"
    fi

    # Add missing items section
    if [ "$MISSING_COUNT" -gt 0 ]; then
        cat >> "$REPORT_FILE" << EOF

## Missing Documentation

\`\`\`
EOF
        grep "warning: missing documentation" /tmp/missing_docs_full.log >> "$REPORT_FILE" || true
        echo '```' >> "$REPORT_FILE"
    fi

    # Add recommendations
    cat >> "$REPORT_FILE" << EOF

## Recommendations

EOF

    if [ "$MISSING_COUNT" -gt 0 ]; then
        cat >> "$REPORT_FILE" << EOF
- Add documentation to $MISSING_COUNT public items
- Focus on public API functions and structures first
- Include examples in documentation where appropriate
- Add \`# Safety\` sections for unsafe code
- Document all parameters and return values
EOF
    else
        cat >> "$REPORT_FILE" << EOF
- ✅ All public items are documented!
- Consider adding more examples to existing documentation
- Keep documentation up-to-date with code changes
EOF
    fi

    echo -e "${GREEN}✅ Coverage report generated${NC}"
    echo -e "   Location: $REPORT_FILE"
    echo ""
    echo "Coverage: ~$COVERAGE% ($((PUBLIC_ITEMS - MISSING_COUNT))/$PUBLIC_ITEMS items documented)"

    cd "$PROJECT_ROOT"
}

# Function to check documentation formatting
check_doc_formatting() {
    echo -e "\n${BLUE}📐 Checking Documentation Formatting...${NC}"
    cd "$PROJECT_ROOT/rust"

    # Check for common documentation issues
    echo "Checking for common documentation issues..."

    ISSUES_FOUND=false

    # Check for missing parameter documentation
    echo "  - Checking parameter documentation..."
    if grep -r "pub fn" src/ --include="*.rs" | grep -v "///" | head -5 | grep -q "pub fn"; then
        echo -e "    ${YELLOW}⚠️  Some functions may be missing parameter documentation${NC}"
        ISSUES_FOUND=true
    fi

    # Check for very short documentation
    echo "  - Checking documentation completeness..."
    SHORT_DOCS=$(grep -r "///" src/ --include="*.rs" -A 0 | awk '{print length}' | awk '$1 < 20 {count++} END {print count+0}')
    if [ "$SHORT_DOCS" -gt 0 ]; then
        echo -e "    ${YELLOW}⚠️  Found $SHORT_DOCS very short documentation comments${NC}"
        echo "       Consider adding more detailed descriptions"
    fi

    if [ "$ISSUES_FOUND" = false ]; then
        echo -e "${GREEN}✅ Documentation formatting looks good${NC}"
    fi

    cd "$PROJECT_ROOT"
}

# Function to check for examples in documentation
check_doc_examples() {
    echo -e "\n${BLUE}💡 Checking for Documentation Examples...${NC}"
    cd "$PROJECT_ROOT/rust"

    # Count functions with examples
    TOTAL_FUNCS=$(grep -r "pub fn" src/ --include="*.rs" | wc -l | tr -d ' ')
    FUNCS_WITH_EXAMPLES=$(grep -r "# Example" src/ --include="*.rs" -B 5 | grep "pub fn" | wc -l | tr -d ' ')

    if [ "$TOTAL_FUNCS" -gt 0 ]; then
        EXAMPLE_COVERAGE=$((FUNCS_WITH_EXAMPLES * 100 / TOTAL_FUNCS))
        echo "Functions with examples: $FUNCS_WITH_EXAMPLES / $TOTAL_FUNCS (~$EXAMPLE_COVERAGE%)"

        if [ "$EXAMPLE_COVERAGE" -ge 50 ]; then
            echo -e "${GREEN}✅ Good example coverage${NC}"
        elif [ "$EXAMPLE_COVERAGE" -ge 25 ]; then
            echo -e "${YELLOW}⚠️  Consider adding more examples${NC}"
        else
            echo -e "${YELLOW}⚠️  Low example coverage - add more examples to help users${NC}"
        fi
    fi

    cd "$PROJECT_ROOT"
}

# Main execution
main() {
    # Parse command line arguments
    GENERATE_REPORT=true
    SKIP_LINKS=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-report)
                GENERATE_REPORT=false
                shift
                ;;
            --skip-links)
                SKIP_LINKS=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --no-report      Skip generating coverage report"
                echo "  --skip-links     Skip checking for broken links"
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

    # Run all checks
    check_missing_docs
    check_doc_formatting
    check_doc_examples

    if [ "$SKIP_LINKS" = false ]; then
        check_broken_links || true
    fi

    if [ "$GENERATE_REPORT" = true ]; then
        generate_coverage_report
    fi

    # Final summary
    echo ""
    echo -e "${BLUE}========================================${NC}"
    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ All documentation checks passed!${NC}"
    else
        echo -e "${YELLOW}⚠️  Some issues found - please review above${NC}"
    fi
    echo -e "${BLUE}========================================${NC}"

    exit $EXIT_CODE
}

# Run main function
main "$@"

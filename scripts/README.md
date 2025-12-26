# Documentation Scripts

This directory contains scripts for managing Rust documentation for the Haze library.

## Available Scripts

### 1. `generate_docs.sh` - Documentation Generator

Generates Rust API documentation and optionally Python Sphinx documentation.

**Usage:**
```bash
# Generate Rust docs only
./scripts/generate_docs.sh

# Generate and open in browser
./scripts/generate_docs.sh --open

# Skip Python documentation
./scripts/generate_docs.sh --no-python

# Help
./scripts/generate_docs.sh --help
```

**Features:**
- Builds Rust documentation with all available features
- Checks documentation coverage
- Optionally generates Python Sphinx documentation
- Opens documentation in default browser

**Output:**
- Rust docs: `rust/target/doc/haze_library/index.html`
- Python docs: `docs/_build/html/index.html` (if available)

---

### 2. `check_docs.sh` - Documentation Quality Checker

Performs comprehensive documentation quality checks.

**Usage:**
```bash
# Run all checks
./scripts/check_docs.sh

# Skip broken link checking
./scripts/check_docs.sh --skip-links

# Skip coverage report generation
./scripts/check_docs.sh --no-report

# Help
./scripts/check_docs.sh --help
```

**Checks Performed:**
1. **Missing Documentation**: Identifies undocumented public items
2. **Documentation Formatting**: Checks for common formatting issues
3. **Example Coverage**: Measures percentage of functions with examples
4. **Broken Links**: Validates internal and external links (requires cargo-deadlinks)
5. **Coverage Report**: Generates detailed coverage statistics

**Output:**
- Coverage report: `doc-coverage-report.md`
- Console output with color-coded status

**Exit Codes:**
- `0`: All checks passed
- `1`: Some issues found (review required)

---

## CI/CD Integration

Documentation is automatically built and checked on:
- Push to `main` branch
- Pull requests to `main` branch

### GitHub Actions Workflow

The `.github/workflows/docs.yml` workflow:

1. **Build Docs Job**: Builds documentation and checks for issues
   - Validates documentation compiles without warnings
   - Checks for broken links
   - Generates coverage report
   - Uploads artifacts

2. **Deploy Docs Job**: Deploys to GitHub Pages (main branch only)
   - Builds optimized documentation
   - Deploys to `gh-pages` branch
   - Available at: `https://kwannz.github.io/haze/`

3. **Coverage Check Job**: Validates documentation coverage
   - Comments on PRs with coverage status
   - Warns if coverage is too low

---

## Documentation Standards

All contributions must meet these documentation requirements:

### Required Documentation

1. **Module-level docs**: Overview of module purpose
2. **Public functions**: Full documentation including:
   - Description of what the function does
   - `# Parameters` section
   - `# Returns` section
   - `# Example` section (with working code)
   - `# Panics` section (if applicable)
   - `# Safety` section (for unsafe code)

3. **Structs and Enums**: Document the type and all public fields
4. **Type aliases**: Explain purpose and when to use

### Example Format

```rust
/// Calculates the Simple Moving Average (SMA) over a specified period.
///
/// The SMA is calculated as the arithmetic mean of the previous `period` values.
/// Returns NaN for the initial `period - 1` values where insufficient data exists.
///
/// # Parameters
/// - `values`: Slice of input price data
/// - `period`: Number of periods for the moving average (must be > 0)
///
/// # Returns
/// Vector of SMA values with the same length as `values`. The first `period - 1`
/// values will be NaN.
///
/// # Example
/// ```
/// use haze_library::indicators::trend::simple_moving_average;
///
/// let prices = vec![10.0, 11.0, 12.0, 13.0, 14.0];
/// let sma = simple_moving_average(&prices, 3).unwrap();
///
/// assert!(sma[0].is_nan());  // Insufficient data
/// assert!(sma[1].is_nan());  // Insufficient data
/// assert!((sma[2] - 11.0).abs() < 1e-10);  // (10+11+12)/3
/// ```
///
/// # Panics
/// This function returns an error instead of panicking.
///
/// # Errors
/// Returns `HazeError::InvalidPeriod` if period is 0.
/// Returns `HazeError::EmptyInput` if values slice is empty.
pub fn simple_moving_average(values: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    // Implementation...
}
```

---

## Troubleshooting

### Issue: `cargo-deadlinks not found`

**Solution:**
```bash
cargo install cargo-deadlinks
```

Or run with `--skip-links`:
```bash
./scripts/check_docs.sh --skip-links
```

### Issue: Documentation build fails with feature errors

The scripts use `--features "python streaming"` to avoid disabled polars dependencies.

If you enable polars in `Cargo.toml`, update the scripts to include it:
```bash
cargo doc --features "python streaming polars"
```

### Issue: Coverage report shows 0% or negative values

This happens when the public item count script fails. The script counts items using:
```bash
grep -E "(pub fn|pub struct|pub enum|pub trait)" rust/src -r
```

Ensure you're running from the project root directory.

---

## Tips

### Quick Documentation Check Before PR

```bash
# 1. Generate and view docs
./scripts/generate_docs.sh --open

# 2. Run quality checks
./scripts/check_docs.sh

# 3. Review coverage report
cat doc-coverage-report.md
```

### Adding Documentation to Existing Code

1. Identify missing items:
   ```bash
   ./scripts/check_docs.sh 2>&1 | grep "missing documentation"
   ```

2. Add documentation following the example format above

3. Verify:
   ```bash
   ./scripts/check_docs.sh
   ```

### Testing Documentation Examples

Rust documentation examples are tested automatically with:
```bash
cargo test --doc
```

Ensure all examples in `# Example` sections compile and run successfully.

---

## Integration with CONTRIBUTING.md

Before submitting a PR, contributors should:

1. ✅ Run `./scripts/check_docs.sh`
2. ✅ Ensure no decrease in documentation coverage
3. ✅ Add examples to all new public functions
4. ✅ Update CHANGELOG.md if adding new public APIs

See `CONTRIBUTING.md` for complete PR guidelines.

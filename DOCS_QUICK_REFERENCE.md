# Documentation Quick Reference

## 🚀 Quick Commands

```bash
# Generate and view docs
./scripts/generate_docs.sh --open

# Check documentation quality
./scripts/check_docs.sh

# View coverage report
cat doc-coverage-report.md

# Build docs for specific features
cd rust && cargo doc --features "python streaming"

# Test documentation examples
cd rust && cargo test --doc
```

## 📋 Pre-PR Checklist

```bash
# Run before submitting any PR
./scripts/check_docs.sh                    # Must pass
./scripts/generate_docs.sh --open          # Verify appearance
cat doc-coverage-report.md                 # Check coverage
cd rust && cargo fmt && cargo clippy       # Format & lint
pytest tests/ -v                           # Run tests
```

## 📝 Documentation Template

```rust
/// Brief one-line description.
///
/// Longer explanation of what this does and how it works.
///
/// # Parameters
/// - `values`: Input price data
/// - `period`: Lookback period
///
/// # Returns
/// `Ok(Vec<f64>)` with indicator values (NaN for warmup period)
///
/// # Errors
/// - `HazeError::EmptyInput`: If values is empty
/// - `HazeError::InvalidPeriod`: If period is invalid
///
/// # Example
/// ```
/// use haze_library::indicators::your_indicator;
/// let prices = vec![10.0, 11.0, 12.0, 13.0, 14.0];
/// let result = your_indicator(&prices, 3).unwrap();
/// assert!(result[0].is_nan());  // Warmup period
/// ```
pub fn your_indicator(values: &[f64], period: usize) -> HazeResult<Vec<f64>> {
    // Implementation
}
```

## 🔍 Common Issues

### Missing documentation
```bash
# Find all missing items
./scripts/check_docs.sh 2>&1 | grep "missing documentation"
```

### Broken links
```bash
# Install cargo-deadlinks first
cargo install cargo-deadlinks

# Then check
./scripts/check_docs.sh
```

### HTML formatting warnings
```bash
# Wrap types in backticks
Vec<f64>  # ❌ Wrong
`Vec<f64>`  # ✅ Correct
```

## 📊 Coverage Goals

- **Minimum**: All public items documented
- **Target**: 100% coverage
- **Required**: Examples for complex functions
- **Quality**: Clear, accurate, helpful

## 🔗 Resources

- **Full Setup Guide**: `DOCUMENTATION_SETUP_SUMMARY.md`
- **Scripts Guide**: `scripts/README.md`
- **Contributing**: `CONTRIBUTING.md`
- **Error Handling**: `docs/ERROR_HANDLING_STRATEGY.md`

## 🎯 CI/CD Status

- ✅ Auto-build on PR
- ✅ Coverage check on PR
- ✅ Auto-deploy to GitHub Pages (main)
- ✅ PR comments with coverage status

## 📍 File Locations

```
.github/workflows/docs.yml          # CI/CD workflow
scripts/generate_docs.sh            # Local doc generator
scripts/check_docs.sh               # Quality checker
rust/Cargo.toml                     # Docs.rs config
doc-coverage-report.md              # Generated report (git-ignored)
rust/target/doc/haze_library/       # Generated docs
```

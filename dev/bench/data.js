window.BENCHMARK_DATA = {
  "lastUpdate": 1767410574904,
  "repoUrl": "https://github.com/kwannz/haze",
  "entries": {
    "Rust Numerical Precision Benchmarks": [
      {
        "commit": {
          "author": {
            "email": "your-email@example.com",
            "name": "Jacksonchiunz"
          },
          "committer": {
            "email": "your-email@example.com",
            "name": "Jacksonchiunz"
          },
          "distinct": true,
          "id": "79f24d9570a4bc1c5294fdef405241ffd6fcf3a8",
          "message": "Merge release/v1.1.3 - License change to Proprietary\n\n- Version updated from 1.1.2 to 1.1.3\n- All version numbers synchronized (Cargo.toml 1.1.1→1.1.3)\n- License changed from CC BY-NC 4.0 to Proprietary\n- Added test-release.yml workflow for TestPyPI validation\n- Updated CHANGELOG.md with v1.1.3 entry",
          "timestamp": "2025-12-30T13:22:01+08:00",
          "tree_id": "08b8b217e5476c03fcd33f19e01913ec06c5a921",
          "url": "https://github.com/kwannz/haze/commit/79f24d9570a4bc1c5294fdef405241ffd6fcf3a8"
        },
        "date": 1767072507263,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40775,
            "range": "± 138",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447380,
            "range": "± 13906",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4519183,
            "range": "± 8107",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20311,
            "range": "± 60",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203838,
            "range": "± 570",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2048593,
            "range": "± 13173",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156931,
            "range": "± 450",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20269,
            "range": "± 35",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447444,
            "range": "± 686",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20275,
            "range": "± 140",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156924,
            "range": "± 8075",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20423,
            "range": "± 118",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93515,
            "range": "± 123",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373714,
            "range": "± 399",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 253674,
            "range": "± 869",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 204084,
            "range": "± 550",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1579920,
            "range": "± 7645",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203707,
            "range": "± 882",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4523768,
            "range": "± 25733",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203787,
            "range": "± 606",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13103994,
            "range": "± 12981",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203748,
            "range": "± 655",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40883204,
            "range": "± 20890",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203257,
            "range": "± 485",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45347695,
            "range": "± 32996",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2043766,
            "range": "± 4795",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "your-email@example.com",
            "name": "Jacksonchiunz"
          },
          "committer": {
            "email": "your-email@example.com",
            "name": "Jacksonchiunz"
          },
          "distinct": true,
          "id": "56287755f22fabd9243d5549dfa3f3257b90076b",
          "message": "feat(ffi): migrate 30 single-input indicators to zero-copy (Phase 1)\n\n## Phase 1 Complete: Zero-Copy FFI Migration\nSuccessfully migrated 30 technical indicators from Vec<f64> to PyReadonlyArray1\nfor zero-copy data transfer between Python and Rust.\n\n### Performance Impact\n- Eliminated 4 data copies per function call (NumPy → List → Vec → List → NumPy)\n- Expected 2-3x speedup for large datasets (n > 10K)\n- Compilation time: 14.60s (within <20s target)\n\n### Migrated Functions (30)\n**Trend**: alma, dpo, vhf, trix, volume_oscillator\n**Momentum**: apo, ppo, cmo, cti, er, bias, psl, mom, roc, percent_rank\n**Volatility**: historical_volatility, ulcer_index\n**Advanced MA**: frama, t3, kama, sinwma, slope, swma\n**Composite**: stc, tdfi, coppock, entropy\n\n### Technical Achievements\n1. **Enhanced Code Generator** (`migrate_to_zero_copy.py`)\n   - Implemented brace-counting algorithm for robust function body extraction\n   - Auto-extracts Option parameter defaults from legacy functions\n   - Success rate: 50% auto + 50% manual fixup\n\n2. **Zero-Copy Infrastructure** (`rust/src/ffi/zero_copy.rs`)\n   - `to_pyarray_or_nan()`: Handles Option<Vec<f64>> → PyArray1\n   - Graceful NaN handling for computation errors\n   - Foundation for multi-output functions (Phase 2-4)\n\n3. **Safe Migration Strategy**\n   - Original functions renamed to `*_legacy` (backward compatible)\n   - Comprehensive backups in `rust/src/backups/`\n   - Integration script with dry-run mode\n\n### Validation\n- ✅ 0 compilation errors (3 harmless warnings)\n- ✅ 5/5 sample functions tested (correct NumPy output)\n- ✅ Type-safe: no runtime type coercion\n\n### Architecture Pattern\n```rust\n// Before (4 copies):\nfn py_alma(values: Vec<f64>, ...) -> Vec<f64>\n\n// After (zero-copy):\nfn py_alma<'py>(\n    py: Python<'py>,\n    values: PyReadonlyArray1<'py, f64>,  // Borrow Python data\n    ...\n) -> Py<PyArray1<f64>>  // Return NumPy view directly\n```\n\n### Migration Progress\n- Phase 1 (1→1): 30/32 ✅ (93.8%)\n  - Deferred: volume_filter, prepare_momentum_features (wrong pattern)\n- Phase 2 (n→1): 0/129 (next)\n- Phase 3 (1→n, n→m): 0/16\n- Total: 30/262 indicators (11.5%)\n\n### Breaking Changes\nNone - legacy functions remain available during transition period.\n\n### Files Changed\n- `rust/src/lib.rs`: +30 zero-copy functions\n- `scripts/migrate_to_zero_copy.py`: Code generator with default extraction\n- `scripts/auto_integrate_zero_copy.py`: Batch integration tool\n- `rust/src/ffi/zero_copy.rs`: Zero-copy helper functions\n- `tests/validation/test_zero_copy_migration.py`: Validation suite\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
          "timestamp": "2025-12-30T16:06:32+08:00",
          "tree_id": "af185cb7680dfc1018e6a8e7af2f36d503e3503c",
          "url": "https://github.com/kwannz/haze/commit/56287755f22fabd9243d5549dfa3f3257b90076b"
        },
        "date": 1767084411122,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 47936,
            "range": "± 123",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 525695,
            "range": "± 927",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 5312624,
            "range": "± 248722",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 24543,
            "range": "± 85",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 247524,
            "range": "± 1099",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2665932,
            "range": "± 34738",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 185998,
            "range": "± 282",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 24490,
            "range": "± 270",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 525780,
            "range": "± 1427",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 24432,
            "range": "± 46",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 185965,
            "range": "± 2232",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 24490,
            "range": "± 84",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 115106,
            "range": "± 1009",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 474582,
            "range": "± 1518",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 239894,
            "range": "± 2428",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 247362,
            "range": "± 151",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1875105,
            "range": "± 21597",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 247303,
            "range": "± 273",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 5347069,
            "range": "± 19815",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 247339,
            "range": "± 7799",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 14979674,
            "range": "± 11824",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 248158,
            "range": "± 293",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 49481439,
            "range": "± 33949",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 246927,
            "range": "± 2816",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 53543202,
            "range": "± 50982",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2612660,
            "range": "± 20880",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Jacksonchiunz",
            "username": "renoschubert",
            "email": "your-email@example.com"
          },
          "committer": {
            "name": "Jacksonchiunz",
            "username": "renoschubert",
            "email": "your-email@example.com"
          },
          "id": "56287755f22fabd9243d5549dfa3f3257b90076b",
          "message": "feat(ffi): migrate 30 single-input indicators to zero-copy (Phase 1)\n\n## Phase 1 Complete: Zero-Copy FFI Migration\nSuccessfully migrated 30 technical indicators from Vec<f64> to PyReadonlyArray1\nfor zero-copy data transfer between Python and Rust.\n\n### Performance Impact\n- Eliminated 4 data copies per function call (NumPy → List → Vec → List → NumPy)\n- Expected 2-3x speedup for large datasets (n > 10K)\n- Compilation time: 14.60s (within <20s target)\n\n### Migrated Functions (30)\n**Trend**: alma, dpo, vhf, trix, volume_oscillator\n**Momentum**: apo, ppo, cmo, cti, er, bias, psl, mom, roc, percent_rank\n**Volatility**: historical_volatility, ulcer_index\n**Advanced MA**: frama, t3, kama, sinwma, slope, swma\n**Composite**: stc, tdfi, coppock, entropy\n\n### Technical Achievements\n1. **Enhanced Code Generator** (`migrate_to_zero_copy.py`)\n   - Implemented brace-counting algorithm for robust function body extraction\n   - Auto-extracts Option parameter defaults from legacy functions\n   - Success rate: 50% auto + 50% manual fixup\n\n2. **Zero-Copy Infrastructure** (`rust/src/ffi/zero_copy.rs`)\n   - `to_pyarray_or_nan()`: Handles Option<Vec<f64>> → PyArray1\n   - Graceful NaN handling for computation errors\n   - Foundation for multi-output functions (Phase 2-4)\n\n3. **Safe Migration Strategy**\n   - Original functions renamed to `*_legacy` (backward compatible)\n   - Comprehensive backups in `rust/src/backups/`\n   - Integration script with dry-run mode\n\n### Validation\n- ✅ 0 compilation errors (3 harmless warnings)\n- ✅ 5/5 sample functions tested (correct NumPy output)\n- ✅ Type-safe: no runtime type coercion\n\n### Architecture Pattern\n```rust\n// Before (4 copies):\nfn py_alma(values: Vec<f64>, ...) -> Vec<f64>\n\n// After (zero-copy):\nfn py_alma<'py>(\n    py: Python<'py>,\n    values: PyReadonlyArray1<'py, f64>,  // Borrow Python data\n    ...\n) -> Py<PyArray1<f64>>  // Return NumPy view directly\n```\n\n### Migration Progress\n- Phase 1 (1→1): 30/32 ✅ (93.8%)\n  - Deferred: volume_filter, prepare_momentum_features (wrong pattern)\n- Phase 2 (n→1): 0/129 (next)\n- Phase 3 (1→n, n→m): 0/16\n- Total: 30/262 indicators (11.5%)\n\n### Breaking Changes\nNone - legacy functions remain available during transition period.\n\n### Files Changed\n- `rust/src/lib.rs`: +30 zero-copy functions\n- `scripts/migrate_to_zero_copy.py`: Code generator with default extraction\n- `scripts/auto_integrate_zero_copy.py`: Batch integration tool\n- `rust/src/ffi/zero_copy.rs`: Zero-copy helper functions\n- `tests/validation/test_zero_copy_migration.py`: Validation suite\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
          "timestamp": "2025-12-30T08:06:32Z",
          "url": "https://github.com/kwannz/haze/commit/56287755f22fabd9243d5549dfa3f3257b90076b"
        },
        "date": 1767151650854,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40775,
            "range": "± 54",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 448164,
            "range": "± 1043",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4525587,
            "range": "± 78775",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20248,
            "range": "± 30",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 205099,
            "range": "± 431",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2062224,
            "range": "± 5126",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156884,
            "range": "± 312",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20237,
            "range": "± 193",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447838,
            "range": "± 483",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20178,
            "range": "± 30",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156829,
            "range": "± 315",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20219,
            "range": "± 71",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93760,
            "range": "± 155",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373497,
            "range": "± 983",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 250334,
            "range": "± 5827",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 204167,
            "range": "± 331",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1579100,
            "range": "± 11413",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 204083,
            "range": "± 854",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4542399,
            "range": "± 39994",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 204592,
            "range": "± 595",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13097707,
            "range": "± 19564",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 204047,
            "range": "± 1423",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40894629,
            "range": "± 24084",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203499,
            "range": "± 453",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45284151,
            "range": "± 19741",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2036833,
            "range": "± 2795",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Jacksonchiunz",
            "username": "renoschubert",
            "email": "your-email@example.com"
          },
          "committer": {
            "name": "Jacksonchiunz",
            "username": "renoschubert",
            "email": "your-email@example.com"
          },
          "id": "56287755f22fabd9243d5549dfa3f3257b90076b",
          "message": "feat(ffi): migrate 30 single-input indicators to zero-copy (Phase 1)\n\n## Phase 1 Complete: Zero-Copy FFI Migration\nSuccessfully migrated 30 technical indicators from Vec<f64> to PyReadonlyArray1\nfor zero-copy data transfer between Python and Rust.\n\n### Performance Impact\n- Eliminated 4 data copies per function call (NumPy → List → Vec → List → NumPy)\n- Expected 2-3x speedup for large datasets (n > 10K)\n- Compilation time: 14.60s (within <20s target)\n\n### Migrated Functions (30)\n**Trend**: alma, dpo, vhf, trix, volume_oscillator\n**Momentum**: apo, ppo, cmo, cti, er, bias, psl, mom, roc, percent_rank\n**Volatility**: historical_volatility, ulcer_index\n**Advanced MA**: frama, t3, kama, sinwma, slope, swma\n**Composite**: stc, tdfi, coppock, entropy\n\n### Technical Achievements\n1. **Enhanced Code Generator** (`migrate_to_zero_copy.py`)\n   - Implemented brace-counting algorithm for robust function body extraction\n   - Auto-extracts Option parameter defaults from legacy functions\n   - Success rate: 50% auto + 50% manual fixup\n\n2. **Zero-Copy Infrastructure** (`rust/src/ffi/zero_copy.rs`)\n   - `to_pyarray_or_nan()`: Handles Option<Vec<f64>> → PyArray1\n   - Graceful NaN handling for computation errors\n   - Foundation for multi-output functions (Phase 2-4)\n\n3. **Safe Migration Strategy**\n   - Original functions renamed to `*_legacy` (backward compatible)\n   - Comprehensive backups in `rust/src/backups/`\n   - Integration script with dry-run mode\n\n### Validation\n- ✅ 0 compilation errors (3 harmless warnings)\n- ✅ 5/5 sample functions tested (correct NumPy output)\n- ✅ Type-safe: no runtime type coercion\n\n### Architecture Pattern\n```rust\n// Before (4 copies):\nfn py_alma(values: Vec<f64>, ...) -> Vec<f64>\n\n// After (zero-copy):\nfn py_alma<'py>(\n    py: Python<'py>,\n    values: PyReadonlyArray1<'py, f64>,  // Borrow Python data\n    ...\n) -> Py<PyArray1<f64>>  // Return NumPy view directly\n```\n\n### Migration Progress\n- Phase 1 (1→1): 30/32 ✅ (93.8%)\n  - Deferred: volume_filter, prepare_momentum_features (wrong pattern)\n- Phase 2 (n→1): 0/129 (next)\n- Phase 3 (1→n, n→m): 0/16\n- Total: 30/262 indicators (11.5%)\n\n### Breaking Changes\nNone - legacy functions remain available during transition period.\n\n### Files Changed\n- `rust/src/lib.rs`: +30 zero-copy functions\n- `scripts/migrate_to_zero_copy.py`: Code generator with default extraction\n- `scripts/auto_integrate_zero_copy.py`: Batch integration tool\n- `rust/src/ffi/zero_copy.rs`: Zero-copy helper functions\n- `tests/validation/test_zero_copy_migration.py`: Validation suite\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
          "timestamp": "2025-12-30T08:06:32Z",
          "url": "https://github.com/kwannz/haze/commit/56287755f22fabd9243d5549dfa3f3257b90076b"
        },
        "date": 1767239436863,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40823,
            "range": "± 666",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447866,
            "range": "± 946",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4522680,
            "range": "± 18824",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20456,
            "range": "± 73",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 204311,
            "range": "± 753",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2049640,
            "range": "± 23346",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156860,
            "range": "± 1110",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20391,
            "range": "± 60",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447799,
            "range": "± 408",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20369,
            "range": "± 171",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156856,
            "range": "± 1756",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20393,
            "range": "± 66",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93543,
            "range": "± 94",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373684,
            "range": "± 254",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252661,
            "range": "± 755",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 204287,
            "range": "± 533",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1581441,
            "range": "± 12023",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 204432,
            "range": "± 600",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4524818,
            "range": "± 62014",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 204554,
            "range": "± 1119",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13105437,
            "range": "± 6900",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 204593,
            "range": "± 5355",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40891387,
            "range": "± 12598",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203816,
            "range": "± 615",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45368334,
            "range": "± 636899",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2054459,
            "range": "± 7620",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Jacksonchiunz",
            "username": "renoschubert",
            "email": "your-email@example.com"
          },
          "committer": {
            "name": "Jacksonchiunz",
            "username": "renoschubert",
            "email": "your-email@example.com"
          },
          "id": "56287755f22fabd9243d5549dfa3f3257b90076b",
          "message": "feat(ffi): migrate 30 single-input indicators to zero-copy (Phase 1)\n\n## Phase 1 Complete: Zero-Copy FFI Migration\nSuccessfully migrated 30 technical indicators from Vec<f64> to PyReadonlyArray1\nfor zero-copy data transfer between Python and Rust.\n\n### Performance Impact\n- Eliminated 4 data copies per function call (NumPy → List → Vec → List → NumPy)\n- Expected 2-3x speedup for large datasets (n > 10K)\n- Compilation time: 14.60s (within <20s target)\n\n### Migrated Functions (30)\n**Trend**: alma, dpo, vhf, trix, volume_oscillator\n**Momentum**: apo, ppo, cmo, cti, er, bias, psl, mom, roc, percent_rank\n**Volatility**: historical_volatility, ulcer_index\n**Advanced MA**: frama, t3, kama, sinwma, slope, swma\n**Composite**: stc, tdfi, coppock, entropy\n\n### Technical Achievements\n1. **Enhanced Code Generator** (`migrate_to_zero_copy.py`)\n   - Implemented brace-counting algorithm for robust function body extraction\n   - Auto-extracts Option parameter defaults from legacy functions\n   - Success rate: 50% auto + 50% manual fixup\n\n2. **Zero-Copy Infrastructure** (`rust/src/ffi/zero_copy.rs`)\n   - `to_pyarray_or_nan()`: Handles Option<Vec<f64>> → PyArray1\n   - Graceful NaN handling for computation errors\n   - Foundation for multi-output functions (Phase 2-4)\n\n3. **Safe Migration Strategy**\n   - Original functions renamed to `*_legacy` (backward compatible)\n   - Comprehensive backups in `rust/src/backups/`\n   - Integration script with dry-run mode\n\n### Validation\n- ✅ 0 compilation errors (3 harmless warnings)\n- ✅ 5/5 sample functions tested (correct NumPy output)\n- ✅ Type-safe: no runtime type coercion\n\n### Architecture Pattern\n```rust\n// Before (4 copies):\nfn py_alma(values: Vec<f64>, ...) -> Vec<f64>\n\n// After (zero-copy):\nfn py_alma<'py>(\n    py: Python<'py>,\n    values: PyReadonlyArray1<'py, f64>,  // Borrow Python data\n    ...\n) -> Py<PyArray1<f64>>  // Return NumPy view directly\n```\n\n### Migration Progress\n- Phase 1 (1→1): 30/32 ✅ (93.8%)\n  - Deferred: volume_filter, prepare_momentum_features (wrong pattern)\n- Phase 2 (n→1): 0/129 (next)\n- Phase 3 (1→n, n→m): 0/16\n- Total: 30/262 indicators (11.5%)\n\n### Breaking Changes\nNone - legacy functions remain available during transition period.\n\n### Files Changed\n- `rust/src/lib.rs`: +30 zero-copy functions\n- `scripts/migrate_to_zero_copy.py`: Code generator with default extraction\n- `scripts/auto_integrate_zero_copy.py`: Batch integration tool\n- `rust/src/ffi/zero_copy.rs`: Zero-copy helper functions\n- `tests/validation/test_zero_copy_migration.py`: Validation suite\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
          "timestamp": "2025-12-30T08:06:32Z",
          "url": "https://github.com/kwannz/haze/commit/56287755f22fabd9243d5549dfa3f3257b90076b"
        },
        "date": 1767324659831,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40785,
            "range": "± 109",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447496,
            "range": "± 1009",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4518395,
            "range": "± 24757",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20268,
            "range": "± 37",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203463,
            "range": "± 553",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2036174,
            "range": "± 6088",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 157131,
            "range": "± 289",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20242,
            "range": "± 53",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447325,
            "range": "± 371",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20202,
            "range": "± 33",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 157057,
            "range": "± 1244",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20244,
            "range": "± 38",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93575,
            "range": "± 1232",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373525,
            "range": "± 330",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 253229,
            "range": "± 1106",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203353,
            "range": "± 831",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1579042,
            "range": "± 10093",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203591,
            "range": "± 730",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4518105,
            "range": "± 21807",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203343,
            "range": "± 577",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13100773,
            "range": "± 31979",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203857,
            "range": "± 1111",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40885246,
            "range": "± 32627",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 202833,
            "range": "± 445",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45336781,
            "range": "± 26991",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2037023,
            "range": "± 5486",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Jacksonchiunz",
            "username": "renoschubert",
            "email": "your-email@example.com"
          },
          "committer": {
            "name": "Jacksonchiunz",
            "username": "renoschubert",
            "email": "your-email@example.com"
          },
          "id": "56287755f22fabd9243d5549dfa3f3257b90076b",
          "message": "feat(ffi): migrate 30 single-input indicators to zero-copy (Phase 1)\n\n## Phase 1 Complete: Zero-Copy FFI Migration\nSuccessfully migrated 30 technical indicators from Vec<f64> to PyReadonlyArray1\nfor zero-copy data transfer between Python and Rust.\n\n### Performance Impact\n- Eliminated 4 data copies per function call (NumPy → List → Vec → List → NumPy)\n- Expected 2-3x speedup for large datasets (n > 10K)\n- Compilation time: 14.60s (within <20s target)\n\n### Migrated Functions (30)\n**Trend**: alma, dpo, vhf, trix, volume_oscillator\n**Momentum**: apo, ppo, cmo, cti, er, bias, psl, mom, roc, percent_rank\n**Volatility**: historical_volatility, ulcer_index\n**Advanced MA**: frama, t3, kama, sinwma, slope, swma\n**Composite**: stc, tdfi, coppock, entropy\n\n### Technical Achievements\n1. **Enhanced Code Generator** (`migrate_to_zero_copy.py`)\n   - Implemented brace-counting algorithm for robust function body extraction\n   - Auto-extracts Option parameter defaults from legacy functions\n   - Success rate: 50% auto + 50% manual fixup\n\n2. **Zero-Copy Infrastructure** (`rust/src/ffi/zero_copy.rs`)\n   - `to_pyarray_or_nan()`: Handles Option<Vec<f64>> → PyArray1\n   - Graceful NaN handling for computation errors\n   - Foundation for multi-output functions (Phase 2-4)\n\n3. **Safe Migration Strategy**\n   - Original functions renamed to `*_legacy` (backward compatible)\n   - Comprehensive backups in `rust/src/backups/`\n   - Integration script with dry-run mode\n\n### Validation\n- ✅ 0 compilation errors (3 harmless warnings)\n- ✅ 5/5 sample functions tested (correct NumPy output)\n- ✅ Type-safe: no runtime type coercion\n\n### Architecture Pattern\n```rust\n// Before (4 copies):\nfn py_alma(values: Vec<f64>, ...) -> Vec<f64>\n\n// After (zero-copy):\nfn py_alma<'py>(\n    py: Python<'py>,\n    values: PyReadonlyArray1<'py, f64>,  // Borrow Python data\n    ...\n) -> Py<PyArray1<f64>>  // Return NumPy view directly\n```\n\n### Migration Progress\n- Phase 1 (1→1): 30/32 ✅ (93.8%)\n  - Deferred: volume_filter, prepare_momentum_features (wrong pattern)\n- Phase 2 (n→1): 0/129 (next)\n- Phase 3 (1→n, n→m): 0/16\n- Total: 30/262 indicators (11.5%)\n\n### Breaking Changes\nNone - legacy functions remain available during transition period.\n\n### Files Changed\n- `rust/src/lib.rs`: +30 zero-copy functions\n- `scripts/migrate_to_zero_copy.py`: Code generator with default extraction\n- `scripts/auto_integrate_zero_copy.py`: Batch integration tool\n- `rust/src/ffi/zero_copy.rs`: Zero-copy helper functions\n- `tests/validation/test_zero_copy_migration.py`: Validation suite\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
          "timestamp": "2025-12-30T08:06:32Z",
          "url": "https://github.com/kwannz/haze/commit/56287755f22fabd9243d5549dfa3f3257b90076b"
        },
        "date": 1767410573740,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40786,
            "range": "± 302",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447828,
            "range": "± 530",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4521878,
            "range": "± 5303",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20294,
            "range": "± 52",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203480,
            "range": "± 345",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2035363,
            "range": "± 10057",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156903,
            "range": "± 237",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20260,
            "range": "± 36",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447759,
            "range": "± 594",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20222,
            "range": "± 46",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156890,
            "range": "± 1679",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20270,
            "range": "± 31",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93711,
            "range": "± 165",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 374139,
            "range": "± 502",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252805,
            "range": "± 1043",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203986,
            "range": "± 808",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1579851,
            "range": "± 7540",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203426,
            "range": "± 412",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4517378,
            "range": "± 17258",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203486,
            "range": "± 420",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13099202,
            "range": "± 6637",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203361,
            "range": "± 472",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40889347,
            "range": "± 17079",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203176,
            "range": "± 655",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45274190,
            "range": "± 25807",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2038048,
            "range": "± 7586",
            "unit": "ns/iter"
          }
        ]
      }
    ]
  }
}
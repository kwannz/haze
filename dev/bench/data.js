window.BENCHMARK_DATA = {
  "lastUpdate": 1768707973578,
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
        "date": 1767498643621,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40787,
            "range": "± 168",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447403,
            "range": "± 424",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4520191,
            "range": "± 20673",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20256,
            "range": "± 29",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 204066,
            "range": "± 295",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2047609,
            "range": "± 7439",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156924,
            "range": "± 208",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20238,
            "range": "± 16",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447205,
            "range": "± 334",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20194,
            "range": "± 23",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 157133,
            "range": "± 606",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20247,
            "range": "± 22",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93564,
            "range": "± 95",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373588,
            "range": "± 180",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 254343,
            "range": "± 1208",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 204117,
            "range": "± 7665",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1581756,
            "range": "± 15452",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 204446,
            "range": "± 415",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4523931,
            "range": "± 8800",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 204368,
            "range": "± 404",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13105236,
            "range": "± 8977",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203993,
            "range": "± 384",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40899006,
            "range": "± 21249",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203942,
            "range": "± 393",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45358286,
            "range": "± 74473",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2060948,
            "range": "± 3883",
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
        "date": 1767585303194,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40806,
            "range": "± 52",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 448077,
            "range": "± 843",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4526617,
            "range": "± 4859",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20255,
            "range": "± 22",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203455,
            "range": "± 603",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2037640,
            "range": "± 9621",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156909,
            "range": "± 364",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20236,
            "range": "± 13",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 448051,
            "range": "± 1968",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20179,
            "range": "± 12",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156926,
            "range": "± 1379",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20233,
            "range": "± 27",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93713,
            "range": "± 142",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373584,
            "range": "± 792",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252307,
            "range": "± 1599",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203393,
            "range": "± 1712",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1582448,
            "range": "± 12912",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203434,
            "range": "± 599",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4522893,
            "range": "± 8395",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203591,
            "range": "± 615",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13106356,
            "range": "± 155934",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203261,
            "range": "± 584",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40899964,
            "range": "± 16660",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 202976,
            "range": "± 465",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45313445,
            "range": "± 53721",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2035424,
            "range": "± 4777",
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
        "date": 1767670176957,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40776,
            "range": "± 132",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447840,
            "range": "± 6807",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4521737,
            "range": "± 211970",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20242,
            "range": "± 12",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 202987,
            "range": "± 689",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2029859,
            "range": "± 4364",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156863,
            "range": "± 215",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20228,
            "range": "± 19",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447781,
            "range": "± 343",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20176,
            "range": "± 20",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156818,
            "range": "± 454",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20220,
            "range": "± 36",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93403,
            "range": "± 162",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373577,
            "range": "± 1332",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252413,
            "range": "± 2883",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203201,
            "range": "± 313",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1579373,
            "range": "± 10253",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 202911,
            "range": "± 269",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4521407,
            "range": "± 170138",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203543,
            "range": "± 540",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13103114,
            "range": "± 377713",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203104,
            "range": "± 522",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40882428,
            "range": "± 116361",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203005,
            "range": "± 522",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45272926,
            "range": "± 19666",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2028973,
            "range": "± 1174",
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
        "date": 1767756597117,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 47898,
            "range": "± 188",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 525920,
            "range": "± 1405",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 5316087,
            "range": "± 80268",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 24211,
            "range": "± 90",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 246614,
            "range": "± 232",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2635845,
            "range": "± 24558",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 185712,
            "range": "± 1786",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 24187,
            "range": "± 28",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 525877,
            "range": "± 1155",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 24126,
            "range": "± 31",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 185606,
            "range": "± 319",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 24182,
            "range": "± 39",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 115190,
            "range": "± 121",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 478918,
            "range": "± 1430",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 259191,
            "range": "± 5369",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 248919,
            "range": "± 2597",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1880220,
            "range": "± 32914",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 246380,
            "range": "± 917",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 5342908,
            "range": "± 10830",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 245965,
            "range": "± 249",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 15013929,
            "range": "± 15488",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 245811,
            "range": "± 336",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 49495314,
            "range": "± 514825",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 245857,
            "range": "± 665",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 53857689,
            "range": "± 69052",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2651720,
            "range": "± 20578",
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
        "date": 1767843013712,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40771,
            "range": "± 169",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447391,
            "range": "± 2020",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4517312,
            "range": "± 10592",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20259,
            "range": "± 20",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203499,
            "range": "± 557",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2034515,
            "range": "± 5817",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156921,
            "range": "± 220",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20280,
            "range": "± 55",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447626,
            "range": "± 446",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20233,
            "range": "± 71",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156931,
            "range": "± 889",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20328,
            "range": "± 61",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93593,
            "range": "± 107",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373795,
            "range": "± 1019",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252445,
            "range": "± 799",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203486,
            "range": "± 643",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1579690,
            "range": "± 7490",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203614,
            "range": "± 575",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4517922,
            "range": "± 4640",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203208,
            "range": "± 279",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13102218,
            "range": "± 8727",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203142,
            "range": "± 571",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40882935,
            "range": "± 13900",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 202871,
            "range": "± 655",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45293668,
            "range": "± 62314",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2037188,
            "range": "± 6721",
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
        "date": 1767929452676,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40786,
            "range": "± 195",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447462,
            "range": "± 7500",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4518943,
            "range": "± 21330",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20258,
            "range": "± 15",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203056,
            "range": "± 3584",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2031926,
            "range": "± 10466",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156867,
            "range": "± 4576",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20229,
            "range": "± 340",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447397,
            "range": "± 5533",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20186,
            "range": "± 33",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156929,
            "range": "± 3254",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20234,
            "range": "± 26",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93526,
            "range": "± 130",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373740,
            "range": "± 339",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 253225,
            "range": "± 6405",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 204163,
            "range": "± 635",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1578731,
            "range": "± 32569",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203102,
            "range": "± 484",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4518995,
            "range": "± 29832",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203013,
            "range": "± 494",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13100171,
            "range": "± 302298",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203426,
            "range": "± 618",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40882712,
            "range": "± 188403",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203178,
            "range": "± 743",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45251960,
            "range": "± 42471",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2031116,
            "range": "± 3418",
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
        "date": 1768015510811,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40782,
            "range": "± 244",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447492,
            "range": "± 495",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4520825,
            "range": "± 5798",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20253,
            "range": "± 23",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203887,
            "range": "± 554",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2040117,
            "range": "± 6177",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156847,
            "range": "± 329",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20228,
            "range": "± 11",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447448,
            "range": "± 491",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20173,
            "range": "± 13",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156944,
            "range": "± 219",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20221,
            "range": "± 88",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93714,
            "range": "± 379",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373873,
            "range": "± 248",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 253059,
            "range": "± 1248",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203656,
            "range": "± 437",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1581332,
            "range": "± 7367",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203917,
            "range": "± 620",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4526247,
            "range": "± 9429",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203645,
            "range": "± 515",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13111515,
            "range": "± 8797",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203470,
            "range": "± 428",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40899724,
            "range": "± 54948",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203126,
            "range": "± 440",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45300095,
            "range": "± 27677",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2044765,
            "range": "± 4665",
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
        "date": 1768103402786,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40777,
            "range": "± 652",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447803,
            "range": "± 1746",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4521421,
            "range": "± 16056",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20356,
            "range": "± 59",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203433,
            "range": "± 795",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2035242,
            "range": "± 5986",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156933,
            "range": "± 311",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20244,
            "range": "± 18",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447744,
            "range": "± 399",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20308,
            "range": "± 100",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156987,
            "range": "± 522",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20404,
            "range": "± 77",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93591,
            "range": "± 200",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373702,
            "range": "± 272",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252677,
            "range": "± 8201",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203293,
            "range": "± 10899",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1583389,
            "range": "± 10191",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203344,
            "range": "± 303",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4538640,
            "range": "± 39008",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203448,
            "range": "± 859",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13117657,
            "range": "± 236843",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203238,
            "range": "± 4625",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40900493,
            "range": "± 17930",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203533,
            "range": "± 3027",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45266099,
            "range": "± 22059",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2033502,
            "range": "± 1298",
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
        "date": 1768189747130,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40779,
            "range": "± 118",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447577,
            "range": "± 1052",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4519787,
            "range": "± 8291",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20267,
            "range": "± 16",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203268,
            "range": "± 2122",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2035415,
            "range": "± 28788",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156958,
            "range": "± 226",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20237,
            "range": "± 24",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447499,
            "range": "± 2363",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20198,
            "range": "± 21",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156931,
            "range": "± 185",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20244,
            "range": "± 25",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93539,
            "range": "± 98",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373579,
            "range": "± 2295",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252623,
            "range": "± 4933",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203247,
            "range": "± 300",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1581483,
            "range": "± 17803",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203305,
            "range": "± 415",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4519213,
            "range": "± 95929",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203244,
            "range": "± 552",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13102056,
            "range": "± 8842",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203102,
            "range": "± 368",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40888206,
            "range": "± 33231",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 202757,
            "range": "± 399",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45245516,
            "range": "± 22892",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2031479,
            "range": "± 8703",
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
        "date": 1768274930659,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 47894,
            "range": "± 497",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 525683,
            "range": "± 3446",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 5312872,
            "range": "± 10273",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 24206,
            "range": "± 48",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 247310,
            "range": "± 327",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2632553,
            "range": "± 14197",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 185671,
            "range": "± 868",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 24185,
            "range": "± 30",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 525575,
            "range": "± 2030",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 24097,
            "range": "± 11",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 185709,
            "range": "± 524",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 24167,
            "range": "± 20",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 115098,
            "range": "± 83",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 478208,
            "range": "± 2103",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 245388,
            "range": "± 3126",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 246303,
            "range": "± 525",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1877020,
            "range": "± 6781",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 246215,
            "range": "± 439",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 5340977,
            "range": "± 15564",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 246207,
            "range": "± 323",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 15000906,
            "range": "± 30230",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 246995,
            "range": "± 351",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 49440956,
            "range": "± 22435",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 246676,
            "range": "± 192",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 53669063,
            "range": "± 25871",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2620580,
            "range": "± 4010",
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
        "date": 1768362450612,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40785,
            "range": "± 1011",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447517,
            "range": "± 1272",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4520857,
            "range": "± 40162",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20255,
            "range": "± 37",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203749,
            "range": "± 2197",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2041052,
            "range": "± 9804",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156845,
            "range": "± 225",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20229,
            "range": "± 35",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447298,
            "range": "± 449",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20176,
            "range": "± 386",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156851,
            "range": "± 347",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20226,
            "range": "± 13",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93591,
            "range": "± 112",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373716,
            "range": "± 389",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 253021,
            "range": "± 1585",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203843,
            "range": "± 549",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1579827,
            "range": "± 9611",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203423,
            "range": "± 354",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4518945,
            "range": "± 9595",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203720,
            "range": "± 453",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13098508,
            "range": "± 12062",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203775,
            "range": "± 502",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40887990,
            "range": "± 32066",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203169,
            "range": "± 469",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45331624,
            "range": "± 41403",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2043932,
            "range": "± 7198",
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
        "date": 1768447885703,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40798,
            "range": "± 544",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447659,
            "range": "± 620",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4522032,
            "range": "± 38271",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20258,
            "range": "± 16",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 204942,
            "range": "± 624",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2160766,
            "range": "± 23307",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156901,
            "range": "± 569",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20246,
            "range": "± 11",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447406,
            "range": "± 21119",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20178,
            "range": "± 40",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156815,
            "range": "± 587",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20219,
            "range": "± 11",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93428,
            "range": "± 59",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373591,
            "range": "± 229",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252537,
            "range": "± 1303",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 203403,
            "range": "± 16007",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1579737,
            "range": "± 6289",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203265,
            "range": "± 466",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4518264,
            "range": "± 7027",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203216,
            "range": "± 537",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13117715,
            "range": "± 15210",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 205022,
            "range": "± 742",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40928481,
            "range": "± 39146",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 204574,
            "range": "± 663",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45502295,
            "range": "± 49209",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2103729,
            "range": "± 6638",
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
        "date": 1768534230085,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40792,
            "range": "± 170",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447342,
            "range": "± 511",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4519825,
            "range": "± 5301",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20262,
            "range": "± 47",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 203860,
            "range": "± 352",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2043373,
            "range": "± 4032",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156865,
            "range": "± 4866",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20243,
            "range": "± 18",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447481,
            "range": "± 1849",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20185,
            "range": "± 40",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156844,
            "range": "± 1045",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20223,
            "range": "± 93",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93508,
            "range": "± 150",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373552,
            "range": "± 254",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252330,
            "range": "± 1455",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 202989,
            "range": "± 451",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1579274,
            "range": "± 9532",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 202791,
            "range": "± 3993",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4518926,
            "range": "± 100573",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 203301,
            "range": "± 557",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13094968,
            "range": "± 13852",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 203666,
            "range": "± 445",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40895127,
            "range": "± 53805",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 203673,
            "range": "± 719",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45299354,
            "range": "± 88381",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2030664,
            "range": "± 6884",
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
        "date": 1768620216893,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 40799,
            "range": "± 233",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 447456,
            "range": "± 979",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 4517571,
            "range": "± 23516",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 20317,
            "range": "± 34",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 202991,
            "range": "± 442",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2027350,
            "range": "± 1230",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 156870,
            "range": "± 870",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 20234,
            "range": "± 21",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 447401,
            "range": "± 441",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 20180,
            "range": "± 10",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 156903,
            "range": "± 409",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 20224,
            "range": "± 12",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 93406,
            "range": "± 70",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 373705,
            "range": "± 223",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 252355,
            "range": "± 984",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 202807,
            "range": "± 746",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1578193,
            "range": "± 4521",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 203105,
            "range": "± 1032",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 4518582,
            "range": "± 9753",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 202829,
            "range": "± 10499",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 13101728,
            "range": "± 5078",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 202812,
            "range": "± 301",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 40885888,
            "range": "± 22273",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 202419,
            "range": "± 260",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 45204173,
            "range": "± 85906",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2028060,
            "range": "± 256",
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
        "date": 1768707972328,
        "tool": "cargo",
        "benches": [
          {
            "name": "sma_large_numbers/1000",
            "value": 47781,
            "range": "± 78",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/10000",
            "value": 524384,
            "range": "± 543",
            "unit": "ns/iter"
          },
          {
            "name": "sma_large_numbers/100000",
            "value": 5303377,
            "range": "± 14633",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/10000",
            "value": 24222,
            "range": "± 949",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/100000",
            "value": 248132,
            "range": "± 213",
            "unit": "ns/iter"
          },
          {
            "name": "ema_long_sequence/1000000",
            "value": 2615732,
            "range": "± 7180",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/sma_volatile",
            "value": 185924,
            "range": "± 473",
            "unit": "ns/iter"
          },
          {
            "name": "extreme_volatility/ema_volatile",
            "value": 24276,
            "range": "± 88",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/sma_tiny",
            "value": 524355,
            "range": "± 2451",
            "unit": "ns/iter"
          },
          {
            "name": "small_numbers/ema_tiny",
            "value": 24157,
            "range": "± 36",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/sma_mixed",
            "value": 185935,
            "range": "± 403",
            "unit": "ns/iter"
          },
          {
            "name": "mixed_range/ema_mixed",
            "value": 24202,
            "range": "± 40",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/naive_sum",
            "value": 115114,
            "range": "± 108",
            "unit": "ns/iter"
          },
          {
            "name": "kahan_summation/kahan_sum",
            "value": 474817,
            "range": "± 1847",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/10",
            "value": 241491,
            "range": "± 959",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/10",
            "value": 246108,
            "range": "± 402",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/50",
            "value": 1877265,
            "range": "± 19810",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/50",
            "value": 246276,
            "range": "± 364",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/100",
            "value": 5343769,
            "range": "± 23156",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/100",
            "value": 246887,
            "range": "± 401",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/200",
            "value": 14986335,
            "range": "± 15862",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/200",
            "value": 245912,
            "range": "± 275",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/sma/500",
            "value": 49491357,
            "range": "± 58220",
            "unit": "ns/iter"
          },
          {
            "name": "period_variations/ema/500",
            "value": 246466,
            "range": "± 408",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/sma_1m_points",
            "value": 53504917,
            "range": "± 80346",
            "unit": "ns/iter"
          },
          {
            "name": "memory_efficiency/ema_1m_points",
            "value": 2615811,
            "range": "± 1348",
            "unit": "ns/iter"
          }
        ]
      }
    ]
  }
}
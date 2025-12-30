window.BENCHMARK_DATA = {
  "lastUpdate": 1767072508436,
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
      }
    ]
  }
}
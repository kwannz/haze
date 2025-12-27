import haze_library.haze_library as haze_ext

print("Checking 8 previously failing functions:")
print("=" * 50)

target_funcs = [
    'py_ulcer_index',
    'py_trix',
    'py_dpo',
    'py_volume_oscillator',
    'py_chandelier_exit',
    'py_historical_volatility',
    'py_mass_index',
    'py_force_index'
]

for fn in target_funcs:
    exists = hasattr(haze_ext, fn)
    status = "✅" if exists else "❌"
    print(f"{status} {fn}: {exists}")

# Quick functional test
if hasattr(haze_ext, 'py_ulcer_index'):
    print("\n" + "=" * 50)
    print("Quick functional test:")
    data = [100.0, 102.0, 101.0, 103.0, 105.0] * 5

    ui = haze_ext.py_ulcer_index(data, 14)
    print(f"✅ py_ulcer_index works: len={len(ui)}")

    trix = haze_ext.py_trix(data, 15)
    print(f"✅ py_trix works: len={len(trix)}")

    dpo = haze_ext.py_dpo(data, 20)
    print(f"✅ py_dpo works: len={len(dpo)}")

    vo = haze_ext.py_volume_oscillator(data, 5, 10)
    print(f"✅ py_volume_oscillator works: len={len(vo)}")

print("\nTotal py_* functions:", len([n for n in dir(haze_ext) if n.startswith('py_')]))

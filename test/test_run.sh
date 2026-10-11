#!/bin/bash
# Test the test runner, test/run.apls
# Requires: dyalog on PATH
#
# The runner loads APLSource/ as #.sm and Starmap/ as #.Starmap,
# sets #.Starmap.Data←#.sm, runs every TEST_* function in #.sm and
# every function in #.Starmap.Tests, prints one line per test and a
# summary, and exits 0 only if every test passed.
# STARMAP_EXTRA_TESTS names a further directory of tests to load
# into #.Starmap.Tests.

cd "$(dirname "$0")/.." || exit 1
FAILED=0
TIMEOUT=600

# Run the runner with a time limit (macOS has no timeout command)
runner() {
    perl -e '$t=shift; $p=fork; if(!$p){setpgrp; exec @ARGV}
        $SIG{ALRM}=sub{kill 9,-$p; exit 142}; alarm $t;
        waitpid $p,0; exit($?>>8)' "$TIMEOUT" dyalog -script test/run.apls 2>&1 |
        tr '\r' '\n'   # Dyalog ends lines with CR when output is piped
    return "${PIPESTATUS[0]}"
}

check() {
    if [[ "$2" == *"$3"* ]]; then
        echo "ok:   $1"
    else
        echo "FAIL: $1 (expected to find: $3)"
        FAILED=1
    fi
}

echo "=== All tests pass ==="
OUT=$(runner)
CODE=$?
echo "$OUT" | tail -3
[[ $CODE -eq 0 ]] && echo "ok:   exit code 0" || { echo "FAIL: exit code $CODE"; FAILED=1; }
for T in TEST_ANIMATE TEST_ANIMATEDSVG TEST_CONSTELLATIONS TEST_DAYNAME \
         TEST_FRAMESVG TEST_JNU TEST_JNUINV TEST_PIPELINE TEST_POSITIONS \
         TEST_SKYPOS TEST_STARCATALOG TEST_SVG; do
    check "book $T passes" "$OUT" "PASS sm.$T"
done
check "modern TestLoad passes" "$OUT" "PASS Starmap.Tests.TestLoad"
check "summary" "$OUT" "13 passed, 0 failed"

echo
echo "=== A failing test fails the run ==="
OUT=$(STARMAP_EXTRA_TESTS=test/fixtures/failing runner)
CODE=$?
echo "$OUT" | tail -3
[[ $CODE -ne 0 ]] && echo "ok:   nonzero exit code" || { echo "FAIL: exit code 0"; FAILED=1; }
check "failure reported" "$OUT" "FAIL Starmap.Tests.TestAlwaysFails"
check "summary" "$OUT" "13 passed, 1 failed"

echo
[[ $FAILED -eq 0 ]] && echo "test_run.sh: all checks passed" || echo "test_run.sh: checks failed"
exit $FAILED

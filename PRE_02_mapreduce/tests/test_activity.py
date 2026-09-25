"""Pruebas del taller de conteo directo con MapReduce."""

def test_builds_the_temporary_input_and_output():
    """Copia los textos y crea el resultado temporal verificable."""
    from ..src.main import INPUT_DIR, OUTPUT_DIR, run_word_count

    output_file = run_word_count()

    assert output_file == OUTPUT_DIR / "part-00000"
    assert output_file.exists()
    assert (OUTPUT_DIR / "_SUCCESS").exists()
    assert len(list(INPUT_DIR.glob("*.txt"))) == 4


def test_counts_words_after_mapping_sorting_and_reducing():
    """Conserva los conteos esperados del corpus de entrada."""
    from ..src.main import run_word_count

    output_file = run_word_count()
    counts = {
        word: int(count)
        for word, count in (
            line.rstrip().split("\t") for line in output_file.read_text().splitlines()
        )
    }

    assert counts["analytics"] == 5
    assert counts["business"] == 7
    assert counts["by"] == 3
    assert counts["algorithms"] == 2
    assert counts["analysis"] == 4

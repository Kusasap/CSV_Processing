import pytest
from pathlib import Path
from performance_report import read_files, compute_averages, write_csv


def test_read_files_and_grouping(tmp_path):
    p1 = tmp_path / "a.csv"
    p2 = tmp_path / "b.csv"
    p1.write_text("Position,Performance\nDev,90\nDev,85\nQA,80\n", encoding='utf-8')
    p2.write_text("position,performance\nQA,82\nManager,88\n", encoding='utf-8')

    data = read_files([str(p1), str(p2)])

    assert "Dev" in data
    assert len(data["Dev"]) == 2
    assert sum(data["Dev"]) == pytest.approx(175.0)

    assert "QA" in data
    assert data["QA"] == [80.0, 82.0]

    assert "Manager" in data
    assert data["Manager"] == [88.0]


def test_compute_averages_sorting():
    data = {"A": [1.0, 3.0], "B": [2.0], "C": [0.5, 0.5]}
    res = compute_averages(data)
    # mapping correctness
    mapped = dict(res)
    assert mapped["A"] == pytest.approx(2.0)
    assert mapped["B"] == pytest.approx(2.0)
    assert mapped["C"] == pytest.approx(0.5)
    # sorted descending by average
    averages = [r[1] for r in res]
    assert averages == sorted(averages, reverse=True)


def test_write_csv_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rows = [("X", 1.23456), ("Y", 2.0)]
    out = write_csv("rpt", rows)
    p = tmp_path / "rpt.csv"
    assert p.exists()
    lines = p.read_text(encoding='utf-8').splitlines()
    assert lines[0] == "position,average_performance"
    assert lines[1].startswith("X,1.234560")


def test_find_field_and_read_bad_files(tmp_path, capsys):
    from performance_report import find_field

    # find_field behaviour
    assert find_field(['Position', 'Perf'], ['position']) == 'Position'
    assert find_field([], ['position']) is None

    # file with wrong headers
    bad = tmp_path / "bad.csv"
    bad.write_text("name,age\nAlice,30\n", encoding='utf-8')

    data = read_files([str(bad)])
    captured = capsys.readouterr()
    assert "Skipping" in captured.out or data == {}


def test_main_creates_report_and_prints_table(tmp_path, monkeypatch, capsys):
    # prepare sample csvs
    f1 = tmp_path / "one.csv"
    f1.write_text("position,performance\nDev,90\nQA,80\n", encoding='utf-8')
    f2 = tmp_path / "two.csv"
    f2.write_text("position,performance\nDev,85\nManager,88\n", encoding='utf-8')

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('sys.argv', ['prog', '--files', str(f1), str(f2), '--report', 'outrep'])

    # call main
    import performance_report as pr
    pr.main()

    out = capsys.readouterr().out
    assert 'Position' in out
    # csv created
    p = tmp_path / 'outrep.csv'
    assert p.exists()


import pytest
import version_manager as vm

def test_save_version():
    version_id = vm.save_version("Бірінші мәтін")
    assert version_id is not None

def test_list_versions():
    vm.save_version("Тест мәтіні")
    assert len(vm.list_versions()) >= 1

def test_compare_versions():
    id1 = vm.save_version("Сәлем")
    id2 = vm.save_version("Сәлем әлем")
    diff = vm.compare_versions(id1, id2)
    assert any(line.startswith("+") for line in diff)

def test_restore_version():
    version_id = vm.save_version("Бастапқы мәтін")
    restored = vm.restore_version(version_id)
    assert restored == "Бастапқы мәтін"

def test_missing_version():
    with pytest.raises(ValueError):
        vm.compare_versions("wrong1", "wrong2")

def test_history_preserved():
    version_id = vm.save_version("Тарихты сақтау")
    before = len(vm.list_versions())
    vm.restore_version(version_id)
    after = len(vm.list_versions())
    assert after == before + 1


def test_compare_versions_as_text():
    id1 = vm.save_version("Бірінші мәтін")
    id2 = vm.save_version("Екінші мәтін")

    result = vm.compare_versions_as_text(id1, id2)

    assert isinstance(result, str)
    assert "Бірінші мәтін" in result
    assert "Екінші мәтін" in result

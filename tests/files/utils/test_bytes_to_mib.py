from mung_manager.files.utils import bytes_to_mib


class TestBytesToMib:
    """
    bytes_to_mib함수의 테스트 클래스

    - Test List:
        Success:
            - test_bytes_to_mib_success
    """

    def test_bytes_to_mib_success(self):
        """bytes_to_mib 함수 성공 테스트"""
        assert bytes_to_mib(1048576) == 1.0
        assert bytes_to_mib(10485760) == 10.0
        assert bytes_to_mib(104857600) == 100.0

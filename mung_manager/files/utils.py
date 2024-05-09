def bytes_to_mib(value: int) -> float:
    """이 함수는 바이트를 메비바이트로 변환합니다.
    Args:
        value (int): 바이트

    Returns:
        float: 메비바이트
    """
    # 1 bytes = 9.5367431640625E-7 mebibytes
    return value * 9.5367431640625e-7

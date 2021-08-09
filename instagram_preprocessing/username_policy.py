from typing import Set


class UserName:
    MAX_LEN: int = 30
    SPECIAL_CHAR: Set[str] = {'_', '.'}

    @classmethod
    def is_username(cls, word: str):
        return len(word) <= cls.MAX_LEN and all(ch.isalnum() or ch in cls.SPECIAL_CHAR for ch in word)


if __name__ == '__main__':
    print(UserName.is_username("Sch\u00e9nheitschirurgie"))

import asyncio
import os
import subprocess

from afreeca import AfreecaTV, GuestCredential, NotStreamingError

from utils import find_default_player, get_m3u8

default_bj = {
    "우왁굳": "ecvhao",
    "아이네": "inehine",
    "징버거": "jingburger1",
    "릴파": "lilpa0309",
    "주르르": "cotton1217",
    "고세구": "gosegu2",
    "비챤": "viichan6",
}


async def main():
    afreeca = AfreecaTV(credential=GuestCredential())

    while True:
        os.system("cls")
        print("최첨단 아프리카 타임머신 프로그램 @ minibox\n\n")

        bj_id_map = {}
        for idx, bj in enumerate(default_bj):
            print(f"[{idx + 1}] {bj}")
            bj_id_map[idx + 1] = default_bj[bj]

        select = input("\n번호 또는 BJ ID 입력 >>> ")

        if not select:
            continue

        bj_id = bj_id_map.get(int(select) if select.isdigit() else select, select)
        bj_name = select if select not in default_bj else default_bj[select]

        try:
            url = await get_m3u8(afreeca, bj_id)
        except NotStreamingError:
            print(f"\n{bj_name}님은 방송중이 아닙니다.")
            input("계속하려면 엔터를 누르세요.\n")
            continue

        vlc = find_default_player()

        if not vlc:
            print("\nVLC 플레이어가 설치되어 있지 않습니다.")
            print("https://www.videolan.org/vlc/index.html")
            input("계속하려면 엔터를 누르세요.\n")
            continue

        cmd = subprocess.list2cmdline([vlc, url])
        os.system(cmd)

        break

    input("\n\n프로그램을 종료하려면 엔터를 누르세요.\n")


if __name__ == "__main__":
    asyncio.run(main())

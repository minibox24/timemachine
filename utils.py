import os
import sys

from afreeca import AfreecaTV, NotStreamingError


# https://github.com/streamlink/streamlink
def check_paths(exes, paths):
    for path in paths:
        for exe in exes:
            path = os.path.expanduser(os.path.join(path, exe))
            if os.path.isfile(path):
                return path


def find_default_player():
    if "darwin" in sys.platform:
        paths = os.environ.get("PATH", "").split(":")
        paths += ["/Applications/VLC.app/Contents/MacOS/"]
        paths += ["~/Applications/VLC.app/Contents/MacOS/"]
        path = check_paths(("VLC", "vlc"), paths)
    elif "win32" in sys.platform:
        exename = "vlc.exe"
        paths = os.environ.get("PATH", "").split(";")
        path = check_paths((exename,), paths)

        if not path:
            subpath = "VideoLAN\\VLC\\"
            envvars = ("PROGRAMFILES", "PROGRAMFILES(X86)", "PROGRAMW6432")
            paths = filter(None, (os.environ.get(var) for var in envvars))
            paths = (os.path.join(p, subpath) for p in paths)
            path = check_paths((exename,), paths)
    else:
        paths = os.environ.get("PATH", "").split(":")
        path = check_paths(("vlc",), paths)

    if path:
        return path


async def get_m3u8(afreeca: AfreecaTV, bj_id: str):
    try:
        broad_info = await afreeca.get_broadcast_info(bj_id)
    except TypeError:
        raise NotStreamingError(bj_id)

    if not broad_info:
        raise NotStreamingError(bj_id)

    session = await afreeca.credential.get_session()

    response = await session.post(
        f"https://stbbs.afreecatv.com/api/video/get_clip_video_info.php",
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://stbbs.afreecatv.com/vodclip/index.php",
        },
        data=f"broad_no={broad_info.bno}",
    )

    data = await response.json()
    host = data["url"].split("/")[2]
    path = data["media_manifest_path"].replace(".m3u8", "_original.m3u8")

    m3u8 = f"https://{host}{path}"

    return m3u8

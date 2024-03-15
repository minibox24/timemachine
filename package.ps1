heat dir dist/timemachine/_internal -dr INSTALLFOLDER -cg TimeMachineComponent -var var.InternalDir -gg -out build/src.wxs
candle project.wxs -out build/project.wixobj -dProgramPath="$PWD/dist/timemachine/timemachine.exe"
candle build/src.wxs -dInternalDir="$PWD/dist/timemachine/_internal" -out build/src.wixobj
light -ext WixUIExtension.dll -cultures:ko-KR build/project.wixobj build/src.wixobj -o dist/timemachine.msi -ext WixUtilExtension -spdb
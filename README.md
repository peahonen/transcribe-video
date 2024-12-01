docker build -t transcribe-video .

docker run --rm -v $PWD:$PWD transcribe-video $PWD/foo.mp4

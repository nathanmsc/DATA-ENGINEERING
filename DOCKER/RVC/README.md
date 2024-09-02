## MANGIO RVC

https://huggingface.co/MangioRVC/Mangio-RVC-Huggingface/tree/main

```sh
sudo apt update
sudo apt install wget p7zip-full
wget https://huggingface.co/MangioRVC/Mangio-RVC-Huggingface/resolve/main/Mangio-RVC-v23.7.0_INFER_TRAIN.7z
7z x Mangio-RVC-v23.7.0_INFER_TRAIN.7z
docker build -t msc/mangio-rvc Mangio-RVC-v23.7.0
docker run --name mangio-rvc -p 7897:7897 msc/mangio
```

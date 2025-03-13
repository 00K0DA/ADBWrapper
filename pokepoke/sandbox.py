from image_util import count_color, get_color
def main():
    image_path = "pack_home.png"
    print(count_color(0, 0, 100, 100, image_path))
    print(get_color(0, 0, image_path))

    # [242 236 224] home

if __name__ == "__main__":
    main()
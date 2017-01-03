import sys
##from randomavatar.randomavatar import Avatar
from avatarClass import Avatar
def main(username):
    # Example usage
    avatar = Avatar(rows=10, columns=10)
    image_byte_array = avatar.get_image(string=username,
                                        width=400,
                                        height=400,
                                        pad=10)

    return avatar.save(image_byte_array=image_byte_array,
                       save_location="./static/avatars/"+username+"/default.png")


if __name__ == '__main__':
    main(sys.argv[1])

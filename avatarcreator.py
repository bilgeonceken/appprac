from avatarClass import Avatar

## createavatar funtion takes username as argument
## and generates and avatar accordingly. Returns location
## of the avatar to be added to the database
def createavatar(username):
    """creates avatar"""
    avatar = Avatar(rows=10, columns=10)
    image_byte_array = avatar.get_image(string=username,
                                        width=400,
                                        height=400,
                                        pad=10)

    save_location="./static/avatars/"+username+"/default.png"

    avatar.save(image_byte_array=image_byte_array, save_location=save_location)

    return save_location

from PIL import Image

def hide_message(image_path, message):
    # Open the image
    img = Image.open(image_path)

    # Convert the message into ASCII 8-bit code
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Add a termination bit sequence to the end of the message
    termination_sequence = '100000000'
    binary_message += termination_sequence

    # Split the binary message into batches of 9 bits
    batches = [binary_message[i:i+9] for i in range(0, len(binary_message), 9)]

    # Select the red channel
    pixels = list(img.getdata())

    # Iterate through the batches
    for i, batch in enumerate(batches):
        # Write each batch into the least significant bits of the pixels
        for j, bit in enumerate(batch):
            pixel_index = i * 9 + j
            pixel_value = pixels[pixel_index][0]
            new_pixel_value = (pixel_value & ~1) | int(bit)
            pixels[pixel_index] = (new_pixel_value, pixels[pixel_index][1], pixels[pixel_index][2])

    # Save the modified image
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(pixels)
    new_img.save('output.png')

def retrieve_message(image_path):
    # Open the image
    img = Image.open(image_path)

    # Select the red channel
    pixels = list(img.getdata())

    # Initialize variables
    message_bits = []
    termination_found = False

    # Iterate through each pixel
    for pixel in pixels:
        # Extract the least significant bit from the red channel
        bit = pixel[0] & 1
        # Append the bit to the message bits list
        message_bits.append(str(bit))

        # Check for termination sequence '100000000' (binary for '1' followed by 8 zeros)
        if len(message_bits) >= 9 and ''.join(message_bits[-9:]) == '100000000':
            termination_found = True
            break

    if termination_found:
        # Convert message bits to characters
        message_bits = message_bits[:-9]  # Remove termination sequence
        message_binary = ''.join(message_bits)
        message_length = len(message_binary) // 8 * 8  # Ensure length is multiple of 8
        message_chars = [chr(int(message_binary[i:i+8], 2)) for i in range(0, message_length, 8)]
        message = ''.join(message_chars)
    else:
        message = "Termination bit not found. Message may be incomplete or missing."

    return message

# Example usage:
hide_message('image_path.png', 'Hello, World!')
print(retrieve_message('output.png'))

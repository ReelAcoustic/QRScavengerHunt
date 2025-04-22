import qrcode
import os

def generate_qr(text, filename):
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Save the image
    img.save(filename)
    print(f"QR code saved as {filename}")

if __name__ == "__main__":
    # Example usage to generate a QR code for each objective
    objectives = [
        "Welcome to CRASH HQ. ID=0",
        "Near Hub City is our FOB, resupply inbound. ID=1",
        "We need new recruits, there's only one other bulldog in this town! Find him for additional personnel. ID=2",
        "Find the secret file, it should be somewhere information is stored on shelves!. ID=3"
    ]

    # Save each QR code as a .png file
    if not os.path.exists('qr_codes'):
        os.mkdir('qr_codes')  # Create a directory for the QR codes

    for i, obj in enumerate(objectives):
        generate_qr(obj, f"qr_codes/qr_objective_{i+1}.png")

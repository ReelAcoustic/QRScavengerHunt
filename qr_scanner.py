import cv2

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    print("Scanning for QR code...")
    scanned_text = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera error.")
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        cv2.imshow("Scan QR Code (press 'q' to quit)", frame)

        if data:
            scanned_text = data
            print(f"QR Code Detected: {scanned_text}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Scan canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()

    return scanned_text  # ✅ Return a clean string

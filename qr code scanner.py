import cv2

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access camera.")
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        cv2.imshow("QR Scanner (press 'q' to quit)", frame)

        if data:
            print(f"Scanned QR Code: {data}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Scan canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return data if data else None

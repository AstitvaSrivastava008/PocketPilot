import os
from datetime import datetime


class ReceiptScanner:
    """
    Foundation for PocketPilot's receipt and screenshot
    transaction capture system.

    Phase 1:
    - Accept a receipt/screenshot image
    - Validate the image
    - Store its path
    - Prepare the structure for OCR extraction

    OCR and AI extraction will be added in later phases.
    """

    # =========================================================
    # SUPPORTED IMAGE FORMATS
    # =========================================================

    SUPPORTED_EXTENSIONS = (
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
    )

    # =========================================================
    # VALIDATE IMAGE
    # =========================================================

    @staticmethod
    def validate_image(image_path):
        """
        Check whether the supplied file exists and has
        a supported image extension.

        Returns:
            (True, "Valid image")
            or
            (False, "Error message")
        """

        if not image_path:
            return False, "No image path was provided."

        if not os.path.exists(image_path):
            return False, "Image file does not exist."

        if not os.path.isfile(image_path):
            return False, "The selected path is not a file."

        extension = os.path.splitext(image_path)[1].lower()

        if extension not in ReceiptScanner.SUPPORTED_EXTENSIONS:
            return (
                False,
                "Unsupported image format. "
                "Use PNG, JPG, JPEG, WEBP, or BMP."
            )

        return True, "Valid image."

    # =========================================================
    # PREPARE IMAGE
    # =========================================================

    @staticmethod
    def prepare_image(image_path):
        """
        Validate and prepare an image for future OCR/AI
        processing.

        Returns a dictionary containing the image information.
        """

        valid, message = ReceiptScanner.validate_image(
            image_path
        )

        if not valid:
            return {
                "success": False,
                "message": message,
            }

        absolute_path = os.path.abspath(image_path)

        file_size = os.path.getsize(absolute_path)

        extension = os.path.splitext(
            absolute_path
        )[1].lower()

        return {
            "success": True,
            "message": "Image ready for processing.",
            "image_path": absolute_path,
            "file_name": os.path.basename(absolute_path),
            "extension": extension,
            "file_size": file_size,
            "prepared_at": datetime.now().isoformat(
                timespec="seconds"
            ),
        }

    # =========================================================
    # PLACEHOLDER FOR OCR
    # =========================================================

    @staticmethod
    def extract_transaction_data(image_path):
        """
        Placeholder for the OCR/AI extraction stage.

        This method will later extract information such as:

        - Merchant
        - Amount
        - Date
        - Transaction type
        - Category
        - Description

        For now, it only validates and prepares the image.
        """

        result = ReceiptScanner.prepare_image(
            image_path
        )

        if not result["success"]:
            return result

        return {
            "success": True,
            "message": (
                "Image prepared successfully. "
                "OCR extraction will be added in the next phase."
            ),
            "image_path": result["image_path"],
            "file_name": result["file_name"],
            "extension": result["extension"],
        }
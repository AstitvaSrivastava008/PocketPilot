import os
import tkinter as tk
from tkinter import filedialog

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from receipt.receipt_scanner import ReceiptScanner


class ReceiptScreen(Screen):

    selected_image_path = ""

    def on_pre_enter(self):
        """
        Reset the screen when entering it.
        """
        self.selected_image_path = ""

        if "receipt_image" in self.ids:
            self.ids.receipt_image.source = ""
            self.ids.receipt_image.opacity = 0

        if "status_label" in self.ids:
            self.ids.status_label.text = (
                "No receipt selected"
            )

        if "instruction_label" in self.ids:
            self.ids.instruction_label.text = (
                "Select a receipt or payment screenshot to begin."
            )

        if "process_button" in self.ids:
            self.ids.process_button.disabled = True

    # =========================================================
    # SELECT RECEIPT / SCREENSHOT
    # =========================================================

    def select_receipt(self):
        """
        Opens the native Windows file picker.

        Supported image formats:
        JPG
        JPEG
        PNG
        """

        # Create a hidden Tkinter root window
        root = tk.Tk()
        root.withdraw()

        # Prevent an unnecessary Tkinter window from appearing
        root.attributes("-topmost", True)

        # Start inside the PocketPilot receipt folder
        receipt_folder = os.path.abspath(
            os.path.join(
                os.path.dirname(
                    os.path.dirname(__file__)
                ),
                "receipt"
            )
        )

        # Make sure the folder exists
        if not os.path.exists(receipt_folder):
            os.makedirs(receipt_folder)

        file_path = filedialog.askopenfilename(
            title="Select Receipt / Payment Screenshot",
            initialdir=receipt_folder,
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png"
                ),
                (
                    "JPG Images",
                    "*.jpg"
                ),
                (
                    "JPEG Images",
                    "*.jpeg"
                ),
                (
                    "PNG Images",
                    "*.png"
                ),
                (
                    "All Files",
                    "*.*"
                ),
            ],
        )

        root.destroy()

        if not file_path:
            return

        self.load_selected_image(file_path)

    # =========================================================
    # LOAD SELECTED IMAGE
    # =========================================================

    def load_selected_image(self, file_path):
        """
        Validates the selected image and displays it.
        """

        result = ReceiptScanner.prepare_image(
            file_path
        )

        if not result.get("success"):
            self.ids.status_label.text = (
                result.get(
                    "message",
                    "Unable to load the selected image."
                )
            )

            self.ids.instruction_label.text = (
                "Please select a valid JPG, JPEG or PNG image."
            )

            self.ids.process_button.disabled = True

            return

        self.selected_image_path = (
            result["image_path"]
        )

        # Display image
        self.ids.receipt_image.source = (
            self.selected_image_path
        )

        self.ids.receipt_image.opacity = 1

        self.ids.status_label.text = (
            result["file_name"]
        )

        self.ids.instruction_label.text = (
            "Receipt selected successfully. "
            "You can now process it."
        )

        self.ids.process_button.disabled = False

        # Force Kivy to reload the image
        self.ids.receipt_image.reload()

    # =========================================================
    # PROCESS RECEIPT
    # =========================================================

    def process_receipt(self):
        """
        Placeholder for the OCR / AI processing stage.

        OCR and automatic transaction extraction will be
        connected in the next stage.
        """

        if not self.selected_image_path:
            self.ids.status_label.text = (
                "Please select a receipt first."
            )

            return

        self.ids.status_label.text = (
            "Receipt ready for AI processing."
        )

        self.ids.instruction_label.text = (
            "The image has been prepared successfully. "
            "OCR and transaction extraction will be added next."
        )

    # =========================================================
    # CLEAR IMAGE
    # =========================================================

    def clear_image(self):
        """
        Clears the selected receipt.
        """

        self.selected_image_path = ""

        self.ids.receipt_image.source = ""

        self.ids.receipt_image.opacity = 0

        self.ids.status_label.text = (
            "No receipt selected"
        )

        self.ids.instruction_label.text = (
            "Select a receipt or payment screenshot to begin."
        )

        self.ids.process_button.disabled = True

    # =========================================================
    # BACK
    # =========================================================

    def go_back(self):
        """
        Return to Add Transaction.
        """

        self.manager.current = "add_transaction"
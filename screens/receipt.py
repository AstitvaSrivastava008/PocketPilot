import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

import pytesseract
from PIL import Image

from kivy.app import App
from kivy.uix.screenmanager import Screen

from database import add_transaction

from receipt.receipt_scanner import ReceiptScanner
from receipt.transaction_parser import TransactionParser


class ReceiptScreen(Screen):
    """
    Smart Transaction screen.

    Flow:

        Select Receipt
            ↓
        Windows File Explorer
            ↓
        Receipt Preview
            ↓
        OCR
            ↓
        Transaction Parser
            ↓
        Review
            ↓
        Save
    """

    selected_image = ""
    extracted_data = None

    # =========================================================
    # SCREEN ENTER
    # =========================================================

    def on_pre_enter(self):

        if not self.selected_image:
            self.reset_screen()

    # =========================================================
    # SELECT RECEIPT
    # =========================================================

    def select_receipt(self):
        """
        Opens the normal Windows file selection dialog.

        No Kivy Popup.
        No Kivy FileChooser.

        The dialog starts directly inside:

            D:\PocketPilot\receipt
        """

        try:

            # -------------------------------------------------
            # Find PocketPilot/receipt folder
            # -------------------------------------------------

            project_folder = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            receipt_folder = os.path.join(
                project_folder,
                "receipt"
            )

            os.makedirs(
                receipt_folder,
                exist_ok=True
            )

            # -------------------------------------------------
            # Create hidden Tkinter root
            # -------------------------------------------------

            root = tk.Tk()

            root.withdraw()

            # Keep the Windows dialog in front.
            root.attributes(
                "-topmost",
                True
            )

            # -------------------------------------------------
            # Open NORMAL Windows file dialog
            # -------------------------------------------------

            selected_file = filedialog.askopenfilename(
                title="Select Receipt / Screenshot",

                initialdir=receipt_folder,

                filetypes=[
                    (
                        "Receipt Images",
                        "*.png *.jpg *.jpeg *.bmp *.webp"
                    ),
                    (
                        "PNG Images",
                        "*.png"
                    ),
                    (
                        "JPEG Images",
                        "*.jpg *.jpeg"
                    ),
                    (
                        "All Files",
                        "*.*"
                    )
                ]
            )

            # -------------------------------------------------
            # Destroy Tkinter root
            # -------------------------------------------------

            root.destroy()

            # -------------------------------------------------
            # User cancelled
            # -------------------------------------------------

            if not selected_file:

                self.ids.receipt_status.text = (
                    "No receipt selected"
                )

                self.ids.status_label.text = (
                    "Select a receipt or payment "
                    "screenshot to begin."
                )

                return

            # -------------------------------------------------
            # Load selected image
            # -------------------------------------------------

            self.load_selected_image(
                selected_file
            )

        except Exception as error:

            print(
                "File selection error:",
                error
            )

            self.ids.status_label.text = (
                f"Unable to open file selector: {error}"
            )

    # =========================================================
    # LOAD SELECTED IMAGE
    # =========================================================

    def load_selected_image(self, image_path):
        """
        Validate and display the selected receipt.
        """

        try:

            result = ReceiptScanner.prepare_image(
                image_path
            )

            if not result.get("success"):

                self.ids.status_label.text = (
                    result.get(
                        "message",
                        "Unable to prepare the image."
                    )
                )

                return

            self.selected_image = (
                result["image_path"]
            )

            # -------------------------------------------------
            # Display image
            # -------------------------------------------------

            self.ids.receipt_image.source = (
                self.selected_image
            )

            self.ids.receipt_image.reload()

            # -------------------------------------------------
            # Update status
            # -------------------------------------------------

            self.ids.receipt_status.text = (
                "Receipt ready for AI processing."
            )

            self.ids.status_label.text = (
                f"Selected: {result['file_name']}"
            )

            self.ids.instruction_label.text = (
                "The image has been prepared successfully. "
                "Press Process Receipt to extract "
                "the transaction."
            )

            # -------------------------------------------------
            # Enable processing
            # -------------------------------------------------

            self.ids.process_button.disabled = False

            # -------------------------------------------------
            # Clear old result
            # -------------------------------------------------

            self.extracted_data = None

            self.ids.extracted_card.opacity = 0
            self.ids.extracted_card.disabled = True

            self.ids.save_button.disabled = True

        except Exception as error:

            print(
                "Image loading error:",
                error
            )

            self.ids.status_label.text = (
                f"Unable to load image: {error}"
            )

    # =========================================================
    # PROCESS RECEIPT
    # =========================================================

    def process_receipt(self):

        if not self.selected_image:

            self.ids.status_label.text = (
                "Please select a receipt first."
            )

            return

        self.ids.receipt_status.text = (
            "Processing receipt..."
        )

        self.ids.status_label.text = (
            "Reading receipt and extracting "
            "transaction information..."
        )

        self.ids.process_button.disabled = True

        try:

            # -------------------------------------------------
            # Tesseract
            # -------------------------------------------------

            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )

            # -------------------------------------------------
            # Open image
            # -------------------------------------------------

            image = Image.open(
                self.selected_image
            )

            # -------------------------------------------------
            # OCR
            # -------------------------------------------------

            ocr_text = pytesseract.image_to_string(
                image
            )

            print(
                "\n========================================"
            )

            print(
                "POCKETPILOT OCR OUTPUT"
            )

            print(
                "========================================"
            )

            print(ocr_text)

            print(
                "========================================\n"
            )

            if not ocr_text.strip():

                self.ids.receipt_status.text = (
                    "No readable text found."
                )

                self.ids.status_label.text = (
                    "Try a clearer receipt or "
                    "payment screenshot."
                )

                return

            # -------------------------------------------------
            # Parse transaction
            # -------------------------------------------------

            transaction = TransactionParser.parse(
                ocr_text
            )

            if not transaction.get("success"):

                self.ids.receipt_status.text = (
                    "Transaction extraction failed."
                )

                self.ids.status_label.text = (
                    transaction.get(
                        "message",
                        "Unable to extract "
                        "transaction details."
                    )
                )

                return

            # -------------------------------------------------
            # Store result
            # -------------------------------------------------

            self.extracted_data = transaction

            # -------------------------------------------------
            # Display result
            # -------------------------------------------------

            self.display_transaction(
                transaction
            )

            self.ids.receipt_status.text = (
                "Transaction extracted successfully."
            )

            self.ids.status_label.text = (
                "Review the extracted information "
                "before saving."
            )

            self.ids.save_button.disabled = False

        except Exception as error:

            print(
                "Receipt processing error:",
                error
            )

            self.ids.receipt_status.text = (
                "Receipt processing failed."
            )

            self.ids.status_label.text = (
                f"Error: {error}"
            )

        finally:

            self.ids.process_button.disabled = False

    # =========================================================
    # DISPLAY TRANSACTION
    # =========================================================

    def display_transaction(self, transaction):

        merchant = (
            transaction.get("merchant")
            or "Not detected"
        )

        amount = transaction.get(
            "amount"
        )

        if amount is None:
            amount_text = "Not detected"
        else:
            amount_text = (
                f"₹{float(amount):,.2f}"
            )

        date = (
            transaction.get("date")
            or "Not detected"
        )

        time = (
            transaction.get("time")
            or "Not detected"
        )

        transaction_type = (
            transaction.get("type")
            or "expense"
        )

        category = (
            transaction.get("category")
            or "Other"
        )

        description = (
            transaction.get("description")
            or merchant
            or "Receipt transaction"
        )

        payment_method = (
            transaction.get("payment_method")
            or "Not detected"
        )

        upi_id = (
            transaction.get("upi_id")
            or "Not detected"
        )

        transaction_id = (
            transaction.get("transaction_id")
            or "Not detected"
        )

        self.ids.merchant_value.text = (
            str(merchant)
        )

        self.ids.amount_value.text = (
            amount_text
        )

        self.ids.date_value.text = (
            f"Date: {date}"
        )

        self.ids.time_value.text = (
            f"Time: {time}"
        )

        self.ids.type_value.text = (
            f"Type: {transaction_type.capitalize()}"
        )

        self.ids.category_value.text = (
            str(category)
        )

        self.ids.description_value.text = (
            str(description)
        )

        self.ids.payment_value.text = (
            f"Payment Method: {payment_method}"
        )

        self.ids.upi_value.text = (
            f"UPI ID: {upi_id}"
        )

        self.ids.transaction_id_value.text = (
            f"Transaction ID: {transaction_id}"
        )

        self.ids.extracted_card.opacity = 1
        self.ids.extracted_card.disabled = False

    # =========================================================
    # SAVE TRANSACTION
    # =========================================================

    def save_transaction(self):

        if not self.extracted_data:

            self.ids.status_label.text = (
                "Please process a receipt first."
            )

            return

        app = App.get_running_app()

        if app.current_user is None:

            self.ids.status_label.text = (
                "No logged-in user found."
            )

            return

        user_id = app.current_user[0]

        transaction_type = (
            self.extracted_data.get(
                "type"
            )
            or "expense"
        )

        amount = (
            self.extracted_data.get(
                "amount"
            )
        )

        category = (
            self.extracted_data.get(
                "category"
            )
            or "Other"
        )

        description = (
            self.extracted_data.get(
                "description"
            )
            or self.extracted_data.get(
                "merchant"
            )
            or "Receipt transaction"
        )

        transaction_date = (
            self.extracted_data.get(
                "date"
            )
        )

        try:

            amount = float(amount)

        except (
            TypeError,
            ValueError
        ):

            self.ids.status_label.text = (
                "Invalid transaction amount."
            )

            return

        if amount <= 0:

            self.ids.status_label.text = (
                "Transaction amount must be "
                "greater than zero."
            )

            return

        if transaction_type not in (
            "income",
            "expense"
        ):

            transaction_type = "expense"

        if not transaction_date:

            transaction_date = (
                datetime.now().strftime(
                    "%Y-%m-%d"
                )
            )

        try:

            add_transaction(
                user_id=user_id,
                transaction_type=transaction_type,
                amount=amount,
                category=category,
                description=description,
                date=transaction_date
            )

            self.ids.receipt_status.text = (
                "✓ Transaction saved successfully!"
            )

            self.ids.status_label.text = (
                f"₹{amount:,.2f} "
                f"{transaction_type} transaction "
                "has been added to PocketPilot."
            )

            self.ids.save_button.disabled = True

            # Refresh screens if supported.
            try:
                self.manager.get_screen(
                    "history"
                ).on_pre_enter()
            except Exception:
                pass

            try:
                self.manager.get_screen(
                    "analytics"
                ).on_pre_enter()
            except Exception:
                pass

            try:
                self.manager.get_screen(
                    "home"
                ).on_pre_enter()
            except Exception:
                pass

        except Exception as error:

            print(
                "Transaction save error:",
                error
            )

            self.ids.status_label.text = (
                f"Could not save transaction: {error}"
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_receipt(self):

        self.selected_image = ""
        self.extracted_data = None

        self.ids.receipt_image.source = ""

        self.ids.receipt_status.text = (
            "No receipt selected"
        )

        self.ids.status_label.text = (
            "Select a receipt or payment "
            "screenshot to begin."
        )

        self.ids.instruction_label.text = (
            "Choose a receipt from the "
            "PocketPilot receipt folder."
        )

        self.ids.process_button.disabled = True
        self.ids.save_button.disabled = True

        self.ids.extracted_card.opacity = 0
        self.ids.extracted_card.disabled = True

    # =========================================================
    # RESET
    # =========================================================

    def reset_screen(self):

        self.selected_image = ""
        self.extracted_data = None

        if "receipt_image" in self.ids:
            self.ids.receipt_image.source = ""

        if "receipt_status" in self.ids:
            self.ids.receipt_status.text = (
                "No receipt selected"
            )

        if "status_label" in self.ids:
            self.ids.status_label.text = (
                "Select a receipt or payment "
                "screenshot to begin."
            )

        if "instruction_label" in self.ids:
            self.ids.instruction_label.text = (
                "Choose a receipt from the "
                "PocketPilot receipt folder."
            )

        if "process_button" in self.ids:
            self.ids.process_button.disabled = True

        if "save_button" in self.ids:
            self.ids.save_button.disabled = True

        if "extracted_card" in self.ids:
            self.ids.extracted_card.opacity = 0
            self.ids.extracted_card.disabled = True

    # =========================================================
    # BACK
    # =========================================================

    def go_back(self):

        self.manager.current = (
            "add_transaction"
        )
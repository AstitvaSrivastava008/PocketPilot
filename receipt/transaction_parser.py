import re
from datetime import datetime


class TransactionParser:
    """
    Converts raw OCR text from a payment receipt or
    transaction screenshot into structured transaction data.

    This parser works locally and does not require
    an internet connection or external AI API.
    """

    # =========================================================
    # MAIN PARSER
    # =========================================================

    @staticmethod
    def parse(ocr_text):
        """
        Parse raw OCR text and return structured transaction data.
        """

        if not ocr_text or not ocr_text.strip():

            return {
                "success": False,
                "message": "No OCR text was provided.",
            }

        text = ocr_text.strip()

        merchant = TransactionParser.extract_merchant(text)

        amount = TransactionParser.extract_amount(text)

        date = TransactionParser.extract_date(text)

        time = TransactionParser.extract_time(text)

        description = TransactionParser.extract_description(text)

        payment_method = (
            TransactionParser.extract_payment_method(text)
        )

        upi_id = TransactionParser.extract_upi_id(text)

        transaction_id = (
            TransactionParser.extract_transaction_id(text)
        )

        transaction_type = (
            TransactionParser.detect_transaction_type(text)
        )

        category = TransactionParser.detect_category(
            merchant,
            description,
            text
        )

        return {
            "success": True,
            "merchant": merchant,
            "amount": amount,
            "date": date,
            "time": time,
            "type": transaction_type,
            "category": category,
            "description": description,
            "payment_method": payment_method,
            "upi_id": upi_id,
            "transaction_id": transaction_id,
        }

    # =========================================================
    # MERCHANT
    # =========================================================

    @staticmethod
    def extract_merchant(text):

        match = re.search(
            r"\bto\s+([A-Za-z][A-Za-z0-9& .'-]{1,50})",
            text,
            re.IGNORECASE
        )

        if match:

            merchant = match.group(1).strip()

            # Only keep the first line
            merchant = merchant.split("\n")[0].strip()

            # Remove common trailing OCR text
            merchant = re.split(
                r"\b(?:Payment|UPI|Txn|Transaction)\b",
                merchant,
                flags=re.IGNORECASE
            )[0].strip()

            return merchant

        # Fallback
        if re.search(
            r"\bblinkit\b",
            text,
            re.IGNORECASE
        ):
            return "Blinkit"

        return None

    # =========================================================
    # AMOUNT
    # =========================================================

    @staticmethod
    def extract_amount(text):

        patterns = [

            # ₹240
            r"[₹]\s*([0-9,]+(?:\.[0-9]{1,2})?)",

            # Rs 240
            r"\bRs\.?\s*([0-9,]+(?:\.[0-9]{1,2})?)",

            # INR 240
            r"\bINR\s*([0-9,]+(?:\.[0-9]{1,2})?)",

            # #240
            r"#\s*([0-9,]+(?:\.[0-9]{1,2})?)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                amount_text = match.group(1)

                amount_text = (
                    amount_text.replace(",", "")
                )

                try:
                    return float(amount_text)

                except ValueError:
                    pass

        return None

    # =========================================================
    # DATE
    # =========================================================

    @staticmethod
    def extract_date(text):

        # Example:
        # 19 Aug 2026

        match = re.search(
            r"\b(\d{1,2}\s+"
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
            r"\s+\d{4})\b",
            text,
            re.IGNORECASE
        )

        if match:

            date_text = match.group(1)

            try:

                parsed_date = datetime.strptime(
                    date_text,
                    "%d %b %Y"
                )

                return parsed_date.strftime(
                    "%Y-%m-%d"
                )

            except ValueError:

                return date_text

        # Fallback: DD/MM/YYYY

        match = re.search(
            r"\b(\d{1,2}/\d{1,2}/\d{4})\b",
            text
        )

        if match:

            date_text = match.group(1)

            try:

                parsed_date = datetime.strptime(
                    date_text,
                    "%d/%m/%Y"
                )

                return parsed_date.strftime(
                    "%Y-%m-%d"
                )

            except ValueError:

                return date_text

        return None

    # =========================================================
    # TIME
    # =========================================================

    @staticmethod
    def extract_time(text):

        match = re.search(
            r"\b(\d{1,2}:\d{2}\s*(?:AM|PM))\b",
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).upper()

        return None

    # =========================================================
    # DESCRIPTION
    # =========================================================

    @staticmethod
    def extract_description(text):
        """
        Extract a useful transaction description.

        For example:

        Blinkit Payment

        instead of accidentally extracting unrelated
        OCR text such as "Paid securely on Payment".
        """

        merchant = TransactionParser.extract_merchant(text)

        if merchant:

            # Escape merchant so special regex characters
            # cannot cause problems.
            merchant_pattern = re.escape(
                merchant
            )

            pattern = (
                r"\b"
                + merchant_pattern
                + r"\s+Payment\b"
            )

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return match.group(0).strip()

        # Fallback: search line-by-line
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for line in lines:

            lower_line = line.lower()

            if (
                "payment" in lower_line
                and "successful" not in lower_line
                and "paid securely" not in lower_line
                and len(line) <= 80
            ):

                return line

        # Final fallback
        if merchant:

            return f"{merchant} Payment"

        return None

    # =========================================================
    # PAYMENT METHOD
    # =========================================================

    @staticmethod
    def extract_payment_method(text):

        if re.search(
            r"\bUPI\b",
            text,
            re.IGNORECASE
        ):
            return "UPI"

        if re.search(
            r"\bcredit\s+card\b|\bdebit\s+card\b|\bcard\b",
            text,
            re.IGNORECASE
        ):
            return "Card"

        if re.search(
            r"\bnet\s*banking\b",
            text,
            re.IGNORECASE
        ):
            return "Net Banking"

        if re.search(
            r"\bcash\b",
            text,
            re.IGNORECASE
        ):
            return "Cash"

        return None

    # =========================================================
    # UPI ID
    # =========================================================

    @staticmethod
    def extract_upi_id(text):

        match = re.search(
            r"\b[\w.-]+@[\w.-]+\b",
            text
        )

        if match:

            return match.group(0)

        return None

    # =========================================================
    # TRANSACTION ID
    # =========================================================

    @staticmethod
    def extract_transaction_id(text):

        patterns = [

            r"UPI\s+txn\s+ID\s*[:\-]?\s*([A-Za-z0-9]+)",

            r"Transaction\s+ID\s*[:\-]?\s*([A-Za-z0-9]+)",

            r"Txn\s+ID\s*[:\-]?\s*([A-Za-z0-9]+)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return match.group(1)

        return None

    # =========================================================
    # TRANSACTION TYPE
    # =========================================================

    @staticmethod
    def detect_transaction_type(text):

        lower_text = text.lower()

        income_keywords = [
            "received",
            "credited",
            "credit",
            "refund",
            "money received",
        ]

        expense_keywords = [
            "payment successful",
            "paid",
            "sent",
            "debited",
            "debit",
            "to ",
        ]

        # Check income first
        for keyword in income_keywords:

            if keyword in lower_text:

                return "income"

        # Then expense
        for keyword in expense_keywords:

            if keyword in lower_text:

                return "expense"

        # Payment screenshots are normally expenses
        if "payment" in lower_text:

            return "expense"

        return "expense"

    # =========================================================
    # CATEGORY
    # =========================================================

    @staticmethod
    def detect_category(
        merchant,
        description,
        text
    ):

        combined_text = " ".join(
            value
            for value in [
                merchant,
                description,
                text
            ]
            if value
        ).lower()

        # -----------------------------------------------------
        # FOOD / GROCERIES
        # -----------------------------------------------------

        food_keywords = [
            "blinkit",
            "zepto",
            "swiggy",
            "zomato",
            "food",
            "grocery",
            "groceries",
            "restaurant",
            "cafe",
            "mcdonald",
            "pizza",
            "domino",
        ]

        for keyword in food_keywords:

            if keyword in combined_text:

                return "Food"

        # -----------------------------------------------------
        # SHOPPING
        # -----------------------------------------------------

        shopping_keywords = [
            "amazon",
            "flipkart",
            "myntra",
            "shopping",
            "ajio",
            "meesho",
        ]

        for keyword in shopping_keywords:

            if keyword in combined_text:

                return "Shopping"

        # -----------------------------------------------------
        # TRAVEL
        # -----------------------------------------------------

        travel_keywords = [
            "uber",
            "ola",
            "rapido",
            "flight",
            "hotel",
            "travel",
            "irctc",
        ]

        for keyword in travel_keywords:

            if keyword in combined_text:

                return "Travel"

        # -----------------------------------------------------
        # BILLS
        # -----------------------------------------------------

        bill_keywords = [
            "electricity",
            "electric bill",
            "water bill",
            "wifi",
            "internet",
            "recharge",
            "mobile recharge",
        ]

        for keyword in bill_keywords:

            if keyword in combined_text:

                return "Bills"

        # -----------------------------------------------------
        # ENTERTAINMENT
        # -----------------------------------------------------

        entertainment_keywords = [
            "netflix",
            "prime video",
            "spotify",
            "movie",
            "cinema",
        ]

        for keyword in entertainment_keywords:

            if keyword in combined_text:

                return "Entertainment"

        # -----------------------------------------------------
        # DEFAULT
        # -----------------------------------------------------

        return "Other"
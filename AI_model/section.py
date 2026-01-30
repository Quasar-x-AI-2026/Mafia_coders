from livekit.agents import function_tool, RunContext

@function_tool()
async def fee_submission_guide(context: RunContext, institute_category: str) -> str:
    """
    Gives step-by-step fee submission procedure
    based on the category of school or college.
    """

    fee_data = {
        "central_government_institute": {
            "title": "Central Government Institutes (IIIT / IIT / NIT / IIM)",
            "method": "SBI Collect / Official Institute Fee Portal",
            "steps": [
                "Visit the official institute website",
                "Open the Fees or Payments section",
                "Click on Pay Fees via SBI Collect",
                "Select the State",
                "Select the Institute name",
                "Enter roll number, name, and semester",
                "Enter the payable fee amount",
                "Choose payment mode (UPI / Net Banking / Card)",
                "Complete the payment",
                "Download and save the payment receipt",
                "Upload receipt on institute portal if required"
            ],
            "note": "Fee payment is fully online. Cash is not accepted."
        },

        "state_board_school": {
            "title": "State Board Schools (Government / Aided)",
            "method": "School Accounts Section (Offline)",
            "steps": [
                "Visit the school campus",
                "Go to the Accounts / Fee Counter",
                "Provide student name, class, and roll number",
                "Pay fees using cash, DD, or bank challan",
                "Accountant verifies the amount",
                "Fee entry is recorded in school register",
                "Collect the official fee receipt"
            ],
            "note": "Mostly offline payment method."
        },

        "cbse_icse_private_school": {
            "title": "CBSE / ICSE Private Schools",
            "method": "School ERP / Online Portal",
            "steps": [
                "Login to the school ERP or parent portal",
                "Navigate to the Fee Payment section",
                "Check pending or due fees",
                "Select online payment method",
                "Complete the payment",
                "Download or print the receipt"
            ],
            "note": "Some schools allow limited offline payment."
        },

        "central_government_school": {
            "title": "Central Government Schools (Kendriya Vidyalaya / JNV)",
            "method": "KVS / Government Payment Portal",
            "steps": [
                "Visit the KVS or respective school portal",
                "Click on Online Fee Payment",
                "Enter student details",
                "Confirm fee amount",
                "Make payment online",
                "Save the payment receipt"
            ],
            "note": "Cash payment is generally not allowed."
        },

        "private_college_university": {
            "title": "Private Colleges / Universities",
            "method": "University Student Portal",
            "steps": [
                "Login to the student portal",
                "Open the Fees or Finance section",
                "Select academic year or semester",
                "Confirm payable amount",
                "Pay using online methods",
                "Download payment receipt"
            ],
            "note": "Payment confirmation is instant."
        }
    }

    key = institute_category.lower().strip()

    if key not in fee_data:
        return (
            "Invalid institute category.\n\n"
            "Valid categories:\n"
            "- central_government_institute\n"
            "- state_board_school\n"
            "- cbse_icse_private_school\n"
            "- central_government_school\n"
            "- private_college_university"
        )

    data = fee_data[key]

    response = f"{data['title']}\n"
    response += f"Fee Payment Method: {data['method']}\n\n"
    response += "Step-by-Step Fee Submission:\n"

    for i, step in enumerate(data["steps"], start=1):
        response += f"{i}. {step}\n"

    response += f"\nNote: {data['note']}"

    return response

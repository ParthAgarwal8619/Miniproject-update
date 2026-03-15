def generate_response(category):

    if category == "Complaint":
        return "We are sorry for the inconvenience. Our support team will resolve your issue shortly."

    elif category == "Query":
        return "Thank you for contacting us. Our team will provide the requested information soon."

    elif category == "Feedback":
        return "Thank you for your valuable feedback. We appreciate your support."

    elif category == "Cancellation":
        return "Your cancellation request has been received and will be processed shortly."

    else:
        return "Thank you for contacting support."
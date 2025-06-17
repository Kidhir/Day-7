# agents/user_review.py
def review_alt_text(image_data, generated_alt):
    print(f"Image: {image_data['src']}")
    print(f"Old Alt: {image_data['alt']}")
    print(f"Suggested Alt: {generated_alt}")
    user_input = input("Accept suggestion? (y/n/edit): ")
    return generated_alt if user_input.lower() == 'y' else input("Your Edit: ") if user_input == 'edit' else image_data['alt']
